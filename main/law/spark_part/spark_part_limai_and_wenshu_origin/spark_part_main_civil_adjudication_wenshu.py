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
reg_part = re.compile(r'<span litigantpart></span>')  # <a type='dir' name='DSRXX'></a>
reg_process = re.compile(r'<span proceeding></span>')  # <a type='dir' name='SSJL'></a>
reg_argued = re.compile(r'<span argued></span>')  # <a type='dir' name='AJJBQK'></a>
reg_fact = re.compile(r'<span fact></span>')
reg_court = re.compile(r'<span courtconsider></span>')  # <a type='dir' name='CPYZ'></a>
reg_result = re.compile(r'<span result></span>')     #<a type='dir' name='PJJG'></a>
# doc_footer                                       #<a type='dir' name='WBWB'></a>

def foot_get(items):
    reg_footer = re.compile(ur'\n(?:\S{0,2}审判).*(?:书记员|\S+年\S+月)\S+', re.S)
    # reg_footer = re.compile(r'审判'.decode('utf8'), re.S)
    reg_replace = re.compile(ur'附\S+$')
    items = items.replace("\\n", '\n')
    footer_result = re.findall(reg_footer, items)
    if footer_result:
        doc_footer = footer_result[0].strip()
        doc_footer = re.sub(reg_replace, '', doc_footer)
        doc_footer = doc_footer.replace(u"审判长",u" 审判长  ").replace(u"代理审判员", u" 代理审判员")\
            .replace(u"审判员",u" 审判员  ").replace(u"书记员", u" 书记员  ").replace(u"陪审员",u" 陪审员  ")\
            .replace(u"二",u" 二")
        return doc_footer
    else:
        return ""

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
    content_text = HTMLParser.HTMLParser().unescape(content)   #python2的代码
    # content_text = html.unescape(content)    #python3的代码

    content_text = content_text.replace("<a type='dir' name='DSRXX'></a>", "00011").replace("<a type='dir' name='SSJL'></a>","00022") \
        .replace("<a type='dir' name='AJJBQK'></a>", "00033") \
        .replace("<a type='dir' name='CPYZ'></a>", "00044").replace("<a type='dir' name='PJJG'></a>", "00055") \
        .replace("<a type='dir' name='WBWB'></a>", "00066")

    content_text = re.sub(reg_link, "", content_text)    #replace后再去掉<a>标签

    rl = content_text.split("000")
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
            content_dict['result'] = remove_html(i).replace("55", "")
        elif i.startswith("66"):
            content_dict['doc_footer'] = remove_html(i).replace("66", "")

    return content_dict

def doc_items(items):
    id = items[0]
    uuid = items[1]
    doc_content = items[2]

    if not doc_content or not doc_content.startswith('$(fun'):
        return None

    content_text = format_content(doc_content)

    # 格式化后的内容
    # content = content_text.get('content')
    # if len(content) < 120:
    #     return None

    party_info = content_text.get('member', '')
    trial_process = content_text.get('process', '')
    trial_request = content_text.get('request', '')
    court_find = content_text.get('fact', '')
    court_idea = content_text.get('idea', '')
    judge_result = content_text.get('result', '')
    doc_footer = content_text.get('doc_footer', '')

    party_info = party_info.replace("\\n","\n")
    court_find = pymysql.escape_string(court_find).replace("\\n","\n")
    trial_process = pymysql.escape_string(trial_process).replace("\\n","\n")
    trial_request = pymysql.escape_string(trial_request).replace("\\n","\n")
    court_idea = pymysql.escape_string(court_idea).replace("\\n","\n")
    judge_result = pymysql.escape_string(judge_result).replace("\\n","\n")
    doc_footer = pymysql.escape_string(doc_footer).replace("\\n","\n")

    # items_dict = dict(party_info=party_info, trial_process=trial_process, trial_request=trial_request,
    #                   court_find=court_find, court_idea=court_idea, judge_result=judge_result, is_format=1,doc_footer=doc_footer)
    # for j in items_dict.keys():
    #     print(j,":::::::",items_dict[j])
    # print type(party_info)
    return (id,uuid,party_info,trial_process,trial_request,court_find,court_idea,judge_result,doc_footer)

if __name__ == "__main__":

    PYSPARK_PYTHON = "C:\\Python27\\python.exe"    #多版本python情况下，需要配置这个变量指定使用哪个版本
    os.environ["PYSPARK_PYTHON"] = PYSPARK_PYTHON
    conf = SparkConf()
    sc = SparkContext(conf=conf)
    sqlContext = SQLContext(sc)
    # sc.setLogLevel("ERROR")  # ALL, DEBUG, ERROR, FATAL, INFO, OFF, TRACE, WARN '(select id,uuid,plaintiff_info,defendant_info from tmp_lawyers ) tmp'
    # df = sqlContext.read.jdbc(url='jdbc:mysql://192.168.10.22:3306/laws_doc', table='(select id,uuid,doc_content from adjudication_civil where id  >= 1010 and id <= 1041 and doc_from = "limai" ) tmp',column='id',lowerBound=1,upperBound=1800000,numPartitions=1,properties={"user": "tzp", "password": "123456"})
    df = sqlContext.read.jdbc(url='jdbc:mysql://192.168.10.22:3306/laws_doc', table='(select id,uuid,doc_content from adjudication_civil where doc_from = "wenshu" ) tmp',column='id',lowerBound=1,upperBound=3600000,numPartitions=24,properties={"user": "tzp", "password": "123456"})

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

    lawyer_k_v = df.map(lambda x:(x[0],x[1],x[2])).map(lambda x:doc_items(x)).filter(lambda x:filter_(x))

    # (id, uuid, party_info, trial_process, trial_request, court_find, court_idea, judge_result, doc_footer)
    schema = StructType([StructField("id", IntegerType(), False)
                            ,StructField("uuid", StringType(), False)
                            ,StructField("party_info", StringType(), True)
                            ,StructField("trial_process", StringType(), True)
                            ,StructField("trial_request", StringType(), True)
                            ,StructField("court_find", StringType(), True)
                            ,StructField("court_idea", StringType(), True)
                            ,StructField("judge_result", StringType(), True)
                            ,StructField("doc_footer", StringType(), True)])

    f = sqlContext.createDataFrame(lawyer_k_v, schema=schema)
    # f.show()
    # , mode = "overwrite"
    # useUnicode = true & characterEncoding = utf8，指定写入mysql时的数据编码，否则会乱码。
    f.write.jdbc(url='jdbc:mysql://cdh-slave1:3306/laws_doc_adjudication?useUnicode=true&characterEncoding=utf8', table='adjudication_civil_etl_wenshu',properties={"user": "root", "password": "root"})

    sc.stop()
