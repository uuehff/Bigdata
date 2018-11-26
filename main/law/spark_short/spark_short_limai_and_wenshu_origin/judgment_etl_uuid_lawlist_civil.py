# -*- coding: utf-8 -*-

from  pyspark import SparkContext,SparkConf
from pyspark.sql import SQLContext
from pyspark.sql.types import *

import re

def p(x):
    if x[1]:
        print type(x)
        print x
        # print x[1]
        # exit(0)
def filter_(x):
    if x[1] and x[1] != '':       #过滤掉数据库中，lawlist为Null或''的行。
        return True
    return False

def get_uuids(uuids):
    l = []
    for x in uuids:
        l.append(x)        #将分组结果ResultIterable转换为List
    return "||".join(l)      #列表不能直接存入Mysql

def get_lawlist_ids(uuid_ids):
    uuid,ids = uuid_ids[0],uuid_ids[1]
    l = []
    title_short_num = []
    lawlist_id = []
    for x in ids:
        al = x.decode("utf-8").split("_")  # 写入Mysql的数据必须是unicode编码，str需解码
        title_short_num.append(al[0])
        lawlist_id.append(al[1])
    return (uuid,"||".join(title_short_num),"||".join(lawlist_id))

def get_title_short_id(x):              #保证lawlist和law_id的有序！
    k = x[0].encode("utf-8") + "|" + x[1].encode("utf-8")
    v = k + "_" + str(x[2])
    return (k,v)

if __name__ == "__main__":

    conf = SparkConf()
    sc = SparkContext(conf=conf)
    sqlContext = SQLContext(sc)
    # sc.setLogLevel("ERROR")  # ALL, DEBUG, ERROR, FATAL, INFO, OFF, TRACE, WARN
    # lawlist = sqlContext.read.jdbc(url='jdbc:mysql://cdh-slave1:3306/civil', table='uuid_reason_lawlist',column='id',lowerBound=0,upperBound=100000,numPartitions=70,properties={"user": "root", "password": "HHly2017."})
    lawlist_id = sqlContext.read.jdbc(url='jdbc:mysql://cdh-slave1:3306/civil', table='law_rule_result2',column='id',lowerBound=0,upperBound=100000,numPartitions=30,properties={"user": "root", "password": "HHly2017."})
    # lawlist= sqlContext.read.jdbc(url='jdbc:mysql://cdh-slave1:3306/civil', table='uuid_reason_lawlist',predicates=["id >= 1 and id <= 100"],properties={"user": "root", "password": "HHly2017."})
    lawlist= sqlContext.read.jdbc(url='jdbc:mysql://cdh-slave1:3306/civil', table='uuid_reason_lawlist',
                              predicates=["id <= 500000", "id > 500000 and id <= 1000000",
                              "id > 1000000 and id <= 1500000", "id > 1500000 and id <= 2000000",
                              "id > 2000000 and id <= 2500000", "id > 2500000 and id <= 3000000",
                              "id > 3000000 and id <= 3500000", "id > 3500000 and id <= 4000000",
                              "id > 4000000 and id <= 4500000", "id > 4500000 and id <= 5000000",
                              "id > 5000000 and id <= 5500000", "id > 5500000 and id <= 6000000",
                              "id > 6000000 and id <= 6500000", "id > 6500000 "],
                              properties={"user": "root", "password": "HHly2017."})


    def etl_lawlist(p1, p2, lawlist):
        if lawlist and lawlist.strip() != '':
            # if not (lawlist.strip().startswith("[") and lawlist.strip().endswith("]")):  # 去掉前后的所有"
            r1 = re.findall(ur'"{0,5}\["{0,5}', lawlist.strip())
            r2 = re.findall(ur'"{0,5}\]"{0,5}', lawlist.strip())
            if r1 and r2:
                start = r1.pop(0)
                end = r2.pop()
                lawlist = lawlist.strip().replace(start, "").replace(end, "")
                # l = list(eval(lawlist.strip()))                 #有脏数据不能直接使用eval()

                l = lawlist.split('", "')      #lawlist类似于：《最高人民法院关于审理建设工程施工合同纠纷案件适用法律问题的解释》第三条", "《中华人民共和国合同法》第九十七条", "最高人民法院关于审理建设工程施工合同纠纷案件适用法律问题的解释》第十条", "《中华人民共和国合同法》第九十八条
                if l:
                    tl = []
                    for i in l:
                        r1 = re.split(p2, i)
                        if len(r1) > 2:            #确保既有《，又有》
                            r2 = re.search(p1, r1[2])
                            if r2:                  #判断是否找到了条
                                tl.append(r1[1].encode("utf-8") + "|" + r2.group(0).encode("utf-8"))
                    return list(set(tl))  # 去重
                return []
            return []
        return []

    lawlist_id2 = lawlist_id.select('title_short','art_num','lawlist_id').map(lambda x:get_title_short_id(x))
    p1 = ur'\u7b2c[\u4e00\u4e8c\u4e09\u56db\u4e94\u516d\u4e03\u516b\u4e5d\u5341\u767e\u5343]{1,10}\u6761'
    p2 = ur'[\u300a\u300b]'  # 按《》切分
    c = lawlist.select('uuid','lawlist').map(lambda x:(x[0],x[1])).flatMapValues(lambda x: etl_lawlist(p1, p2, x)).filter(filter_).map(lambda x: (x[1], x[0])).groupByKey().mapValues(lambda v: get_uuids(v))
    # flatMapValues(lambda x: etl_lawlist(p1, p2, x)).filter(filter_).map(lambda x: (x[1].encode("utf-8"), x[0]))
        # groupByKey().mapValues(lambda v: get_uuids(v))
    # filter(filter_).map(lambda x: (x[1].encode("utf-8"), x[0])).groupByKey().mapValues(lambda v: get_uuids(v))
    # print str(c.count()) + "======================"
    # c.foreach(p)

    lawlist_title_id_result = lawlist_id2.join(c).map(lambda x:x[1]).flatMapValues(lambda x:(x.split("||"))).map(lambda x:(x[1],x[0])).groupByKey().map(lambda x:(get_lawlist_ids(x)))

    schema = StructType([StructField("uuid", StringType(), False),StructField("lawlist", StringType(), False),StructField("law_id", StringType(), False)])

    f = sqlContext.createDataFrame(lawlist_title_id_result, schema=schema)
    # , mode = "overwrite"
    # useUnicode = true & characterEncoding = utf8，指定写入mysql时的数据编码，否则会乱码。
    # print str(f.count()) + "======================"
    f.write.jdbc(url='jdbc:mysql://cdh-slave1:3306/civil?useUnicode=true&characterEncoding=utf8', table='judgment_etl_uuid_lawlist_law_id_result',properties={"user": "root", "password": "HHly2017."})

    sc.stop()