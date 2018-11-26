# -*- coding: utf-8 -*-

from  pyspark import SparkContext,SparkConf
from pyspark.sql import SQLContext
from pyspark.sql.types import *
import os

import re
if __name__ == "__main__":

    conf = SparkConf()
    sc = SparkContext(conf=conf)
    sqlContext = SQLContext(sc)

    # PYSPARK_PYTHON = "C:\\Python27\\python.exe"    #多版本python情况下，需要配置这个变量指定使用哪个版本
    # os.environ["PYSPARK_PYTHON"] = PYSPARK_PYTHON

    def p(x):
        print type(x),type(x[0]),type(x[1])
        # print type(x)
        # print type(x[0]),type(x[1])
        print x[0],x[1][0],x[1][1]
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


    # def flat_uid(uid):
    #     reason_uid = []
    #     if len(uid) == 7:
    #         reason_uid.append(uid[:4])
    #     elif len(uid) == 10:
    #         reason_uid.append(uid[:4])
    #         reason_uid.append(uid[:7])
    #     elif len(uid) == 13:
    #         reason_uid.append(uid[:4])
    #         reason_uid.append(uid[:7])
    #         reason_uid.append(uid[:10])
    #     elif len(uid) == 16:
    #         reason_uid.append(uid[:4])
    #         reason_uid.append(uid[:7])
    #         reason_uid.append(uid[:10])
    #         reason_uid.append(uid[:13])
    #     else:
    #         pass
    #     # reason_uid.append(uid)       #这里的自己uid传过来是唯一的，且要与reason_name保持顺序一致，这里就不添加，后面使用字符串连接上去
    #     return reason_uid
    # def get_reason(x):
    #     # acc.add(1)
    #     # uuid,title,trial_process
    #     title = x[1]
    #     trial_process = x[2]
    #     name = []
    #     uid = []
    #     for i in reason_broadcast.value:  #
    #         if i[0] in title or i[0] in trial_process:
    #             name.append(i[0])
    #             uid.append(i[1])
    #     uid_l = list(set(uid))
    #     t3 = []
    #     for uid in uid_l:       #这里的uid_l已经是唯一的，经前面的get_unique_uids函数处理过
    #         t3.extend(flat_uid(uid))
    #     reason_uids = "||".join(uid_l) + "||" + "||".join(list(set(t3)))
    #
    #     return (x[0],("||".join(list(set(name))),reason_uids))


    # judgment_new：556万
    df = sqlContext.read.jdbc(url='jdbc:mysql://cdh-slave1:3306/civil',
                               table='(select id,uuid,court from judgment_civil_all) tmp',
                               column='id', lowerBound=1, upperBound=6720000, numPartitions=30,
                               properties={"user": "root", "password": "HHly2017."})
    # court:4778条
    df1 = sqlContext.read.jdbc(url='jdbc:mysql://cdh-slave1:3306/civil',
                               table='(select id,name,province,full_uid from court ) tmp1',
                               column='id', lowerBound=1, upperBound=5000, numPartitions=1,
                               properties={"user": "root", "password": "HHly2017."})
    # reason：1497条
    # df2 = sqlContext.read.jdbc(url='jdbc:mysql://cdh-slave1:3306/laws_doc',
    #                            table='(select id,name,uid from reason ) tmp2',
    #                            column='id', lowerBound=1, upperBound=1500, numPartitions=1,
    #                            properties={"user": "root", "password": "root"})


    # acc = sc.accumulator(0)
    # print "df.count()======================" + str(df.count())
    # reason_broadcast = sc.broadcast(df2.map(lambda x:(x[1],x[2])).collect())
    # uuid_reason = df.map(lambda x:(x[1],x[3],x[4])).map(lambda x:get_reason(x))    #title_trial_process
    # print "uuid_reason.count()======================" + str(uuid_reason.count())
    # uuid_reason.foreach(p)
    uuid_court = df.map(lambda x:(x[2],x[1]))  #court,uuid
    court_province_full_uid = df1.map(lambda x:(x[1],(x[2],x[3])))   #court,province,full_uid
    uuid_province_full_uid = uuid_court.join(court_province_full_uid).map(lambda x:x[1]).map(lambda x:(x[0],x[1][0],x[1][1]))
    # .map(lambda x: (x[0], x[1][0], x[1][1]))  # uuid,province,full_uid
    # print "uuid_province_full_uid.count()======================" + str(uuid_province_full_uid.count())

    # result = uuid_reason.join(uuid_province_full_uid).map(lambda x:(x[0],x[1][0][0],x[1][0][1],x[1][1][0],x[1][1][1]))
    # print "acc======================" + str(acc.value)

    # reason_uids2 = reason_uid.map(lambda x:(x[6],x[6].encode("utf-8")+"_"+x[5].encode("utf-8")))
    # reason_uids2.foreach(p)
    # print str(reason_uids2.count()) + "=================="
    # c1 = reason_null.select('uuid','doc_reason').map(lambda x:(x[0],x[1])).filter(lambda x:filter_(x)).flatMapValues(lambda x:extact_reason(x)).map(lambda x:(x[1],x[0])).cache()

    # c2 = c1.groupByKey().mapValues(lambda v:get_uuids(v)).cache()

    # c3 = reason_uids.join(c2).map(lambda x:x[1]).flatMapValues(lambda x:(x.split("||"))).map(lambda x:(x[1],x[0])).cache()

    # c4 = c3.groupByKey().mapValues(lambda x:(get_unique_uids(x))).cache()

    # d = c4.flatMapValues(lambda x:(extact_reason(x))).map(lambda x:(x[1],x[0])).groupByKey().mapValues(lambda v:get_uuids(v))
    # reason_uids_result = reason_uids2.join(d).map(lambda x:x[1]).flatMapValues(lambda x:(x.split("||"))).map(lambda x:(x[1],x[0])).groupByKey().map(lambda x:(get_reason_name_and_uids(x)))

    schema = StructType([StructField("uuid", StringType(), False),
                         # StructField("reason", StringType(), True),
                         # StructField("reason_uid", StringType(), True),
                         StructField("province", StringType(), True),
                         StructField("court_uid", StringType(), True)])

    f = sqlContext.createDataFrame(uuid_province_full_uid, schema=schema)
    # , mode = "overwrite"
    # useUnicode = true & characterEncoding = utf8，指定写入mysql时的数据编码，否则会乱码。
    # print str(f.count()) + "======================"
    f.write.jdbc(url='jdbc:mysql://cdh-slave1:3306/civil?useUnicode=true&characterEncoding=utf8', table='court_uid',properties={"user": "root", "password": "HHly2017."})

    sc.stop()