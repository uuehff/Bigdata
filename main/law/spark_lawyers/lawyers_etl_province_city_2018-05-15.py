# -*- coding: utf-8 -*-

from  pyspark import SparkContext,SparkConf
from pyspark.sql import SQLContext
from pyspark.sql.types import *
import os
import json

if __name__ == "__main__":
    # if len(sys.argv) > 2:
    #     host = sys.argv[1]
    #     hbase_table_read = sys.argv[2]
    #     hbase_table_save = sys.argv[3]
    # else:
    # host = '192.168.12.35'
    # hbase_table_read = 'laws_doc:judgment'
    # hbase_table_save = 'laws_doc:label'
    # PYSPARK_PYTHON = "C:\\Python27\\python.exe"    #多版本python情况下，需要配置这个变量指定使用哪个版本
    # os.environ["PYSPARK_PYTHON"] = PYSPARK_PYTHON
    conf = SparkConf()
    sc = SparkContext(conf=conf)
    sqlContext = SQLContext(sc)
    # sc.setLogLevel("ERROR")  # ALL, DEBUG, ERROR, FATAL, INFO, OFF, TRACE, WARN '(select id,uuid,plaintiff_info,defendant_info from tmp_lawyers ) tmp'
    lawyers = sqlContext.read.jdbc(url='jdbc:mysql://cdh-slave1:3306/laws_doc_lawyers', table='(select id,law_office from lawyers_full_outer_join ) tmp2',column='id',lowerBound=1,upperBound=715185,numPartitions=16,properties={"user": "root", "password": "root"})
    lawyer_info = sqlContext.read.jdbc(url='jdbc:mysql://cdh-slave1:3306/laws_doc_lawyers', table='(select id,law_office,province,city from law_office_province_city) tmp',column='id',lowerBound=1,upperBound=581262,numPartitions=8,properties={"user": "root", "password": "root"})

    def p(x):
        print type(x)
        print type(x[0]),type(x[1]),type(x[2])
        print x[0],x[1],x[2]

    def get_results(x):
        s = ("","")
        for i in x[1]:
            s = i
            break
        return (x[0],s)

    lawyers_kv = lawyers.map(lambda x:x).map(lambda x:(x[1],x[0]))
    lawyer_info_kv = lawyer_info.map(lambda x: (x[1],(x[2],x[3]))).groupByKey().map(lambda x:get_results(x))

    result = lawyers_kv.join(lawyer_info_kv).map(lambda x:x[1]).map(lambda x:(x[0],x[1][0],x[1][1]))

    schema = StructType([
        StructField("id", IntegerType(), False),
        StructField("province", StringType(), True),
        StructField("city", StringType(), True)
    ])

    f = sqlContext.createDataFrame(result, schema=schema)
    # f.show()
    # , mode = "overwrite"
    # useUnicode = true & characterEncoding = utf8，指定写入mysql时的数据编码，否则会乱码。
    f.write.jdbc(url='jdbc:mysql://cdh-slave1:3306/laws_doc_lawyers?useUnicode=true&characterEncoding=utf8', table='id_province_city',properties={"user": "root", "password": "root"})

    sc.stop()