# -*- coding: utf-8 -*-

from  pyspark import SparkContext,SparkConf
from pyspark.sql import SQLContext
from pyspark.sql.types import *

import re
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
    reason_null = sqlContext.read.jdbc(url='jdbc:mysql://cdh-slave1:3306/civil', table='uuid_reason_lawlist',column='id',lowerBound=0,upperBound=1000000,numPartitions=7,properties={"user": "root", "password": "HHly2017."})
    reason_uid = sqlContext.read.jdbc(url='jdbc:mysql://cdh-slave1:3306/civil', table='reason',column='id',lowerBound=0,upperBound=2000,numPartitions=1,properties={"user": "root", "password": "HHly2017."}).cache()
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

    def extact_reason(x):
        # if x and x != '':
        uid_l = x.split("||")
        return uid_l

    def get_uuids(uuids):
        l = []
        for x in uuids:
            l.append(x)        #将分组结果ResultIterable转换为List
        return "||".join(l)      #列表不能直接存入Mysql


    def flat_uid(uid):
        reason_uid = []
        if len(uid) == 7:
            reason_uid.append(uid[:4])
        elif len(uid) == 10:
            reason_uid.append(uid[:4])
            reason_uid.append(uid[:7])
        elif len(uid) == 13:
            reason_uid.append(uid[:4])
            reason_uid.append(uid[:7])
            reason_uid.append(uid[:10])
        elif len(uid) == 16:
            reason_uid.append(uid[:4])
            reason_uid.append(uid[:7])
            reason_uid.append(uid[:10])
            reason_uid.append(uid[:13])
        else:
            pass
        # reason_uid.append(uid)       #这里的自己uid传过来是唯一的，且要与reason_name保持顺序一致，这里就不添加，后面使用字符串连接上去
        return reason_uid

    def get_unique_uids(uids):
        l = []
        for x in uids:
            l.append(x)        #将分组结果ResultIterable转换为List
        s = "|" + "||".join(l)      #最前面加|,保证也能匹配到第一个uuid.

        t2 = []
        for i in l:
            if s.count("|"+i) == 1:             #出现过一次，代表一个案由
                t2.append(i)
        unique_uids = "||".join(t2)

        # t3 = []
        # for uid in t2:
        #     t3.extend(flat_uid(uid))
        # reason_uids = "||".join(list(set(t3)))

        # return (reason_uids,unique_uids)
        return unique_uids


    def get_reason_name_and_uids(x):
        uuid,uid_names = x[0],x[1]
        uid_l = []
        name_l = []
        for x in uid_names:
            al = x.decode("utf-8").split("_")    #写入Mysql的数据必须是unicode编码，str需解码
            uid_l.append(al[0])
            name_l.append(al[1])
        reason_names = "||".join(name_l)

        # s = "|" + "||".join(uid_l)      #最前面加|,保证也能匹配到第一个uuid.
        # t2 = []
        # for i in uid_l:
        #     if s.count("|"+i) == 1:             #出现过一次，代表一个案由
        #         t2.append(i)
        # unique_uids = "||".join(t2)

        t3 = []
        for uid in uid_l:       #这里的uid_l已经是唯一的，经前面的get_unique_uids函数处理过
            t3.extend(flat_uid(uid))
        reason_uids = "||".join(uid_l) + "||" + "||".join(list(set(t3)))

        return (uuid,reason_names,reason_uids)
        # return unique_uids


    def reason_del_zui(x):
        reason = x[5][:len(x[5])-1]     #去掉罪字
        return (reason,x[6])


    reason_uids = reason_uid.map(lambda x:reason_del_zui(x))
    reason_uids2 = reason_uid.map(lambda x:(x[6],x[6].encode("utf-8")+"_"+x[5].encode("utf-8")))
    # reason_uids2.foreach(p)
    # print str(reason_uids2.count()) + "=================="
    c1 = reason_null.select('uuid','doc_reason').map(lambda x:(x[0],x[1])).filter(lambda x:filter_(x)).flatMapValues(lambda x:extact_reason(x)).map(lambda x:(x[1],x[0])).cache()

    c2 = c1.groupByKey().mapValues(lambda v:get_uuids(v)).cache()

    c3 = reason_uids.join(c2).map(lambda x:x[1]).flatMapValues(lambda x:(x.split("||"))).map(lambda x:(x[1],x[0])).cache()

    c4 = c3.groupByKey().mapValues(lambda x:(get_unique_uids(x))).cache()

    d = c4.flatMapValues(lambda x:(extact_reason(x))).map(lambda x:(x[1],x[0])).groupByKey().mapValues(lambda v:get_uuids(v))
    reason_uids_result = reason_uids2.join(d).map(lambda x:x[1]).flatMapValues(lambda x:(x.split("||"))).map(lambda x:(x[1],x[0])).groupByKey().map(lambda x:(get_reason_name_and_uids(x)))

    schema = StructType([StructField("uuid", StringType(), False),StructField("reason_names", StringType(), False),StructField("reason_uids", StringType(), False)])

    f = sqlContext.createDataFrame(reason_uids_result, schema=schema)
    # , mode = "overwrite"
    # useUnicode = true & characterEncoding = utf8，指定写入mysql时的数据编码，否则会乱码。
    # print str(f.count()) + "======================"
    f.write.jdbc(url='jdbc:mysql://cdh-slave1:3306/civil?useUnicode=true&characterEncoding=utf8', table='judgment_etl_uuid_reason_name_uid_result',properties={"user": "root", "password": "HHly2017."})

    sc.stop()