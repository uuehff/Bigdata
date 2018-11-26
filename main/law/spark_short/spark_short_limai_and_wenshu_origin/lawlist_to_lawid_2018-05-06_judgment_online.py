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
    l = []
    # title_short_num = []
    lawlist_id = []
    for x in ids:
        al = x.decode("utf-8").split("_")  # 写入Mysql的数据必须是unicode编码，str需解码
        # title_short_num.append(al[0])
        lawlist_id.append(al[1])
    return (uuid,"||".join(lawlist_id))

def get_title_short_id(x):              #保证lawlist和law_id的有序！
    k = x[0].encode("utf-8") + "|" + x[1].encode("utf-8")
    v = k + "_" + str(x[2])
    return (k,v)

if __name__ == "__main__":

    conf = SparkConf()
    sc = SparkContext(conf=conf)
    sqlContext = SQLContext(sc)
    # sc.setLogLevel("ERROR")  # ALL, DEBUG, ERROR, FATAL, INFO, OFF, TRACE, WARN
    # lawlist = sqlContext.read.jdbc(url='jdbc:mysql://cdh-slave1:3306/civil', table='uuid_reason_lawlist',column='id',lowerBound=0,upperBound=100000,numPartitions=70,properties={"user": "root", "password": "HHly2017."})
    lawlist_id = sqlContext.read.jdbc(url='jdbc:mysql://cdh-slave1:3306/civil', table='(select id,lawlist_id from law_rule_result2_error_flag) tmp',column='id',lowerBound=170,upperBound=2880280,numPartitions=1,properties={"user": "root", "password": "HHly2017."})
    # lawlist= sqlContext.read.jdbc(url='jdbc:mysql://cdh-slave1:3306/civil', table='uuid_reason_lawlist',predicates=["id >= 1 and id <= 100"],properties={"user": "root", "password": "HHly2017."})
    lawlist= sqlContext.read.jdbc(url='jdbc:mysql://cdh-slave1:3306/civil', table='(select id,uuid,law_id from judgment_civil_all) tmp2',column='id',lowerBound=1,upperBound=11295123,numPartitions=108,properties={"user": "root", "password": "HHly2017."})


    def error_del(x):
        if x[1] and x[1] !="":
            t = []
            for i in x[1].split("||"):
                if i in error_law_broadcast.value:
                    continue
                t.append(i)
            return (x[0],"||".join(t))
        return (x[0],"")
    error_law_broadcast = sc.broadcast(lawlist_id.map(lambda x:x[1]).collect())
    # p1 = ur'\u7b2c[\u4e00\u4e8c\u4e09\u56db\u4e94\u516d\u4e03\u516b\u4e5d\u5341\u767e\u5343]{1,10}\u6761'
    # p2 = ur'[\u300a\u300b]'  # 按《》切分
    c = lawlist.select('uuid','law_id').map(lambda x:error_del(x))
    # flatMapValues(lambda x: etl_lawlist(p1, p2, x)).filter(filter_).map(lambda x: (x[1].encode("utf-8"), x[0]))
        # groupByKey().mapValues(lambda v: get_uuids(v))
    # filter(filter_).map(lambda x: (x[1].encode("utf-8"), x[0])).groupByKey().mapValues(lambda v: get_uuids(v))
    # print str(c.count()) + "======================"
    # c.foreach(p)

    # lawlist_title_id_result = lawlist_id2.join(c).map(lambda x:x[1]).flatMapValues(lambda x:(x.split("||"))).map(lambda x:(x[1],x[0])).groupByKey().map(lambda x:(get_lawlist_ids(x)))

    schema = StructType([StructField("uuid", StringType(), False),StructField("law_id", StringType(), True)])

    f = sqlContext.createDataFrame(c, schema=schema)
    # , mode = "overwrite"
    # useUnicode = true & characterEncoding = utf8，指定写入mysql时的数据编码，否则会乱码。
    # print str(f.count()) + "======================"
    f.write.jdbc(url='jdbc:mysql://cdh-slave1:3306/civil?useUnicode=true&characterEncoding=utf8', table='law_id_civil_0001',properties={"user": "root", "password": "HHly2017."})

    sc.stop()