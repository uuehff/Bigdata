# -*- coding: utf-8 -*-

from  pyspark import SparkContext
from pyspark.sql import SQLContext

sc = SparkContext("local","t6")
sc.setLogLevel("ERROR")  # ALL, DEBUG, ERROR, FATAL, INFO, OFF, TRACE, WARN


# 用Spark取：

# hbase_rdd2 = hbase_rdd.flatMapValues(lambda v: v.split("\n"))
# tt=sqlContext.jsonRDD(hbase_rdd2.values())
# tt.take(1)
# tt.take(2)
# tt.printSchema()


# host = '192.168.10.24'
# hbase_table = 't5'
# rkeyConv = "hbase.pythonconverters.ImmutableBytesWritableToStringConverter"
# rvalueConv = "hbase.pythonconverters.HBaseResultToStringConverter"

# conf参数配置:
# http://www.myexception.cn/other/1915134.html
# https://github.com/apache/hbase/blob/master/hbase-server/src/main/java/org/apache/hadoop/hbase/mapreduce/TableInputFormat.java

# rconf = {"hbase.zookeeper.quorum": host,"hbase.mapreduce.inputtable": hbase_table}
# ps_data = sc.newAPIHadoopRDD(
#     "org.apache.hadoop.hbase.mapreduce.TableInputFormat",
#     "org.apache.hadoop.hbase.io.ImmutableBytesWritable",
#     "org.apache.hadoop.hbase.client.Result",
#     keyConverter=rkeyConv,
#     valueConverter=rvalueConv,
#     conf=rconf
# )
# ps_data1 = ps_data.flatMapValues(lambda v: v.split("\n")).mapValues(json.loads).cache()
# ps_data1.take(5)
# ps_data1 = ps_data.map(lambda x:(x[1]))

# 用spark存

# sqlContext = SQLContext(sc)
host = '192.168.10.24'
hbase_table = 't6'
conf = {"hbase.zookeeper.quorum": host,
        "hbase.mapred.outputtable": hbase_table,
        "mapreduce.outputformat.class": "org.apache.hadoop.hbase.mapreduce.TableOutputFormat",
        "mapreduce.job.output.key.class": "org.apache.hadoop.hbase.io.ImmutableBytesWritable",
        "mapreduce.job.output.value.class": "org.apache.hadoop.io.Writable"}
keyConv = "hbase.pythonconverters.StringToImmutableBytesWritableConverter"
valueConv = "hbase.pythonconverters.StringListToPutConverter"
import time
#id,name,salary
def split_(x):
    # t = str(time.time())
    s = x.split("\t")
    c = ['id','name','salary']
    d = 0
    l_ = []
    for v in s:
        l_.append((s[0],[s[0],'info',c[d],v]))
        d += 1
    return l_       #此处不能使用yield，否则不能flatMap,压扁

rdd_ = sc.textFile("hdfs://cdh-master-slave1:8020/user/weiwc/data/hive/employees.txt").flatMap(split_).cache()
# rdd2 = rdd_.rdd.coalesce(3).flatMap(lambda row : transform_comment_content(row,'02')).map(lambda x: (x[0], x)).cache()
rdd_.saveAsNewAPIHadoopDataset(conf=conf,keyConverter=keyConv,valueConverter=valueConv)

sc.stop()