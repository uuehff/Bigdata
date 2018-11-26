# -*- coding: utf-8 -*-

from  pyspark import SparkContext,SparkConf
from pyspark.sql import SQLContext
from pyspark.sql.types import *

import re

def p(x):
    if x[1]:
        print type(x)
        print x
        # print x[1]
        # exit(0)
def filter_(x):
    if x[1] and x[1] != '':       #过滤掉数据库中，lawlist为Null或''的行。
        return True
    return False

def get_uuids(uuids):
    l = []
    for x in uuids:
        l.append(x)
        #将分组结果ResultIterable转换为List
    return "||".join(l)      #列表不能直接存入Mysql


if __name__ == "__main__":

    conf = SparkConf()
    sc = SparkContext(conf=conf)
    sqlContext = SQLContext(sc)
    # sc.setLogLevel("ERROR")  # ALL, DEBUG, ERROR, FATAL, INFO, OFF, TRACE, WARN
    # uuid_type_history_title = sqlContext.read.jdbc(url='jdbc:mysql://cdh-slave1:3306/civil', table='uuid_reason_lawlist',column='id',lowerBound=0,upperBound=100000,numPartitions=70,properties={"user": "root", "password": "HHly2017."})
    # uuid_history= sqlContext.read.jdbc(url='jdbc:mysql://cdh-slave1:3306/civil', table='uuid_court_history',column='id',lowerBound=490000,upperBound=500000,numPartitions=14,properties={"user": "root", "password": "HHly2017."})
    # uuid_history= sqlContext.read.jdbc(url='jdbc:mysql://cdh-slave1:3306/civil', table='uuid_court_history',predicates=["id >= 1 and id <= 100"],properties={"user": "root", "password": "HHly2017."})
    # lawlist= sqlContext.read.jdbc(url='jdbc:mysql://cdh-slave1:3306/civil', table='uuid_reason_lawlist',
    #                           predicates=["id <= 500000", "id > 500000 and id <= 1000000",
    #                           "id > 1000000 and id <= 1500000", "id > 1500000 and id <= 2000000",
    #                           "id > 2000000 and id <= 2500000", "id > 2500000 and id <= 3000000",
    #                           "id > 3000000 and id <= 3500000", "id > 3500000 and id <= 4000000",
    #                           "id > 4000000 and id <= 4500000", "id > 4500000 and id <= 5000000",
    #                           "id > 5000000 and id <= 5500000", "id > 5500000 and id <= 6000000",
    #                           "id > 6000000 and id <= 6500000", "id > 6500000 "],
    #                           properties={"user": "root", "password": "HHly2017."})

    # schema = StructType([StructField("uuid", StringType(), False),StructField("history", StringType(), False),StructField("title", StringType(), False)])
    # f = sqlContext.createDataFrame(history_title_results, schema=schema)
    # , mode = "overwrite"
    # useUnicode = true & characterEncoding = utf8，指定写入mysql时的数据编码，否则会乱码。
    # print str(f.count()) + "======================"
    # f.write.jdbc(url='jdbc:mysql://cdh-slave1:3306/civil?useUnicode=true&characterEncoding=utf8', table='judgment_etl_uuid_history_title_result',properties={"user": "root", "password": "HHly2017."})

    df = sqlContext.read.jdbc(url='jdbc:mysql://cdh-slave2:3306/civil', table='(select id,uuid from tmp_wxy where id <= 50) tmp',column='id',lowerBound=0,upperBound=50,numPartitions=3,properties={"user": "root", "password": "HHly2017."})

    # print df.count()
    print df.filter("id < 30").count()
    sc.stop()