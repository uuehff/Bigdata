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
        l.append(x)        #将分组结果ResultIterable转换为List
    return "||".join(l)      #列表不能直接存入Mysql

def get_lawlist_ids(uuid_ids):
    uuid,ids = uuid_ids[0],uuid_ids[1]
    lawlist_id = []
    for x in ids:
        lawlist_id.append(x)
    return (uuid,"||".join(lawlist_id))

def get_title_short_id(x):              #保证lawlist和law_id的有序！
    k = x[0] + "|" + x[1]
    v = str(x[2])
    return (k,v)

if __name__ == "__main__":

    conf = SparkConf()
    sc = SparkContext(conf=conf)
    sqlContext = SQLContext(sc)
    # sc.setLogLevel("ERROR")  # ALL, DEBUG, ERROR, FATAL, INFO, OFF, TRACE, WARN
    # lawlist = sqlContext.read.jdbc(url='jdbc:mysql://cdh-slave1:3306/civil', table='uuid_reason_lawlist',column='id',lowerBound=0,upperBound=100000,numPartitions=70,properties={"user": "root", "password": "HHly2017."})
    lawlist_id = sqlContext.read.jdbc(url='jdbc:mysql://cdh5-slave3:3306/laws_doc_civil', table='(select * from civil_other_fields_v2_800w_01) tmp',column='id',lowerBound=1,upperBound=7997816,numPartitions=69,properties={"user": "weiwc", "password": "HHly2017."})
    # lawlist= sqlContext.read.jdbc(url='jdbc:mysql://cdh-slave1:3306/civil', table='uuid_reason_lawlist',predicates=["id >= 1 and id <= 100"],properties={"user": "root", "password": "HHly2017."})
    uuid_uuid= sqlContext.read.jdbc(url='jdbc:mysql://cdh5-slave3:3306/laws_doc_civil', table='(select id,uuid,uuid_ from civil_etl_v2_800w_01 ) tmp2',column='id',lowerBound=1,upperBound=8000000,numPartitions=30,properties={"user": "weiwc", "password": "HHly2017."})


    a = uuid_uuid.map(lambda x:(x[1],x[2]))  #uuid,uuid_

    # id,    uuid,    reason,    reason_uid,    casedate,    province,    court_uid

    b = lawlist_id.map(lambda x:(x[1],x))

    result = a.join(b).map(lambda x:x[1]).map(lambda x:(x[1][0],x[0],x[1][2],x[1][3],x[1][4],x[1][5],x[1][6]))

    schema = StructType([
        StructField("id", StringType(), False),
        StructField("uuid", StringType(), False),
        StructField("reason", StringType(), True),
        StructField("reason_uid", StringType(), True),
        StructField("casedate", StringType(), True),
        StructField("province", StringType(), True),
        StructField("court_uid", StringType(), True)

    ])

    f = sqlContext.createDataFrame(result, schema=schema)
    # , mode = "overwrite"
    # useUnicode = true & characterEncoding = utf8，指定写入mysql时的数据编码，否则会乱码。
    # print str(f.count()) + "======================"
    f.write.jdbc(url='jdbc:mysql://cdh5-slave3:3306/laws_doc_civil?useUnicode=true&characterEncoding=utf8', table='civil_other_fields_v2_800w_01_result',properties={"user": "weiwc", "password": "HHly2017."})

    sc.stop()