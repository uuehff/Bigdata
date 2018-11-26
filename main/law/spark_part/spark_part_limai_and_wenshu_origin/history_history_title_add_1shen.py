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
    uuid_history = sqlContext.read.jdbc(url='jdbc:mysql://cdh-slave1:3306/laws_doc2', table='uuid_history_title',column='id',lowerBound=0,upperBound=10000,numPartitions=1,properties={"user": "root", "password": "root"})
    # reason_uid = sqlContext.read.jdbc(url='jdbc:mysql://cdh-slave1:3306/laws_doc', table='reason',column='id',lowerBound=0,upperBound=100,numPartitions=15,properties={"user": "root", "password": "root"})
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
    # def p2(x):
    #     k,v = x[0],x[1]
    #     print k,
    #     # print type(v)
    #     for i2 in v:
    #         print i2,
    #     print "\n"
    def filter_(x):
        if x[1] and x[1] != '':       #过滤掉数据库中，lawlist为Null或''的行。
            return True
        return False

    def extact_uuid(x):
        # if x and x != '':
        uuid_l = x.split("||")
        return uuid_l

    def get_history_title(x):
        uuid,history_titles = x[0],x[1]
        uuid_l = []
        title = []
        for i in history_titles:
            al = i.decode("utf-8").split("||")  # 写入Mysql的数据必须是unicode编码，str需解码
            uuid_l.append(al[0])
            title.append(al[1])
        return (uuid, "||".join(uuid_l), "||".join(title))

    def get_reason_uids(uids):
        l = []
        for x in uids:
            l.append(x)        #将分组结果ResultIterable转换为List
        return "||".join(l)

    def get_k_v(x):
        return (x[0].encode("utf-8") + "||" + x[2].encode("utf-8"),x[1])

    # reason_uids = reason_uid.map(lambda x:(x[5],x[6]))
    # x[3],x[1]),x[2] => casedate,uuid,lawlist
    # c = df.map(lambda x:((x[3],x[1]),x[2])).filter(lambda x:filter_(x[1])).flatMapValues(lambda x:x.split(",")).map(lambda x:(x[1],x[0])).groupByKey().cache()
    uuid_history_title = uuid_history.select('uuid','history','title').map(lambda x:get_k_v(x)).filter(lambda x:filter_(x)).\
        flatMapValues(lambda x:extact_uuid(x)).map(lambda x:(x[1],x[0])).groupByKey().map(lambda v:get_history_title(v))
    # map(lambda x:(x[1],x[0])).groupByKey(24).cache()

    # reason_uids_result = reason_uids.join(c).map(lambda x:x[1]).flatMapValues(lambda x:(x.split("||"))).map(lambda x:(x[1],x[0])).groupByKey().mapValues(lambda x:(get_reason_uids(x)))
    # d1 = c.mapValues(lambda v:get_lawlist_ids(v)).cache()
    # d2 = c.mapValues(lambda v:get_lawlist_ids(v)).cache()

    # print d1.count() + "================="
    # print d2.count() + "================="

    # 经统计x[0].split("|")，分割后有等于1的法律发条，此为无效，否则x[0].split("|")[1]报错数组越界！
    # def filterLength(x):
    #     t = x[0].split("|")
    #     if len(t) == 2:
    #         return True
    #     return False

    # e = d.filter(lambda x:(filterLength(x))).map(lambda x:(x[0].split("|")[0],x[0].split("|")[1],x[1][0],x[1][1]))

    schema = StructType([StructField("uuid", StringType(), False),StructField("history", StringType(), False),StructField("title", StringType(), False)])

    f = sqlContext.createDataFrame(uuid_history_title, schema=schema)
    # , mode = "overwrite"
    # useUnicode = true & characterEncoding = utf8，指定写入mysql时的数据编码，否则会乱码。
    f.write.jdbc(url='jdbc:mysql://cdh-slave1:3306/laws_doc?useUnicode=true&characterEncoding=utf8', table='judgment_etl_uuid_history_title_result',properties={"user": "root", "password": "root"})

    sc.stop()