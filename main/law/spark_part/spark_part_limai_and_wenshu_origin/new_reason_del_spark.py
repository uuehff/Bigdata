# -*- coding: utf-8 -*-

from  pyspark import SparkContext,SparkConf
from pyspark.sql import SQLContext
from pyspark.sql.types import *


def p(x):
    # print type(x)
    print type(x), type(x[0]), type(x[1])
    print x

def filter_(x):
    if x[1] and x[1] != '':  # 过滤掉数据库中，lawlist为Null或''的行。
        return True
    return False

def get_key_value(x):
    key = x[0]
    t = []
    for uid in set(x[1].strip().split("||")):
        t.append((str(key) + "_" + uid[:4], uid))
    return t

def transfer(x):
    t_len = []
    t = []
    for uid in x[1]:
        t_len.append(len(uid))
        t.append(uid)
    uid_max = max(t_len)
    result = []
    for uid in t:
        if len(uid) == uid_max:
            result.append(uid)
    return (x[0].split("_")[0], "||".join(result))

def get_uids(x):
    uids = []
    for i in x:
        uids.append(i)
    return "||".join(uids)

if __name__ == "__main__":

    conf = SparkConf()
    sc = SparkContext(conf=conf)
    sqlContext = SQLContext(sc)
    # sc.setLogLevel("ERROR")  # ALL, DEBUG, ERROR, FATAL, INFO, OFF, TRACE, WARN
    df = sqlContext.read.jdbc(url='jdbc:mysql://cdh-slave1:3306/laws_doc2', table='judgment2_etl',column='id',lowerBound=0,upperBound=2000,numPartitions=22,properties={"user": "root", "password": "root"})
    # df= sqlContext.read.jdbc(url='jdbc:mysql://cdh-slave1:3306/laws_doc2', table='judgment2_etl',
                              # predicates=["id >= 1 and id <= 5"],
                              # "id > 30000 and id <= 40000", "id > 40000 and id <= 50000",
                              # "id > 50000 and id <= 60000", "id > 60000 and id <= 70000",
                              # "id > 70000 and id <= 80000", "id > 80000 and id <= 90000",
                              # "id > 90000 and id <= 10000", "id > 100000 and id <= 110000",
                              # "id > 110000 and id <= 120000", "id > 120000 and id <= 130000",
                              # "id > 130000 and id <= 140000", "id > 140000 and id <= 150000",
                              # "id > 150000 and id <= 160000"],
                              # properties={"user": "root", "password": "root"})


    result = df.select('id','reason_uid').map(lambda x:(x[0],x[1])).filter(filter_).flatMap(lambda x:get_key_value(x)).groupByKey().map(transfer).groupByKey().mapValues(get_uids)

    schema = StructType([StructField("id", StringType(), False),StructField("reason_uid", StringType(), False)])

    f = sqlContext.createDataFrame(result, schema=schema)
    # f.show()
    # , mode = "overwrite"
    # useUnicode = true & characterEncoding = utf8，指定写入mysql时的数据编码，否则会乱码。
    f.write.jdbc(url='jdbc:mysql://cdh-slave1:3306/laws_doc2?useUnicode=true&characterEncoding=utf8', table='reason_uid_distinct_result',properties={"user": "root", "password": "root"})

    sc.stop()