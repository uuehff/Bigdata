# -*- coding: utf-8 -*-

from  pyspark import SparkContext,SparkConf
from pyspark.sql import SQLContext
from pyspark.sql.types import *

def split_history(x):
    t = []
    for i in x.split("||"):
        t.append(i)
    return t

def get_36_24(x):
    if len(x[1]) == 36 or len(x[1]) == 24:
        return True
    else:
        return False

def get_not_36_24(x):
    if len(x[1]) < 36 and len(x[1]) > 24:
        return True
    else:
        return False

def reverseMap(x):
    return (x[1][-27:], x[0])

def p(x):
    print type(x)
    print type(x[0]),type(x[1])
    print x[0],x[1]

def get_uuids(uuids):
    l = []
    for x in uuids:
        l.append(x)        #将分组结果ResultIterable转换为List
    return "||".join(l)      #列表不能直接存入Mysql

if __name__ == "__main__":
    conf = SparkConf()
    sc = SparkContext(conf=conf)
    sqlContext = SQLContext(sc)
    # sc.setLogLevel("ERROR")  # ALL, DEBUG, ERROR, FATAL, INFO, OFF, TRACE, WARN
    # df = sqlContext.read.jdbc(url='jdbc:mysql://cdh-slave2:3306/law', table='uuids_lawlist_id_1shen',column='id',lowerBound=0,upperBound=1000,numPartitions=12,properties={"user": "root", "password": "HHly2017."})
    reason_add = sqlContext.read.jdbc(url='jdbc:mysql://cdh-slave1:3306/laws_doc2', table='reason_add',column='id',lowerBound=0,upperBound=20000,numPartitions=1,properties={"user": "root", "password": "root"})
    reason = sqlContext.read.jdbc(url='jdbc:mysql://cdh-slave1:3306/laws_doc', table='reason',column='id',lowerBound=0,upperBound=2000,numPartitions=1,properties={"user": "root", "password": "root"})
    acc = sc.accumulator(0)
    # uuid_history= sqlContext.read.jdbc(url='jdbc:mysql://cdh-slave1:3306/laws_doc2', table='uuid_history',predicates=["id >= 1 and id <= 10"],properties={"user": "root", "password": "root"})
                              # predicates=["id >= 1 and id <= 5", "id > 5 and id <= 10"],
                              # "id > 30000 and id <= 40000", "id > 40000 and id <= 50000",
                              # "id > 50000 and id <= 60000", "id > 60000 and id <= 70000",
                              # "id > 70000 and id <= 80000", "id > 80000 and id <= 90000",
                              # "id > 90000 and id <= 10000", "id > 100000 and id <= 110000",
                              # "id > 110000 and id <= 120000", "id > 120000 and id <= 130000",
                              # "id > 130000 and id <= 140000", "id > 140000 and id <= 150000",
                              # "id > 150000 and id <= 160000"],
                              # properties={"user": "root", "password": "root"})
    def get_new_reason(x):
        x[2].s

    def p(x):
        acc.add(1)
        print type(x)
        print x
        print "---------------------------"

    def filter_tuple(x):
        if x[0] and x[0] != '':
            return True
        return False

    def filter_(x):
        if x and x != '':
            return True
        return False

    c = reason_add.map(lambda x:x[2]).flatMap(lambda x:x.split("||")).map(lambda x:(x,1)).reduceByKey(lambda x,y:x+y).map(lambda x:x[0]).filter(filter_)
    reason2 = reason.map(lambda x:x[5]).filter(filter_)
    c.subtract(reason2).foreach(p)
    print str(acc) + "================================="
    # history_part_ok = c.filter(lambda x:get_36_24(x))
    #
    # d = c.filter(lambda x:get_not_36_24(x)).map(lambda x:reverseMap(x))
    #
    # uuids_result = uuids.map(lambda x:(x[1][-27:], x[1]))
    #
    # result = d.join(uuids_result).map(lambda x:x[1]).union(history_part_ok).groupByKey().mapValues(lambda x:(get_uuids(x)))
    #
    # schema = StructType([StructField("new_reason", StringType(), False),StructField("count_num", IntegerType(), False)])
    # schema = StructType([StructField("new_reason", StringType(), False)])
    # f = sqlContext.createDataFrame(c, schema=schema)
    # # , mode = "overwrite"
    # # useUnicode = true & characterEncoding = utf8，指定写入mysql时的数据编码，否则会乱码。
    # f.write.jdbc(url='jdbc:mysql://cdh-slave1:3306/laws_doc2?useUnicode=true&characterEncoding=utf8', table='reason_c',properties={"user": "root", "password": "root"})

    sc.stop()