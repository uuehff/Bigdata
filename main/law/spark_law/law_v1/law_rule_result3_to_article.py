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
    df = sqlContext.read.jdbc(url='jdbc:mysql://cdh-slave2:3306/law', table='(select * from law_rule_result3 ) tmp',column='id',lowerBound=1,upperBound=3500000,numPartitions=20,properties={"user": "root", "password": "HHly2017."})
    # df2 = sqlContext.read.jdbc(url='jdbc:mysql://cdh-slave1:3306/laws_doc2', table='(select id,plaintiff_info,defendant_info from tmp_lawyers ) tmp2',column='id',lowerBound=0,upperBound=100000,numPartitions=10,properties={"user": "root", "password": "root"})
    # df= sqlContext.read.jdbc(url='jdbc:mysql://cdh-slave1:3306/laws_doc', table='judgment_etl_lawlist',
                              # predicates=["id >= 2311362 and id <= 2311366", "id > 2311366 and id <= 2311372"],
                              # "id > 30000 and id <= 40000", "id > 40000 and id <= 50000",
                              # "id > 50000 and id <= 60000", "id > 60000 and id <= 70000",
                              # "id > 70000 and id <= 80000", "id > 80000 and id <= 90000",
                              # "id > 90000 and id <= 10000", "id > 100000 and id <= 110000",
                              # "id > 110000 and id <= 120000", "id > 120000 and id <= 130000",
                              # "id > 130000 and id <= 140000", "id > 140000 and id <= 150000",
                              # "id > 150000 and id <= 160000"],
                              # properties={"user": "root", "password": "root"})

    # def p(x):
    #     print type(x)
    #     print type(x[0]),type(x[1]),type(x[2])
    #     print x[0],x[1],x[2]
    # def p_(x):
        # print type(x)
        # print x[0],x[1]
        # for i in x[1]:
        #     print type(i),i
    # def p2(x):
    #     k,v = x[0],x[1]
    #     print k,
    #     # print type(v)
    #     for i2 in v:
    #         print i2,
    #     print "\n"
    def filter_(x):
        if x[0] and x[0] != '' and x[1] and x[1] != '':       #过滤掉数据库中，lawlist为Null或''的行。
            return True
        return False

    def concat(x):
        l = []
        for i in x:
            l.append((int(i[-1]),i[9]))  #(art_digit,art)，art_digit用于法条的排序，1,2，3,4,5.

        l2 = sorted(l, key=lambda e: e[0])    #按art_digit升序，保证法条的顺序
        l3 = []
        for j in l2:
            l3.append(j[1])
        s = "<br/>".join(l3)         #法条之间换行
        return (s,l3[0])    #article,art

    def get_k(x):
        t = []
        for i in range(len(x)-1):  #0~11,第9个为art
            if i == 9: continue    #art字段不要作为key

            if x[i] and x[i] != "":
                if i ==7:
                    t.append(str(x[i]))     #int字段转为str
                    continue
                t.append(x[i])
            else:
                t.append("null")
        s = "||".join(t)
        return s

    def get_results(x):
        t = []
        for i in x[0].split("||"):
            if i == "null":
                t.append(None)
                continue
            t.append(i)
        t.append(x[1][0])
        t.append(x[1][1])
        return t


    results = df.map(lambda x:x[1:]).groupBy(lambda x:get_k(x)).mapValues(lambda x: concat(x)).map(lambda x:get_results(x))

    schema = StructType([StructField("law_id", StringType(), False),
                         StructField("cate_a", StringType(), True),
                         StructField("cate_b", StringType(), True),
                         StructField("department", StringType(), True),
                         StructField("publish_date", StringType(), True),
                         StructField("effective_date", StringType(), True),
                         StructField("effective_range", StringType(), True),
                         StructField("effective_status", StringType(), True),
                         StructField("title_short", StringType(), True),
                         StructField("area", StringType(), True),
                         StructField("doc_num", StringType(), True),
                         StructField("article", StringType(), True),
                         StructField("art", StringType(), True)])

    f = sqlContext.createDataFrame(results, schema=schema)
    # , mode = "overwrite"
    # useUnicode = true & characterEncoding = utf8，指定写入mysql时的数据编码，否则会乱码。
    f.write.jdbc(url='jdbc:mysql://cdh-slave2:3306/law?useUnicode=true&characterEncoding=utf8', table='law_rule_result4',properties={"user": "root", "password": "HHly2017."})

    sc.stop()