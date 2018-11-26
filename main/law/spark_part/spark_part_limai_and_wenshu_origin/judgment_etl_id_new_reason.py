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
    reason_null = sqlContext.read.jdbc(url='jdbc:mysql://cdh-slave1:3306/laws_doc2', table='reason_uid_distinct_result',column='id',lowerBound=0,upperBound=50000,numPartitions=1,properties={"user": "root", "password": "root"})
    reason_uid = sqlContext.read.jdbc(url='jdbc:mysql://cdh-slave1:3306/laws_doc', table='reason',column='id',lowerBound=0,upperBound=100,numPartitions=15,properties={"user": "root", "password": "root"})
    # reason_null= sqlContext.read.jdbc(url='jdbc:mysql://cdh-slave1:3306/laws_doc', table='judgment_etl_reason_uid_is_null',predicates=["id >= 1 and id <= 10"],properties={"user": "root", "password": "root"})
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
    #     # print type(x)
    #     print type(x[0]),type(x[1])
    #     print x[0],x[1]
    def filter_(x):
        if x[1] and x[1] != '':       #过滤掉数据库中，lawlist为Null或''的行。
            return True
        return False

    def extact_reason(x):
        # if x and x != '':
        uid_l = x.split("||")
        return uid_l

    def get_uuids(uuids):
        l = []
        for x in uuids:
            l.append(x)        #将分组结果ResultIterable转换为List
        return "||".join(l)      #列表不能直接存入Mysql

    def get_new_name(new_names):
        l = []
        for x in new_names:
            l.append(x)        #将分组结果ResultIterable转换为List
        return "||".join(l)

    reason_uids = reason_uid.map(lambda x:(x[6],x[5]))      #x[5],x[6] -> new_name , uid
    c = reason_null.map(lambda x:(str(x[0]),x[1])).filter(lambda x:filter_(x)).flatMapValues(lambda x:extact_reason(x)).map(lambda x:(x[1],x[0])).groupByKey().mapValues(lambda v:get_uuids(v))

    reason_uids_result = reason_uids.join(c).map(lambda x:x[1]).flatMapValues(lambda x:(x.split("||"))).map(lambda x:(x[1],x[0])).groupByKey().mapValues(lambda x:(get_new_name(x)))

    schema = StructType([StructField("id", StringType(), False),StructField("new_names", StringType(), False)])

    f = sqlContext.createDataFrame(reason_uids_result, schema=schema)
    # , mode = "overwrite"
    # useUnicode = true & characterEncoding = utf8，指定写入mysql时的数据编码，否则会乱码。
    f.write.jdbc(url='jdbc:mysql://cdh-slave1:3306/laws_doc2?useUnicode=true&characterEncoding=utf8', table='judgment_etl_id_new_reason_result',properties={"user": "root", "password": "root"})

    sc.stop()