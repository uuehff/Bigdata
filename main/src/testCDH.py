# -*- coding: utf-8 -*-

import json
from  pyspark import SparkContext
from pyspark.sql import SQLContext

sc = SparkContext()
sc.setLogLevel("ERROR")  # ALL, DEBUG, ERROR, FATAL, INFO, OFF, TRACE, WARN


# 用Spark取：

# hbase_rdd2 = hbase_rdd.flatMapValues(lambda v: v.split("\n"))
# tt=sqlContext.jsonRDD(hbase_rdd2.values())
# tt.take(1)
# tt.take(2)
# tt.printSchema()


host = 'cdh-slave1'
hbase_table = 't'
rkeyConv = "hbase.pythonconverters.ImmutableBytesWritableToStringConverter"
rvalueConv = "hbase.pythonconverters.HBaseResultToStringConverter"

rconf = {"hbase.zookeeper.quorum": host,"hbase.mapreduce.inputtable": hbase_table}
ps_data = sc.newAPIHadoopRDD(
    "org.apache.hadoop.hbase.mapreduce.TableInputFormat",
    "org.apache.hadoop.hbase.io.ImmutableBytesWritable",
    "org.apache.hadoop.hbase.client.Result",
    keyConverter=rkeyConv,
    valueConverter=rvalueConv,
    conf=rconf
)
ps_data1 = ps_data.flatMapValues(lambda v: v.split("\n")).mapValues(json.loads).cache()
ps_data1.saveAsTextFile("hdfs://cdh-master:8020/cdh/data/out")

sc.stop()