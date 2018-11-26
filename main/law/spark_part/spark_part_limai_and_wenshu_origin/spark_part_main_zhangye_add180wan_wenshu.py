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
import os

reg_link = re.compile(r"<a[^>]+>|</a>", flags=re.S)
reg_blank = re.compile(r'((?!\n)\s)*', flags=re.S)
reg_part = re.compile(r'<span litigantpart></span>')  # <a type='dir' name='DSRXX'></a>, 当事人信息
reg_process = re.compile(r'<span proceeding></span>')  # <a type='dir' name='SSJL'></a>，审理过程
reg_argued = re.compile(r'<span argued></span>')  # <a type='dir' name='AJJBQK'></a> ，诉讼请求
reg_fact = re.compile(r'<span fact></span>')                                         #法院查明
reg_court = re.compile(r'<span courtconsider></span>')  # <a type='dir' name='CPYZ'></a> #法院认为
reg_result = re.compile(r'<span result></span>')     #<a type='dir' name='PJJG'></a>    #判决结果
# doc_footer                                       #<a type='dir' name='WBWB'></a>


def format_content(content, b_value):
    """
    理脉网内容分段
    :param content:
    :return:
    """
    content_dict = dict()

    # s1 = ur"var[ ]{0,5}jsonHtmlData[ ]{0,5}="
    # s2 = ur""

    # html_content = re.split(ur"var[ ]{0,5}jsonHtmlData[ ]{0,5}=|var[ ]{0,5}jsonData[ ]{0,5}=", content)
    # html_content = re.split(ur"var jsonHtmlData =|var jsonData =", content)
    # html_content = re.split(ur"{\"{\\\"Title\\\":|\\\"}\";", content)
    # if len(html_content) > 1:
    #     content_text = html_content[1]
    # else:
    #     return None

    content_text = HTMLParser.HTMLParser().unescape(content)  # python2的代码
    # content_text = html.unescape(content)    #python3的代码

    # , "不公开理由":"",
    # ur"[\u4e00-\u9fa5]"
    # pri_reason_re = re.search(ur"不公开理由\":\"[\u4e00-\u9fa5]{0,200}\"",content_text)    #等价于下面的方式，使用三个引号‘’‘将字符串括起来。
    pri_reason_re = re.search(ur'''不公开理由":"[\u4e00-\u9fa5]{0,200}"''',content_text)
    if pri_reason_re:
        content_dict['pri_reason'] = pri_reason_re.group(0).replace(ur'''不公开理由":"''',"").replace(ur'''"''',"")
        # content_dict['pri_reason'] = pri_reason_re.group(0).split(":")[1]


    content_text = content_text.replace("<a type='dir' name='DSRXX'></a>", "00011").replace(
        "<a type='dir' name='SSJL'></a>", "00022") \
        .replace("<a type='dir' name='AJJBQK'></a>", "00033") \
        .replace("<a type='dir' name='CPYZ'></a>", "00044").replace("<a type='dir' name='PJJG'></a>", "00055") \
        .replace("<a type='dir' name='WBWB'></a>", "00066")

    content_text = re.sub(reg_link, "", content_text)  # replace后再去掉<a>标签

    rl = content_text.split("000")

    ss = remove_html(rl[0])
    content_dict['court'] = ""
    # "法院名称":"长沙市望城区人民法院"
    court_re = re.search(ur'''法院名称":"[\u4e00-\u9fa5]{3,200}"''', content_text)
    if court_re:
        content_dict['court'] = court_re.group(0).replace(ur'''法院名称":"''', "").replace(ur'''"''', "")
    else:
        for c in b_value:
            if c in ss:
                content_dict['court'] = c
                break

    for i in rl:
        if i.startswith("11"):
            content_dict['member'] = remove_html(i).replace("11", "")
        elif i.startswith("22"):
            content_dict['process'] = remove_html(i).replace("22", "")
        elif i.startswith("33"):
            content_dict['request'] = remove_html(i).replace("33", "")
        elif i.startswith("44"):
            content_dict['idea'] = remove_html(i).replace("44", "")
        elif i.startswith("55"):
            content_dict['result'] = re.split(ur"\\\"}\";", remove_html(i).replace("55", ""))[0]
        elif i.startswith("66"):
            content_dict['doc_footer'] = re.split(ur"\\\"}\";", remove_html(i).replace("66", ""))[0]

    return content_dict


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


def doc_items(items, b_value):
    id = items[0]
    uuid = items[1]
    doc_content = items[2]

    if not doc_content or not doc_content.startswith('$(fun'):
        return None

    content_text = format_content(doc_content, b_value)
    if not content_text:
        return None

    party_info = content_text.get('member', '')
    trial_process = content_text.get('process', '')
    trial_request = content_text.get('request', '')
    court_find = content_text.get('fact', '')
    court_idea = content_text.get('idea', '')
    judge_result = content_text.get('result', '')
    doc_footer = content_text.get('doc_footer', '')
    court = content_text.get('court', '')

    pri_reason = content_text.get('pri_reason',"")

    if party_info == "" and trial_process == "" and trial_request == "" and court_find == "" and court_idea == "" and judge_result == "":  # 没有当事人、判决结果的文书，没有意义！
        party_info = pri_reason    #如果长文本字段都没有，则将未公开理由放到当事人信息里！！

    party_info = party_info.replace("\\n", "\n")
    court_find = pymysql.escape_string(court_find).replace("\\n", "\n")
    trial_process = pymysql.escape_string(trial_process).replace("\\n", "\n")
    trial_request = pymysql.escape_string(trial_request).replace("\\n", "\n")
    court_idea = pymysql.escape_string(court_idea).replace("\\n", "\n")
    judge_result = pymysql.escape_string(judge_result).replace("\\n", "\n")
    doc_footer = pymysql.escape_string(doc_footer).replace("\\n", "\n")

    # items_dict = dict(party_info=party_info, trial_process=trial_process, trial_request=trial_request,
    #                   court_find=court_find, court_idea=court_idea, judge_result=judge_result, is_format=1,doc_footer=doc_footer)
    # for j in items_dict.keys():
    #     print(j,":::::::",items_dict[j])
    # print type(party_info)
    return (id, uuid, party_info, trial_process, trial_request, court_find, court_idea, judge_result, doc_footer, court)


if __name__ == "__main__":

    # PYSPARK_PYTHON = "C:\\Python27\\python.exe"    #多版本python情况下，需要配置这个变量指定使用哪个版本
    # os.environ["PYSPARK_PYTHON"] = PYSPARK_PYTHON
    conf = SparkConf()
    sc = SparkContext(conf=conf)
    sqlContext = SQLContext(sc)
    # sc.setLogLevel("ERROR")  # ALL, DEBUG, ERROR, FATAL, INFO, OFF, TRACE, WARN '(select id,uuid,plaintiff_info,defendant_info from tmp_lawyers ) tmp'
    # df = sqlContext.read.jdbc(url='jdbc:mysql://192.168.10.22:3306/laws_doc', table='(select id,uuid,doc_content from adjudication_civil where id  >= 1010 and id <= 1041 and doc_from = "limai" ) tmp',column='id',lowerBound=1,upperBound=1800000,numPartitions=1,properties={"user": "tzp", "password": "123456"})
    df = sqlContext.read.jdbc(url='jdbc:mysql://10.41.104.5:3306/laws_doc', table='(select id,uuid,doc_content from judgment where id > 4816521 and id <= 5816521 ) tmp',column='id',lowerBound=4816521,upperBound=5816521,numPartitions=24,properties={"user": "root", "password": "Hhly@2018"})

    df2 = sqlContext.read.jdbc(url='jdbc:mysql://cdh-slave1:3306/laws_doc',
                               table='(select id,name from court where name is not null ) tmp', column='id',
                               lowerBound=1, upperBound=5000, numPartitions=1,
                               properties={"user": "weiwc", "password": "HHly2017."})

    def filter_(x):
        if x is not None :
            return True
        return False


    court_value = sc.broadcast(df2.map(lambda x: x[1]).collect()).value

    lawyer_k_v = df.map(lambda x:(x[0],x[1],x[2])).map(lambda x:doc_items(x,court_value)).filter(lambda x:filter_(x))


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
                            ,StructField("court", StringType(), True)])

    f = sqlContext.createDataFrame(lawyer_k_v, schema=schema)
    # f.show()
    # , mode = "overwrite"
    # useUnicode = true & characterEncoding = utf8，指定写入mysql时的数据编码，否则会乱码。
    # f.write.jdbc(url='jdbc:mysql://cdh-slave1:3306/laws_doc_zhangye_update1?useUnicode=true&characterEncoding=utf8', table='judgment_zhangye_etl01',properties={"user": "root", "password": "root"},mode="overwrite")
    f.write.jdbc(url='jdbc:mysql://cdh-slave1:3306/laws_doc_zhangye_update2?useUnicode=true&characterEncoding=utf8', table='judgment_zhangye_add180wan_etl01',properties={"user": "root", "password": "root"})
    sc.stop()
