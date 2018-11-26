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
    PYSPARK_PYTHON = "C:\\Python27\\python.exe"    #多版本python情况下，需要配置这个变量指定使用哪个版本
    os.environ["PYSPARK_PYTHON"] = PYSPARK_PYTHON
    conf = SparkConf()
    sc = SparkContext(conf=conf)
    sqlContext = SQLContext(sc)
    # sc.setLogLevel("ERROR")  # ALL, DEBUG, ERROR, FATAL, INFO, OFF, TRACE, WARN '(select id,uuid,plaintiff_info,defendant_info from tmp_lawyers ) tmp'
    df = sqlContext.read.jdbc(url='jdbc:mysql://cdh5-slave2:3306/laws_doc_lawyers_new', table='(select lawyer_id,name,org_names,id from hht_lawyer_all_collect_match_result ) tmp',column='id',lowerBound=1,upperBound=360861,numPartitions=5,properties={"user": "weiwc", "password": "HHly2017."})


    def get_results(x):
        lawyer_ids = []
        for i in x[1]:
            lawyer_ids.append(i)
        return (x[0].split("||")[0],x[0].split("||")[1],"||".join(lawyer_ids))


    def get_key(x):
        return (x[0].split("||")[1] + "||" + x[1], x[0].split("||")[0])
    results = df.map(lambda x:(x[0]+ "||" + x[1],x[2])).flatMapValues(lambda x:x.split("||")).map(lambda x:get_key(x)).groupByKey().map(lambda x: get_results(x))

    # print "+++++++++++++++++++++" + str(results.count())
    # results.foreach(p2)
    schema = StructType([
        StructField("name", StringType(), False),
        StructField("org_name", StringType(), False),
        StructField("lawyer_ids", StringType(), False)
    ])

    f = sqlContext.createDataFrame(results, schema=schema)
    # , mode = "overwrite"
    # useUnicode = true & characterEncoding = utf8，指定写入mysql时的数据编码，否则会乱码。
    f.write.jdbc(url='jdbc:mysql://cdh5-slave2:3306/laws_doc_lawyers_new?useUnicode=true&characterEncoding=utf8', table='hht_lawyer_v2_name_org_name_lawyer_ids',properties={"user": "weiwc", "password": "HHly2017."})

    sc.stop()