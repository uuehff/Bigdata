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



if __name__ == "__main__":

    # PYSPARK_PYTHON = "C:\\Python27\\python.exe"    #多版本python情况下，需要配置这个变量指定使用哪个版本
    # os.environ["PYSPARK_PYTHON"] = PYSPARK_PYTHON
    conf = SparkConf()
    sc = SparkContext(conf=conf)
    sqlContext = SQLContext(sc)
    # sc.setLogLevel("ERROR")  # ALL, DEBUG, ERROR, FATAL, INFO, OFF, TRACE, WARN '(select id,uuid,plaintiff_info,defendant_info from tmp_lawyers ) tmp'
    # df = sqlContext.read.jdbc(url='jdbc:mysql://192.168.10.22:3306/laws_doc', table='(select id,uuid,doc_content from adjudication_civil where id  >= 1010 and id <= 1041 and doc_from = "limai" ) tmp',column='id',lowerBound=1,upperBound=1800000,numPartitions=1,properties={"user": "tzp", "password": "123456"})
    df = sqlContext.read.jdbc(url='jdbc:mysql://192.168.74.103:3306/civil', table='(select id,type,judge_type,doc_from from judgment  where is_crawl = 1) tmp',column='id',lowerBound=1,upperBound=16437624,numPartitions=40,properties={"user": "weiwc", "password": "HHly2017."})

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

    lawyer_k_v = df.map(lambda x:(x[1] + "|" + x[2]+ "|" +x[3],1)).reduceByKey(lambda x,y:x+y)

    # (id, uuid, party_info, trial_process, trial_request, court_find, court_idea, judge_result, doc_footer)
    schema = StructType([StructField("reason_type_type_judge_type_doc_from", StringType(), True)
                            , StructField("count_num", IntegerType(), True)
                            # , StructField("judge_type", StringType(), True)
                            # , StructField("doc_from", StringType(), True)
                         ])

    f = sqlContext.createDataFrame(lawyer_k_v, schema=schema)
    # f.show()
    # , mode = "overwrite"
    # useUnicode = true & characterEncoding = utf8，指定写入mysql时的数据编码，否则会乱码。
    f.write.jdbc(url='jdbc:mysql://cdh5-slave3:3306/civil?useUnicode=true&characterEncoding=utf8', table='judgment__reason_type_type_judge_type',properties={"user": "weiwc", "password": "HHly2017."})

    sc.stop()
