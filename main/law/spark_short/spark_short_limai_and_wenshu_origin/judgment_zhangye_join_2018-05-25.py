# -*- coding: utf-8 -*-

from  pyspark import SparkContext,SparkConf
from pyspark.sql import SQLContext
from pyspark.sql.types import *
import os
import time

import re
if __name__ == "__main__":

    conf = SparkConf()
    sc = SparkContext(conf=conf)
    sqlContext = SQLContext(sc)

    # PYSPARK_PYTHON = "C:\\Python27\\python.exe"    #多版本python情况下，需要配置这个变量指定使用哪个版本
    # os.environ["PYSPARK_PYTHON"] = PYSPARK_PYTHON

    def p(x):
        print type(x),type(x[0]),type(x[1])
        # print type(x)
        # print type(x[0]),type(x[1])
        print x[0],x[1][0],x[1][1]


    # judgment_new：556万,3030306	3392975
    df = sqlContext.read.jdbc(url='jdbc:mysql://cdh-slave1:3306/laws_doc_zhangye_etl',
                               table='(select * from judgment_zhangye_etl01  ) tmp',
                               column='id', lowerBound=1, upperBound=4816521, numPartitions=28,
                               properties={"user": "weiwc", "password": "HHly2017."})
    # court:4778条
    df1 = sqlContext.read.jdbc(url='jdbc:mysql://cdh-slave1:3306/laws_doc_zhangye_etl',
                               table='(select id,doc_id,case_name,case_type,case_number,jud_pro,jud_date from judgment_doc  ) tmp',
                               column='id', lowerBound=1, upperBound=21730222, numPartitions=56,
                               properties={"user": "weiwc", "password": "HHly2017."})

    # id,uuid,party_info,trial_process,trial_request,court_find,court_idea,judge_result,doc_footer,court
    uuid_x = df.map(lambda x:(x[1],x))

    # id,doc_id,case_name,case_type,case_number,jud_pro,jud_date
    uuid_x2 = df1.map(lambda x:(x[1],(x[2],x[3],x[4],x[5],x[6])))

    def get_result(x):
        judge_type = ""
        if x[1][0] and x[1][0] != "":
            if x[1][0].endswith(u"判决书"):
                judge_type = u"判决"
            elif x[1][0].endswith(u"裁定书"):
                judge_type = u"裁定"
            elif x[1][0].endswith(u"调解书"):
                judge_type = u"调解"
            elif x[1][0].endswith(u"决定书"):
                judge_type = u"决定"
            elif x[1][0].endswith(u"通知书"):
                judge_type = u"通知"
        # lawlist = ""


        return (x[0][0],x[0][1],x[0][2],x[0][3],x[0][4],x[0][5],x[0][6],x[0][7],x[0][8],x[0][9],x[1][0],x[1][1],x[1][2],x[1][3],x[1][4],judge_type)

    result = uuid_x.join(uuid_x2).map(lambda x:x[1]).map(lambda x:get_result(x))

    schema = StructType([StructField("id", StringType(), False),
                         StructField("uuid", StringType(), False),
                         StructField("party_info", StringType(), True),
                         StructField("trial_process", StringType(), True),
                         StructField("trial_request", StringType(), True),
                         StructField("court_find", StringType(), True),
                         StructField("court_idea", StringType(), True),
                         StructField("judge_result", StringType(), True),
                         StructField("doc_footer", StringType(), True),
                         StructField("court", StringType(), True),
                         StructField("title", StringType(), True),
                         StructField("reason_type", StringType(), True),
                         StructField("caseid", StringType(), True),
                         StructField("type", StringType(), True),
                         StructField("casedate", StringType(), True),
                         StructField("judge_type", StringType(), True)
                         # StructField("lawlist", StringType(), True)
                         ])

    f = sqlContext.createDataFrame(result, schema=schema)
    # , mode = "overwrite"
    # useUnicode = true & characterEncoding = utf8，指定写入mysql时的数据编码，否则会乱码。
    # print str(f.count()) + "======================"
    f.write.jdbc(url='jdbc:mysql://cdh-slave1:3306/laws_doc_zhangye_etl?useUnicode=true&characterEncoding=utf8', table='judgment_zhangye_join_all',properties={"user": "weiwc", "password": "HHly2017."})

    sc.stop()