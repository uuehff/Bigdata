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
    df = sqlContext.read.jdbc(url='jdbc:mysql://192.168.74.102:3306/laws_doc', table='(select id,uuid,age_year,court_cate,delay_date,duration,edu,gender,if_accumulate,if_adult,if_delay,if_surrender,if_team,lawyer_id,nation,law_office,province,punish_cate,punish_date,punish_money,degree from judgment_visualization_v2 ) tmp',column='id',lowerBound=1,upperBound=2630629,numPartitions=99,properties={"user": "weiwc", "password": "HHly2017."})

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


    def doc_items(items):
        # id, uuid, age_year, court_cate, delay_date, \
        # duration, edu, gender, if_accumulate, if_adult, \
        # if_delay, if_surrender, if_team, lawyer_id, nation, law_office, \
        # province, punish_cate, punish_date, punish_money, degree

        uuid = unicode(UUID.uuid3(UUID.NAMESPACE_DNS2, items[1].encode("utf8"))).replace("-", "")
        return (items[0],uuid,items[2],items[3],items[4],
                items[5],items[6],items[7],items[8],items[9],
                items[10],items[11],items[12],items[13],items[14],
                items[15],items[16],items[17],items[18],items[19],items[20])

    lawyer_k_v = df.map(lambda x:x).map(lambda x:doc_items(x))


    # id, uuid, age_year, court_cate, delay_date, \
    # duration, edu, gender, if_accumulate, if_adult, \
    # if_delay, if_surrender, if_team, lawyer_id, nation, law_office, \
    # province, punish_cate, punish_date, punish_money, degree
    schema = StructType([StructField("id", IntegerType(), False)
                            ,StructField("uuid", StringType(), False)
                            ,StructField("age_year", StringType(), True)
                            ,StructField("court_cate", StringType(), True)
                            ,StructField("delay_date", StringType(), True)
                            ,StructField("duration", StringType(), True)
                            ,StructField("edu", StringType(), True)
                            ,StructField("gender", StringType(), True)
                            ,StructField("if_accumulate", StringType(), True)
                            , StructField("if_adult", StringType(), True)
                            , StructField("if_delay", StringType(), True)
                            , StructField("if_surrender", StringType(), True)
                            , StructField("if_team", StringType(), True)
                            , StructField("lawyer_id", StringType(), True)
                            , StructField("nation", StringType(), True)
                            , StructField("law_office", StringType(), True)
                            , StructField("province", StringType(), True)
                            , StructField("punish_cate", StringType(), True)
                            , StructField("punish_date", StringType(), True)
                            , StructField("punish_money", StringType(), True)
                            , StructField("degree", StringType(), True)
                         ])

    f = sqlContext.createDataFrame(lawyer_k_v, schema=schema)
    # f.show()
    # , mode = "overwrite"
    # useUnicode = true & characterEncoding = utf8，指定写入mysql时的数据编码，否则会乱码。
    f.write.jdbc(url='jdbc:mysql://cdh5-slave2:3306/laws_doc_judgment?useUnicode=true&characterEncoding=utf8', table='judgment_visualization_v2_only',properties={"user": "weiwc", "password": "HHly2017."})

    sc.stop()
