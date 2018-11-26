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
import time

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
    reg_footer = re.compile(ur'\n(?:\S{0,2}审[　  ]{0,2}判|\S{0,2}执[　  ]{0,2}行员|\S{0,2}院[　  ]{0,2}长).*(?:书[　  ]{0,2}记员|\S+年\S+月)\S+', re.S)
    items = items.replace("\\n", '\n')
    footer_result = re.findall(reg_footer, items)

    if footer_result:
        # footer_result[0]中可能有特殊符号：类似？号等等，？在split的pattern中属于特殊字符，因此要替换掉再分割.
        items_tmp = items.replace(footer_result[0],"!1qw23er4!")

        lp = re.split("!1qw23er4!",items_tmp)
        doc_footer = footer_result[0].strip() + lp[1]

        doc_footer = doc_footer.replace(u"审判长",u" 审判长  ").replace(u"代理审判员", u" 代理审判员")\
            .replace(u"审判员",u" 审判员  ").replace(u"书记员", u" 书记员  ").replace(u"陪审员",u" 陪审员  ")\
            .replace(u"二",u" 二").replace(u"执行员",u" 执行员 ").replace(u"院长",u" 院长 ")
        return lp[0],doc_footer   #result,doc_footer
    else:
        return items,""

def doc_items(items):
    # id, uuid, judge_result, doc_footer, court_idea
    id = items[0]
    uuid = items[1]
    judge_result = items[2]
    doc_footer = items[3]
    court_idea = items[4]

    doc_footer = doc_footer.replace("u3000","  ")
    judge_result = judge_result.replace("u3000","  ")
    court_idea = court_idea.replace("u3000","  ")

    if doc_footer == "" :
        judge_result, doc_footer = foot_get(judge_result)
        #否则就是未分段，直接使用court_idea即可。

    return (id,uuid,court_idea,judge_result,doc_footer)

if __name__ == "__main__":

    # PYSPARK_PYTHON = "C:\\Python27\\python.exe"    #多版本python情况下，需要配置这个变量指定使用哪个版本
    # os.environ["PYSPARK_PYTHON"] = PYSPARK_PYTHON
    conf = SparkConf()
    sc = SparkContext(conf=conf)
    sqlContext = SQLContext(sc)
    # sc.setLogLevel("ERROR")  # ALL, DEBUG, ERROR, FATAL, INFO, OFF, TRACE, WARN '(select id,uuid,plaintiff_info,defendant_info from tmp_lawyers ) tmp'
    # df = sqlContext.read.jdbc(url='jdbc:mysql://192.168.10.22:3306/laws_doc', table='(select id,uuid,doc_content from adjudication_civil where id  >= 1010 and id <= 1041 and doc_from = "limai" ) tmp',column='id',lowerBound=1,upperBound=1800000,numPartitions=1,properties={"user": "tzp", "password": "123456"})
    df = sqlContext.read.jdbc(url='jdbc:mysql://192.168.74.102:3306/laws_doc_judgment', table='(select id,uuid,judge_result,doc_footer,court_idea from judgment_etl_v2  where doc_footer like "%u3000%" or judge_result like "%u3000%" or court_idea like "%u3000%") tmp',column='id',lowerBound=1,upperBound=3861714,numPartitions=99,properties={"user": "weiwc", "password": "HHly2017."})

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

    lawyer_k_v = df.map(lambda x:x).map(lambda x:doc_items(x))

    # (id, uuid, party_info, trial_process, trial_request, court_find, court_idea, judge_result, doc_footer)
    schema = StructType([StructField("id", IntegerType(), False)
                            ,StructField("uuid", StringType(), False)
                            ,StructField("court_idea", StringType(), True)
                            ,StructField("judge_result", StringType(), True)
                            ,StructField("doc_footer", StringType(), True)

                         ])

    f = sqlContext.createDataFrame(lawyer_k_v, schema=schema)
    # f.show()
    # , mode = "overwrite"
    # useUnicode = true & characterEncoding = utf8，指定写入mysql时的数据编码，否则会乱码。
    f.write.jdbc(url='jdbc:mysql://cdh5-slave2:3306/laws_doc_judgment?useUnicode=true&characterEncoding=utf8', table='doc_footer_u3000',properties={"user": "weiwc", "password": "HHly2017."})

    sc.stop()
