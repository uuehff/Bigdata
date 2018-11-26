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
    #
    df = sqlContext.read.jdbc(url='jdbc:mysql://cdh-slave2:3306/law', table='(select id,lawlist_id from law_rule_result2 where art_digit is not null) tmp',column='id',lowerBound=0,upperBound=2800000,numPartitions=10,properties={"user": "root", "password": "HHly2017."})
    df2 = sqlContext.read.jdbc(url='jdbc:mysql://cdh-slave1:3306/laws_doc2', table='(select id,uuid,law_id from judgment2_main_etl ) tmp2',column='id',lowerBound=0,upperBound=100000,numPartitions=1,properties={"user": "root", "password": "root"})
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
    #     # print type(x)
    #     print type(x)
    #     print type(x[0]),type(x[1])
    #     print x[0],x[1]

    def trans(x):
        plain = []
        if x and x != "":
            for i in x.split("||"):
                plain.append(i)
        return plain

    def get_ids(ids):
        l = []
        for x in ids:
            l.append(x)  # 将分组结果ResultIterable转换为List
        return "||".join(l)

    # def get_new_name(new_names):
    #     l = []
    #     for x in new_names:
    #         l.append(x)  # 将分组结果ResultIterable转换为List
    #     return "||".join(l)

    lawyer_k_v = df.map(lambda x:(str(x[0]),x[1]))  #id,lawlist_id
    # lawyer_k_v.foreach(p_)
    tr = df2.map(lambda x:(x[1],x[2])).flatMapValues(lambda x:trans(x)).map(lambda x:(x[1],x[0])).\
        groupByKey().mapValues(lambda v:get_ids(v))    #（lawid,uuids），需要将id的类型int转为str，才可以join，连接。

    results = lawyer_k_v.join(tr).map(lambda x:x[1]).flatMapValues(lambda x:x.split("||")).\
        map(lambda x:(x[1],x[0])).groupByKey().mapValues(lambda x:get_ids(x))



    #注意：这里加不加filter(filter_)过滤函数都一样，flatMapValues对value为[]进行展开时，不会返回包含该[]对应key任何记录。
    # s1 = tr.map(lambda x:(x[0],x[1])).flatMapValues(lambda x:x).filter(filter_).map(lambda x:(x[1],x[0])).groupByKey().mapValues(lambda v:get_ids(v))  # (plaintiff_info,id)
    # s1.foreach(p_)

    # s2 = tr.map(lambda x:(x[0],x[2])).flatMapValues(lambda x:x).filter(filter_).map(lambda x:(x[1],x[0])).groupByKey().mapValues(lambda v:get_ids(v))  #（defendant_info,id）
    # s2.foreach(p_)
    # result_s1 = lawyer_k_v.join(s1).map(lambda x:x[1]).flatMapValues(lambda x:(x.split("||"))).map(lambda x:(x[1],x[0])).groupByKey().mapValues(lambda x:(get_new_name(x)))
    # result_s1.foreach(p_)
    # result_s2 = lawyer_k_v.join(s2).map(lambda x:x[1]).flatMapValues(lambda x:(x.split("||"))).map(lambda x:(x[1],x[0])).groupByKey().mapValues(lambda x:(get_new_name(x)))
    # result_s2.foreach(p_)
    # all_result = result_s1.fullOuterJoin(result_s2).map(lambda x:(int(x[0]),x[1][0],x[1][1])).sortBy(lambda x:x[0])
    # all_result.foreach(p)

    # e = d.filter(lambda x:(filterLength(x))).map(lambda x:(x[0].split("|")[0],x[0].split("|")[1],x[1][0],x[1][1]))

    schema = StructType([StructField("uuid", StringType(), False),StructField("law_id", StringType(), True)])

    f = sqlContext.createDataFrame(results, schema=schema)
    # f.show()
    # , mode = "overwrite"
    # useUnicode = true & characterEncoding = utf8，指定写入mysql时的数据编码，否则会乱码。
    f.write.jdbc(url='jdbc:mysql://cdh-slave1:3306/laws_doc2?useUnicode=true&characterEncoding=utf8', table='tmp_lawlist_id',properties={"user": "root", "password": "root"})

    sc.stop()