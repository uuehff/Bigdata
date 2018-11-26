# -*- coding: utf-8 -*-
"""
对抓取的文书内容进行数据提取
"""
import re
from  pyspark import SparkContext,SparkConf
from pyspark.sql import SQLContext
from pyspark.sql.types import *



if __name__ == "__main__":

    # PYSPARK_PYTHON = "C:\\Python27\\python.exe"    #多版本python情况下，需要配置这个变量指定使用哪个版本
    # os.environ["PYSPARK_PYTHON"] = PYSPARK_PYTHON
    conf = SparkConf()
    sc = SparkContext(conf=conf)
    sqlContext = SQLContext(sc)
    # sc.setLogLevel("ERROR")  # ALL, DEBUG, ERROR, FATAL, INFO, OFF, TRACE, WARN '(select id,uuid,plaintiff_info,defendant_info from tmp_lawyers ) tmp'
    # df = sqlContext.read.jdbc(url='jdbc:mysql://192.168.10.22:3306/laws_doc', table='(select id,uuid,doc_content from adjudication_civil where id  >= 1010 and id <= 1041 and doc_from = "limai" ) tmp',column='id',lowerBound=1,upperBound=1800000,numPartitions=1,properties={"user": "tzp", "password": "123456"})
    df = sqlContext.read.jdbc(url='jdbc:mysql://slave2:3306/civil_v2', table="(select id,uuid_,party_info,trial_process,trial_request,court_find,court_idea,judge_result,doc_footer,caseid,title,court,lawlist,casedate,reason_type,type,judge_type from judgment_new_v2 ) tmp ",column='id',lowerBound=1,upperBound=6003507,numPartitions=99,properties={"user": "weiwc", "password": "HHly2017."})


    lawyer_k_v = df.map(lambda x:x)

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
                            , StructField("caseid", StringType(), True)
                            , StructField("title", StringType(), True)
                            , StructField("court", StringType(), True)
                            , StructField("lawlist", StringType(), True)
                            , StructField("casedate", StringType(), True)
                            , StructField("reason_type", StringType(), True)
                            , StructField("type", StringType(), True)
                            , StructField("judge_type", StringType(), True)
                         ])

    f = sqlContext.createDataFrame(lawyer_k_v, schema=schema)
    # f.show()
    # , mode = "overwrite"
    # useUnicode = true & characterEncoding = utf8，指定写入mysql时的数据编码，否则会乱码。
    f.write.jdbc(url='jdbc:mysql://slave2:3306/civil_v2?useUnicode=true&characterEncoding=utf8', table='judgment_new_v2_v2',properties={"user": "weiwc", "password": "HHly2017."})

    sc.stop()
