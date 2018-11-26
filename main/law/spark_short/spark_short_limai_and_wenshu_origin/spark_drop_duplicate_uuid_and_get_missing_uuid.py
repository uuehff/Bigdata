# -*- coding: utf-8 -*-

from  pyspark import SparkContext,SparkConf
from pyspark.sql import SQLContext
from pyspark.sql.types import *

import re


if __name__ == "__main__":

    conf = SparkConf()
    sc = SparkContext(conf=conf)
    sqlContext = SQLContext(sc)
    # sc.setLogLevel("ERROR")  # ALL, DEBUG, ERROR, FATAL, INFO, OFF, TRACE, WARN
    # lawlist = sqlContext.read.jdbc(url='jdbc:mysql://cdh-slave1:3306/civil', table='uuid_reason_lawlist',column='id',lowerBound=0,upperBound=100000,numPartitions=70,properties={"user": "root", "password": "HHly2017."})
    all_uuid = sqlContext.read.jdbc(url='jdbc:mysql://192.168.74.113:3306/wenshu_gov', table='(select id,uuid from all_uuid) tmp',column='id',lowerBound=1,upperBound=46593620,numPartitions=47,properties={"user": "root", "password": "hhly419"})
    # lawlist= sqlContext.read.jdbc(url='jdbc:mysql://cdh-slave1:3306/civil', table='uuid_reason_lawlist',predicates=["id >= 1 and id <= 100"],properties={"user": "root", "password": "HHly2017."})
    hbase_uuid= sqlContext.read.jdbc(url='jdbc:mysql://192.168.74.113:3306/wenshu_gov', table='(select id,uuid_old from hbase_uuid_old04 ) tmp2',column='id',lowerBound=1,upperBound=47915950,numPartitions=52,properties={"user": "root", "password": "hhly419"})

    hbase_uuid_tmp = hbase_uuid.select('uuid_old').distinct()
    miss_uuid = all_uuid.select('uuid').subtract(hbase_uuid_tmp).map(lambda x:(None,x[0]))

    schema = StructType([StructField("id", StringType(), False),StructField("uuid", StringType(), False)])

    f = sqlContext.createDataFrame(miss_uuid, schema=schema)
    # , mode = "overwrite"
    # useUnicode = true & characterEncoding = utf8，指定写入mysql时的数据编码，否则会乱码。
    # print str(f.count()) + "======================"
    f.write.jdbc(url='jdbc:mysql://192.168.74.113:3306/wenshu_gov?useUnicode=true&characterEncoding=utf8', table='uuid_missing',properties={"user": "root", "password": "hhly419"})

    sc.stop()