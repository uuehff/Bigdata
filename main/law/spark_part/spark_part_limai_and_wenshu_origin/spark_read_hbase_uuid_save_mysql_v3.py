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

    host = 'cdh5-master-slave1,cdh5-slave2,cdh5-slave3'
    # hbase_table = 'laws_doc:judgment_administration_all'
    # hbase_table = 'laws_doc:judgment_implement_all'
    # hbase_table = 'laws_doc:judgment_all'
    hbase_table = 'laws_doc:judgment_civil_all_v2'
    rkeyConv = "hbase.pythonconverters.ImmutableBytesWritableToStringConverter"
    rvalueConv = "hbase.pythonconverters.HBaseResultToStringConverter"
    rconf = {"hbase.zookeeper.quorum": host, "hbase.mapreduce.inputtable": hbase_table,
             "hbase.mapreduce.scan.columns":"d:uuid_old"
             #uuid_old字段每行都存在时，才相当于是统计表的行数
             # "hbase.mapreduce.scan.row.stop":"0013a32561b3357d8836650771f8e232"
             }
    ps_data = sc.newAPIHadoopRDD(
        "org.apache.hadoop.hbase.mapreduce.TableInputFormat",
        "org.apache.hadoop.hbase.io.ImmutableBytesWritable",
        "org.apache.hadoop.hbase.client.Result",
        keyConverter=rkeyConv,
        valueConverter=rvalueConv,
        conf=rconf
    )

    ps_data1 = ps_data.repartition(66).map(lambda v: (None,v[0],json.loads(v[1])['value']))
    # ps_data1 = ps_data.flatMapValues(lambda v: v.split("\n")).mapValues(json.loads).cache()
    # print ps_data.take(100)
    # print ps_data1.take(100)
    # print ps_data1.count()
    # def p(x):
    #     print type(x)
    #     print x
    # ps_data1.foreach(p)

    schema = StructType([
        StructField("id", StringType(), False),
        StructField("uuid", StringType(), False),
        StructField("uuid_old", StringType(), False)
                         ])
    # #
    f = sqlContext.createDataFrame(ps_data1, schema=schema)

    # f.show()
    # , mode = "overwrite"
    # d = result.collect()
    # useUnicode = true & characterEncoding = utf8，指定写入mysql时的数据编码，否则会乱码。
    f.write.jdbc(url='jdbc:mysql://cdh5-slave2:3306/docs_count?useUnicode=true&characterEncoding=utf8', table='civil_v2',properties={"user": "weiwc", "password": "HHly2017."})

    sc.stop()