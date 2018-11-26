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
    lawyers = sqlContext.read.jdbc(url='jdbc:mysql://cdh-slave1:3306/laws_doc_lawyers', table='(select * from lawyers ) tmp2',column='id',lowerBound=1,upperBound=707718,numPartitions=16,properties={"user": "root", "password": "root"})
    lawyer_info = sqlContext.read.jdbc(url='jdbc:mysql://cdh-slave1:3306/laws_doc_lawyers', table='(select * from lawyer_info) tmp',column='id',lowerBound=1,upperBound=305694,numPartitions=8,properties={"user": "root", "password": "root"})
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

    def p(x):
        print type(x)
        print type(x[0]),type(x[1]),type(x[2])
        print x[0],x[1],x[2]
    def p_(x):
        # print type(x)
        print type(x)
        print type(x[0]),type(x[1])
        print x[0],x[1]
    def filter_(x):
        if x[1] and x[1] != '':       #过滤掉数据库中，lawlist为Null或''的行。
            return True
        return False

    def get_ids(ids):
        l = []
        for x in ids:
            l.append(str(x))        #将分组结果ResultIterable转换为List
        return "||".join(l)

    def get_result(x):
        t =  x[0]
        iter = x[1]

        if iter is None:
            id_count.add(1)
            id_count0.add(1)
            return t
        elif t is None:
            id_count1.add(1)
            id_count0.add(1)
            s = [''] * 17
            for i in iter:
              for j in range(0,len(i)):
                  if i[j] and i[j] != "":
                      s[j] = i[j]
            s[0] = 0
            return tuple(s)
        else:
            id_count0.add(1)
            id_count2.add(1)
            s = list(t)
            for i in iter:
                for j in range(0, len(i)):
                    if s[j] is None or s[j] == "":
                        s[j] = i[j]
            return tuple(s)

    def get_results(iter):
        s = []
        c = 707717
        for i in iter:
            l = list(i)
            l[0] = c + 1
            s.append(tuple(l))
            c +=1
        return s

    # c = df.map(lambda x:((x[3],x[1]),x[2])).filter(lambda x:filter_(x[1])).flatMapValues(lambda x:x.split(",")).map(lambda x:(x[1],x[0])).groupByKey().cache()
    #
    # == == == == == == == == == result27468
    # == == == == == == == == == id_count01422902
    # == == == == == == == == == id_count443923
    # == == == == == == == == == id_count17468
    # == == == == == == == == == id_count2263794

    id_count0 = sc.accumulator(707717)  #715185
    id_count = sc.accumulator(0)  #715185
    id_count1 = sc.accumulator(0)  #715185
    id_count2 = sc.accumulator(0)  #715185
    lawyers_kv = lawyers.map(lambda x:x).map(lambda x:(x[1]+"|"+x[2],x))
    lawyer_info_kv = lawyer_info.map(lambda x: x).map(lambda x: (x[1] + "|" + x[2], x)).groupByKey()

    result = lawyers_kv.fullOuterJoin(lawyer_info_kv).map(lambda x:x[1]).map(lambda x:get_result(x)).cache()
    result1 = result.filter(lambda x: False if x[0] == 0 else True)
    result2 = result.filter(lambda x: True if x[0] == 0 else False).map(lambda x:(x[0],x)).groupByKey().flatMap(lambda x:get_results(x[1]))
    result_all = result1.union(result2)

    # print "==================result1" + str(result1.count())
    # print "==================result2" + str(result2.count())
    # print "==================id_count0" + str(id_count0.value)
    # print "==================id_count" + str(id_count.value)
    # print "==================id_count1" + str(id_count1.value)
    # print "==================id_count2" + str(id_count2.value)


    schema = StructType([
        StructField("id", IntegerType(), False),
        StructField("lawyer", StringType(), True),
        StructField("law_office", StringType(), True),
        StructField("char_no", StringType(), True),
        StructField("gender", StringType(), True),
        StructField("province", StringType(), True),
        StructField("city", StringType(), True),
        StructField("nation", StringType(), True),
        StructField("edu", StringType(), True),
        StructField("politics", StringType(), True),
        StructField("org_identity", StringType(), True),
        StructField("birthday", StringType(), True),
        StructField("pra_type", StringType(), True),
        StructField("pra_course", StringType(), True),
        StructField("first_pra_time", StringType(), True),
        StructField("qua_number", StringType(), True),
        StructField("qua_time", StringType(), True)
    ])

    f = sqlContext.createDataFrame(result_all, schema=schema)
    # f.show()
    # , mode = "overwrite"
    # useUnicode = true & characterEncoding = utf8，指定写入mysql时的数据编码，否则会乱码。
    f.write.jdbc(url='jdbc:mysql://cdh-slave1:3306/laws_doc_lawyers?useUnicode=true&characterEncoding=utf8', table='lawyers_full_outer_join',properties={"user": "root", "password": "root"})

    sc.stop()