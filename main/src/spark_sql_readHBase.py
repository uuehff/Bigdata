# -*- coding: utf-8 -*-
# sparkSql读取Mysql，分区理解： ：http://dataunion.org/21528.html

from pyspark import SparkContext,SparkConf,SQLContext

import json

if __name__ == "__main__":
    # if len(sys.argv) > 2:
    #     host = sys.argv[1]
    #     hbase_table_read = sys.argv[2]
    #     hbase_table_save = sys.argv[3]
    # else:
    host = '192.168.12.34'
    hbase_table_read = 'laws_doc:judgment'
    hbase_table_save = 'laws_doc:label'

    conf = SparkConf()
    sc = SparkContext(conf=conf)
    sqlContext = SQLContext(sc)
    # sc.setLogLevel("ERROR")  # ALL, DEBUG, ERROR, FATAL, INFO, OFF, TRACE, WARN

    rkeyConv = "hbase.pythonconverters.ImmutableBytesWritableToStringConverter"
    rvalueConv = "hbase.pythonconverters.HBaseResultToStringConverter"
    rconf = {"hbase.zookeeper.quorum": host,"hbase.mapreduce.inputtable": hbase_table_read,
             "hbase.mapreduce.scan.row.start":"1","hbase.mapreduce.scan.row.start":"1000",
             "hbase.mapreduce.scan.column.family":"d","hbase.mapreduce.scan.columns":"uuid,lawlist"}
    ps_data = sc.newAPIHadoopRDD(
        "org.apache.hadoop.hbase.mapreduce.TableInputFormat",
        "org.apache.hadoop.hbase.io.ImmutableBytesWritable",
        "org.apache.hadoop.hbase.client.Result",
        keyConverter=rkeyConv,
        valueConverter=rvalueConv,
        conf=rconf
    )
    # df.map(lambda x : format_html_to_line(x)).map(lambda x: get_X(x)).flatMap(lambda x : save_result_to_hbase(x)).foreach(lambda x:p(x))
    df = ps_data.flatMapValues(lambda v: v.split("\n")).mapValues(json.loads)
    print  df.take(5)
    # ps_data1 = ps_data.map(lambda x:(x[1]))
    # df = sqlContext.read.jdbc(url='jdbc:mysql://cdh-slave2:3306/laws_doc', table='judgment',
    #                           predicates=["id > 10000 and id <= 20000", "id > 20000 and id <= 30000",
    #                                       "id > 30000 and id <= 40000", "id > 40000 and id <= 50000",
    #                                       "id > 50000 and id <= 60000", "id > 60000 and id <= 70000",
    #                                       "id > 70000 and id <= 80000", "id > 80000 and id <= 90000",
    #                                       "id > 90000 and id <= 10000", "id > 100000 and id <= 110000",
    #                                       "id > 110000 and id <= 120000", "id > 120000 and id <= 130000",
    #                                       "id > 130000 and id <= 140000", "id > 140000 and id <= 150000",
    #                                       "id > 150000 and id <= 160000"],
    #                           properties={"user": "root", "password": "root"})

    # df = sqlContext.read.jdbc(url='jdbc:mysql://cdh-slave2:3306/laws_doc', table='judgment',predicates=["id <= 10000","id > 10000 and id <= 20000","id > 20000 and id <= 30000","id > 30000 and id <= 40000","id > 40000 and id <= 50000","id > 50000 and id <= 60000","id > 60000 and id <= 70000","id > 70000 and id <= 80000","id > 80000 and id <= 90000","id > 90000 and id <= 10000"],properties={"user":"root","password":"root"})
    # df = sqlContext.read.jdbc(url='jdbc:mysql://cdh-slave2:3306/laws_doc', table='judgment',predicates=["id <= 10000","id > 10000 and id <= 20000","id > 20000 and id <= 30000","id > 30000 and id <= 40000","id > 40000 and id <= 50000","id > 50000 and id <= 60000","id > 60000 and id <= 70000","id > 70000 and id <= 80000","id > 80000 and id <= 90000","id > 90000 and id <= 100000"],properties={"user":"root","password":"root"})
    # df = sqlContext.read.jdbc(url='jdbc:mysql://cdh-slave2:3306/laws_doc', table='judgment',predicates=["id <= 2","id > 2 and id <=4","id > 4 and id <=6","id > 6 and id <=8","id > 8 and id <=10","id > 10 and id <=12","id > 12 and id <=14"],properties={"user":"root","password":"root"})
    # df = sqlContext.read.jdbc(url='jdbc:mysql://cdh-slave2:3306/laws_doc', table='judgment',predicates=["id <= 1","id > 1 and id <=2"],properties={"user":"root","password":"root"})

    # df.map(lambda x : format_html_to_line(x)).map(lambda x: get_X(x)).flatMap(lambda x : save_result_to_hbase(x)).foreach(lambda x:p(x))
    # df.map(lambda x : format_html_to_line(x)).map(lambda x: get_X(x)).foreach(lambda x :p(x))
    # df.map(lambda x : format_html_to_line(x)).foreach(lambda x :p(x))
        # .\
        # foreachPartition(lambda x : data.write_result_to_file(x))
    # conf = {"hbase.zookeeper.quorum": host,
    #         "hbase.mapred.outputtable": hbase_table_save,
    #         "mapreduce.outputformat.class": "org.apache.hadoop.hbase.mapreduce.TableOutputFormat",
    #         "mapreduce.job.output.key.class": "org.apache.hadoop.hbase.io.ImmutableBytesWritable",
    #         "mapreduce.job.output.value.class": "org.apache.hadoop.io.Writable"}
    # keyConv = "hbase.pythonconverters.StringToImmutableBytesWritableConverter"
    # valueConv = "hbase.pythonconverters.StringListToPutConverter"
    #
    # df.map(lambda x: format_html_to_line(x)).map(lambda x: get_X(x)).flatMap(lambda x: save_result_to_hbase(x)).\
    #     saveAsNewAPIHadoopDataset(conf=conf, keyConverter=keyConv, valueConverter=valueConv)

    sc.stop()