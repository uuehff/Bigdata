# -*- coding: utf-8 -*-

from  pyspark import SparkContext,SparkConf
from pyspark.sql import SQLContext
from pyspark.sql.types import *

if __name__ == "__main__":
    # if len(sys.argv) > 2:
    #     host = sys.argv[1]
    #     hbase_table_read = sys.argv[2]
    #     hbase_table_save = sys.argv[3]
    # else:
    # host = '192.168.12.35'
    # hbase_table_read = 'laws_doc:judgment'
    # hbase_table_save = 'laws_doc:label'

    conf = SparkConf()
    sc = SparkContext(conf=conf)
    sqlContext = SQLContext(sc)
    # sc.setLogLevel("ERROR")  # ALL, DEBUG, ERROR, FATAL, INFO, OFF, TRACE, WARN
    df = sqlContext.read.jdbc(url='jdbc:mysql://cdh-slave1:3306/laws_doc2', table='judgment2_etl_lawlist',column='id',lowerBound=0,upperBound=50000,numPartitions=10,properties={"user": "root", "password": "root"})
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
    #     # print type(x)
    #     print type(x)
        # print type(x[0]),type(x[1]),type(x[2])
    # def p2(x):
    #     k,v = x[0],x[1]
    #     print k,
    #     # print type(v)
    #     for i2 in v:
    #         print i2,
    #     print "\n"
    def filter_(x):
        if x and x != '':       #过滤掉数据库中，lawlist为Null或''的行。
            return True
        return False


    def sort_(v):
        l = []
        for x in v:
            l.append(x)        #将分组结果ResultIterable转换为List
        sl = []
        c = 0
        for i in sorted(l,key=lambda t: t[0],reverse=True):     # 按时间排序，降序指定reverse=True,如果casedate在mysql中为''或Null时,则认为时间最小，排序时相当于00-00-00
            sl.append(i[1])         #去掉casedate字段
            c += 1
        return ("||".join(sl) ,c)        #列表不能直接存入Mysql

        # student_tuples = [
        #     ('john', 'A', 15),
        #     ('jane', 'B', 12),
        #     ('dave', 'B', 10),
        # ]
        # >> > sorted(student_tuples, key=lambda student: student[2])  # sort by age
        # [('dave', 'B', 10), ('jane', 'B', 12), ('john', 'A', 15)]

    # x[3],x[1]),x[2] => casedate,uuid,lawlist
    c = df.map(lambda x:((x[3],x[1]),x[2])).filter(lambda x:filter_(x[1])).flatMapValues(lambda x:x.split(",")).map(lambda x:(x[1],x[0])).groupByKey().cache()

    d = c.mapValues(lambda v:sort_(v)).cache()

    # 经统计x[0].split("|")，分割后有等于1的法律发条，此为无效，否则x[0].split("|")[1]报错数组越界！
    def filterLength(x):
        t = x[0].split("|")
        if len(t) == 2:
            return True
        return False

    e = d.filter(lambda x:(filterLength(x))).map(lambda x:(x[0].split("|")[0],x[0].split("|")[1],x[1][0],x[1][1]))

    schema = StructType([StructField("title_short", StringType(), False),StructField("art_num", StringType(), False),StructField("uuids", StringType(), True),StructField("uuids_len", IntegerType(), True)])

    f = sqlContext.createDataFrame(e, schema=schema)

    # , mode = "overwrite"
    # useUnicode = true & characterEncoding = utf8，指定写入mysql时的数据编码，否则会乱码。
    f.write.jdbc(url='jdbc:mysql://cdh-slave2:3306/law?useUnicode=true&characterEncoding=utf8', table='lawlist_uuids_2shen_all',properties={"user": "root", "password": "HHly2017."})

    sc.stop()