# -*- coding: utf-8 -*-
"""
对抓取的文书内容进行数据提取
"""
import re
from  pyspark import SparkContext,SparkConf
from pyspark.sql import SQLContext
from pyspark.sql.types import *
import json
import pymysql
from lxml import etree
import HTMLParser
import uuid as UUID


reg_link = re.compile(r"<a[^>]+>|</a>", flags=re.S)
reg_blank = re.compile(r'((?!\n)\s)*', flags=re.S)
reg_part = re.compile(r'<span litigantpart></span>')
reg_process = re.compile(r'<span proceeding></span>')
reg_argued = re.compile(r'<span argued></span>')
reg_fact = re.compile(r'<span fact></span>')
reg_court = re.compile(r'<span courtconsider></span>')
reg_result = re.compile(r'<span result></span>')

def foot_get(items):
    # judge_result:
    # 准许原告暨诉讼代表人撤回起诉。
    # 案件受理费50元，减半收取25元，由原告暨诉讼代表人负担。
    # 审判长吴铁梅
    # 审判员殷载媛
    # 人民陪审员肖正江
    # 二〇一七年一月十日
    # 书记员欧阳小玲

    # ?  0或1次，+ 1或多， * 0或多
    # reg_footer = re.compile(ur'\n(?:\S{0,2}审判).*(?:书记员|\S+年\S+月)\S+', re.S)
    # 附里面的当事人信息里面也有年月的匹配。
    # re.S开启了.匹配任意字符串，用(?:和)将其之间的内容作为一个整体，而不是用（），\n(?:\S{0,2}审判)，其中judge_result中的空格都已去掉，有的只是
    # 换行回车等：\f\n\r\t\v，审判前面匹配0-2个非空字符，可能匹配到代理等词，再前面是\n，是判决结果那句话与下面的换行符。
    # .*匹配任意字符，(?:书记员|\S+年\S+月)\S+，这里能匹配到“书记员，代书记员，或者多个书记员等等”，匹配到最后一个符合条件的值，
    # 拆开为：匹配到最后一个.*书记员\S+ 或 匹配到最后一个.*\S+年\S+月\S+，哪个的值在最最后，就以哪个的匹配值结尾。\S+匹配任意非空，遇空（\f\n\r\t\v）就停止。
    # reg_footer = re.compile(ur'\n(?:\S{0,2}审判).*(?:书记员|\S+年\S+月)\S+', re.S)
    reg_footer = re.compile(ur'\n(?:\S{0,2}审判|\S{0,2}执行员).*(?:\S{0,2}书记员|\S+年\S+月)\S+', re.S)
    items = items.replace("\\n", '\n')
    footer_result = re.findall(reg_footer, items)

    if footer_result:
        # footer_result[0]中可能有特殊符号：类似？号等等，？在split的pattern中属于特殊字符，因此要替换掉再分割.
        items_tmp = items.replace(footer_result[0],"!1qw23er4!")

        lp = re.split("!1qw23er4!",items_tmp)
        doc_footer = footer_result[0].strip() + lp[1]

        doc_footer = doc_footer.replace(u"审判长",u" 审判长  ").replace(u"代理审判员", u" 代理审判员")\
            .replace(u"审判员",u" 审判员  ").replace(u"书记员", u" 书记员  ").replace(u"陪审员",u" 陪审员  ")\
            .replace(u"二",u" 二")
        return lp[0],doc_footer   #result,doc_footer
    else:
        return items,""

def remove_html(html_data):
    """
    移除HTML标签
    :param html_data:
    :return:
    """
    html_item = re.sub(reg_blank, "", html_data)
    if html_item:
        item_list = etree.HTML(html_item).xpath('//text()')
        html_text = "\n".join(item_list).strip()
    else:
        html_text = ''
    return html_text

def format_content(content):
    """
    理脉网内容分段
    :param content:
    :return:
    """

    content_dict = dict()
    content_text = HTMLParser.HTMLParser().unescape(content)
    # content_text = html.unescape(content)
    content_text = re.sub(reg_link, "", content_text)

    content_text = content_text.replace("<span litigantpart></span>","0|0|0|11").replace("<span proceeding></span>","0|0|0|22").replace("<span argued></span>","0|0|0|33") \
        .replace("<span fact></span>", "0|0|0|44").replace("<span courtconsider></span>", "0|0|0|55") \
        .replace("<span result></span>", "0|0|0|66")

    rl = content_text.split("0|0|0|")
    ss = remove_html(rl[0])
    content_dict['court'] = ""
    for c in court.value:
        if c in ss:
            content_dict['court'] = c
            break
    content_dict['caseid'] = ""
    if len(ss.split(u"（20")) == 2:
        content_dict['caseid'] = u"（20" + ss.split(u"（20")[1]

    for i in rl:
        if i.startswith("11"):
            content_dict['member'] = remove_html(i).replace("11","")
        elif i.startswith("22"):
            content_dict['process'] = remove_html(i).replace("22","")
        elif i.startswith("33"):
            content_dict['request'] = remove_html(i).replace("33","")
        elif i.startswith("44"):
            content_dict['fact'] = remove_html(i).replace("44","")
        elif i.startswith("55"):
            content_dict['idea'] = remove_html(i).replace("55","")
        elif i.startswith("66"):
            content_dict['result'] = remove_html(i).replace("66","")

    return content_dict,content_text

def doc_items(items):
    # id, uuid, doc_content, title, lawlist, reason_type, type, judge_type
    id = items[0]
    uuid = items[1]
    doc_content = items[2]
    title = items[3]
    lawlist = items[4]
    reason_type = items[5]
    type = items[6]
    judge_type = items[7]

    if not doc_content or not doc_content.endswith('/div&gt;') :
        return None


    content_text,doc_text = format_content(doc_content)
    # if not content_text:
    #     return None

    # 格式化后的内容
    # content = content_text.get('content')
    # if len(content) < 120:
    #     return None

    party_info = content_text.get('member', '').replace("\\n","\n").replace(r'''\\r''',"").replace("\\r","")
    trial_process = content_text.get('process', '')
    trial_request = content_text.get('request', '')
    court_find = content_text.get('fact', '')
    court_idea = content_text.get('idea', '')
    judge_result = content_text.get('result', '')
    court = content_text.get('court', '')
    caseid = content_text.get('caseid', '')

    # In [10]: print uuid.uuid3(uuid.NAMESPACE_DNS,"http://uat_datalaw.fy13322.com")
    # e779e0fa-5386-3732-b1ab-5252efcbe561    #使用默认UUID.NAMESPACE_DNS和平台网址生成新的命名空间NAMESPACE_DNS
    # uuid_ = UUID.uuid3(UUID.NAMESPACE_DNS, uuid)
    uuid_ = unicode(UUID.uuid3(UUID.NAMESPACE_DNS2, uuid.encode("utf8"))).replace("-","")  #基于平台的命名空间 + uuid确定新的uuid_,uuid_是一个对象，需要转化为字符串


    court_find = pymysql.escape_string(court_find).replace("\\n","\n").replace(r'''\\r''',"").replace("\\r","")
    trial_process = pymysql.escape_string(trial_process).replace("\\n","\n").replace(r'''\\r''',"").replace("\\r","")
    trial_request = pymysql.escape_string(trial_request).replace("\\n","\n").replace(r'''\\r''',"").replace("\\r","")
    court_idea = pymysql.escape_string(court_idea).replace("\\n","\n").replace(r'''\\r''',"").replace("\\r","")
    judge_result = pymysql.escape_string(judge_result).replace("\\n","\n").replace(r'''\\r''',"").replace("\\r","")
    judge_result,doc_footer = foot_get(judge_result)

    court_idea_all = party_info  + trial_process + trial_request + court_find + court_idea + judge_result + doc_footer
    # 无标签下的数据处理
    if court_idea_all == "":
        doc_text = remove_html(doc_text)
        # reg_caseid = re.compile(ur'\n[(（](?:20|19|2０|2O)\S+号\S*', re.S)
        reg_caseid = re.compile(ur'\n[(（](?:20|19|2０|2O)\S+号\S*', re.S) #\S* 号下面有0或多个非空字符
        doc_result = re.findall(reg_caseid, doc_text)

        if doc_result:
            doc_tmp = doc_text.replace(doc_result[0], "!1qw23er4!")
            court_idea = re.split("!1qw23er4!", doc_tmp)[1]
            if court_idea == "":
                return None

        elif len(doc_text) < 50 and doc_text != "":    #无标签，无案号，是不公开的数据
            court_idea = doc_text
        else:                   #无标签，无案号，且不是不公开的
            return None

    # 对最终的court_idea做处理，包含有标签和无标签得到的court_idea
    c_r = re.compile(ur"[^\u4e00-\u9fa5]")  #去除court_idea开头不为汉字的。
    if re.match(c_r,court_idea.strip()):
        if  court_idea_all == "":   #无标签的数据，court_idea为空的。
            return None
        elif court_idea_all.replace(court_idea,"") == "":  #有标签的数据，除了court_idea之外全为空的。
            return None
        else:                       # 有标签的数据，除了court_idea之外,其他字段还有值的。
            court_idea = ""

            # for i in remove_html(doc_text).split("\n"):
            #     print "0====" + i
    court_idea.replace("\\n", "\n").replace(r'''\\r''',"").replace("\\r","")
    return (id,uuid,party_info,trial_process,trial_request,court_find,court_idea,judge_result,doc_footer,court,caseid,uuid_,title, lawlist, reason_type, type, judge_type)


    # items_dict = dict(party_info=party_info, trial_process=trial_process, trial_request=trial_request,
    #                   court_find=court_find, court_idea=court_idea, judge_result=judge_result, is_format=1,doc_footer=doc_footer,court = court,caseid = caseid)
    # for j in items_dict.keys():
    #     print(j,":::::::",items_dict[j])
    # print type(party_info)

if __name__ == "__main__":

    # PYSPARK_PYTHON = "C:\\Python27\\python.exe"    #多版本python情况下，需要配置这个变量指定使用哪个版本
    # os.environ["PYSPARK_PYTHON"] = PYSPARK_PYTHON
    conf = SparkConf()
    sc = SparkContext(conf=conf)
    sqlContext = SQLContext(sc)
    # sc.setLogLevel("ERROR")  # ALL, DEBUG, ERROR, FATAL, INFO, OFF, TRACE, WARN '(select id,uuid,plaintiff_info,defendant_info from tmp_lawyers ) tmp'
    # df = sqlContext.read.jdbc(url='jdbc:mysql://192.168.10.22:3306/laws_doc', table='(select id,uuid,doc_content from adjudication_civil where id  >= 1010 and id <= 1041 and doc_from = "limai" ) tmp',column='id',lowerBound=1,upperBound=1800000,numPartitions=1,properties={"user": "tzp", "password": "123456"})
    df = sqlContext.read.jdbc(url='jdbc:mysql://192.168.10.22:3306/laws_doc', table='(select id,uuid,doc_content,title,lawlist,reason_type,type,judge_type from administration ) tmp',column='id',lowerBound=1,upperBound=550542,numPartitions=96,properties={"user": "tzp", "password": "123456"})
    df2 = sqlContext.read.jdbc(url='jdbc:mysql://cdh5-slave2:3306/laws_doc', table='(select id,name from court where name is not null ) tmp',column='id',lowerBound=1,upperBound=5000,numPartitions=1,properties={"user": "weiwc", "password": "HHly2017."})

    def p(x):
        print type(x),x
        # print type(x[0]),type(x[1]),type(x[2]),type(x[3]),type(x[4])
        # if len(x) >6:
        #     print x[0],x[1],x[2],x[3],x[4],x[5],x[6]
        # else:print x[0],x[1],x[2],x[3],x[4],x[5]
    def filter_(x):
        if x :
            return True
        return False

    court = sc.broadcast(df2.map(lambda x:x[1]).collect())
    # lawyer_k_v = df.map(lambda x:(x[0],x[1],x[2])).map(lambda x:doc_items(x)).filter(lambda x:filter_(x))
    lawyer_k_v = df.map(lambda x:x).map(lambda x:doc_items(x)).filter(lambda x:filter_(x))

    # (id, uuid, party_info, trial_process, trial_request, court_find, court_idea, judge_result, doc_footer)
    schema = StructType([StructField("id", IntegerType(), False)
                            ,StructField("uuid", StringType(), False)
                            ,StructField("party_info", StringType(), True)
                            ,StructField("trial_process", StringType(), True)
                            ,StructField("trial_request", StringType(), True)
                            ,StructField("court_find", StringType(), True)
                            ,StructField("court_idea", StringType(), True)
                            ,StructField("judge_result", StringType(), True)
                            ,StructField("doc_footer", StringType(), True)
                            ,StructField("court", StringType(), True)
                            ,StructField("caseid", StringType(), True)
                            ,StructField("uuid_", StringType(), True)
                            ,StructField("title", StringType(), True)
                            ,StructField("lawlist", StringType(), True)
                            ,StructField("reason_type", StringType(), True)
                            ,StructField("type", StringType(), True)
                            ,StructField("judge_type", StringType(), True)
                            ])

    f = sqlContext.createDataFrame(lawyer_k_v, schema=schema)
    # f.show()
    # , mode = "overwrite"
    # useUnicode = true & characterEncoding = utf8，指定写入mysql时的数据编码，否则会乱码。
    f.write.jdbc(url='jdbc:mysql://cdh5-slave2:3306/laws_doc_administration?useUnicode=true&characterEncoding=utf8', table='administration_etl_v3',properties={"user": "weiwc", "password": "HHly2017."})

    sc.stop()

