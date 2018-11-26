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
        l.append(x)
        #将分组结果ResultIterable转换为List
    return "||".join(l)      #列表不能直接存入Mysql

def get_history_titles(uuid_ids):
    uuid,ids = uuid_ids[0],uuid_ids[1]
    l = []
    history_l = []
    title_l = []
    for x in ids:
        al = x.decode("utf-8").split("||")  # 写入Mysql的数据必须是unicode编码，str需解码
        history_l.append(al[0])
        title_l.append(al[1])
    return (uuid,"||".join(history_l),"||".join(title_l))

def get_title_short_id(x):              #保证lawlist和law_id的有序！
    k = x[0].encode("utf-8") + "|" + x[1].encode("utf-8")
    v = k + "_" + str(x[2])
    return (k,v)



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

if __name__ == "__main__":

    conf = SparkConf()
    sc = SparkContext(conf=conf)
    sqlContext = SQLContext(sc)
    # sc.setLogLevel("ERROR")  # ALL, DEBUG, ERROR, FATAL, INFO, OFF, TRACE, WARN
    # uuid_type_history_title = sqlContext.read.jdbc(url='jdbc:mysql://cdh-slave1:3306/civil', table='uuid_reason_lawlist',column='id',lowerBound=0,upperBound=100000,numPartitions=70,properties={"user": "root", "password": "HHly2017."})
    uuid_title = sqlContext.read.jdbc(url='jdbc:mysql://cdh-slave1:3306/civil', table='tmp_wxy',column='id',lowerBound=110000,upperBound=120000,numPartitions=100,properties={"user": "root", "password": "HHly2017."})
    uuid_history= sqlContext.read.jdbc(url='jdbc:mysql://cdh-slave1:3306/civil', table='uuid_court_history',column='id',lowerBound=490000,upperBound=500000,numPartitions=14,properties={"user": "root", "password": "HHly2017."})
    # uuid_history= sqlContext.read.jdbc(url='jdbc:mysql://cdh-slave1:3306/civil', table='uuid_court_history',predicates=["id >= 1 and id <= 100"],properties={"user": "root", "password": "HHly2017."})
    # lawlist= sqlContext.read.jdbc(url='jdbc:mysql://cdh-slave1:3306/civil', table='uuid_reason_lawlist',
    #                           predicates=["id <= 500000", "id > 500000 and id <= 1000000",
    #                           "id > 1000000 and id <= 1500000", "id > 1500000 and id <= 2000000",
    #                           "id > 2000000 and id <= 2500000", "id > 2500000 and id <= 3000000",
    #                           "id > 3000000 and id <= 3500000", "id > 3500000 and id <= 4000000",
    #                           "id > 4000000 and id <= 4500000", "id > 4500000 and id <= 5000000",
    #                           "id > 5000000 and id <= 5500000", "id > 5500000 and id <= 6000000",
    #                           "id > 6000000 and id <= 6500000", "id > 6500000 "],
    #                           properties={"user": "root", "password": "HHly2017."})
    def filter_history_null(x):
            if x and x != '':
                return True
            return False

    def get_normal(x):
        if len(x[1]) == 36 or len(x[1]) == 24:
            return True
        else:
            return False
    def get_abnormal(x):
        if len(x[1]) != 36 and len(x[1]) != 24:
            return True
        else:
            return False

    def get_27(x):
        if x[1][-27:] == 'b647-11e3-84e9-5cf3fc0c2c18':
            return True
        else:
            return False

    def get_not_27(x):
        if x[1][-27:] != 'b647-11e3-84e9-5cf3fc0c2c18':
            return True
        else:
            return False

    p1 = ur'\u7b2c[\u4e00\u4e8c\u4e09\u56db\u4e94\u516d\u4e03\u516b\u4e5d\u5341\u767e\u5343]{1,10}\u6761'
    p2 = ur'[\u300a\u300b]'  # 按《》切分
    # uuid_title = uuid_history_title.select('uuid','title')

    uuid_k_v = uuid_title.select('uuid').map(lambda x:(x[0][-27:],x[0]))

    def filter_27_uuid(x):   #'a','c','d','e','f'
        x = x.strip()
        if len(x) == 36 and x[0][-27:] == 'b647-11e3-84e9-5cf3fc0c2c18' and (x.startswith("a") or x.startswith("c") or x.startswith("d") or x.startswith("e") or x.startswith("f")):
             return True
        return False


    uuid_history = uuid_history.select('uuid','history_origin').map(lambda x:x).filter(lambda x:filter_history_null(x[1])).flatMapValues(lambda x:(x.split("||")))

    normal_data = uuid_history.filter(lambda x:get_normal(x))           #后27位重复的uuid的后27位： b647-11e3-84e9-5cf3fc0c2c18
    abnormal_data_not_27 = uuid_history.filter(lambda x: get_abnormal(x)).filter(lambda x: get_not_27(x)).map(lambda x: (x[1][-27:], x[0])).groupByKey().mapValues(lambda x:(get_uuids(x)))

    normal_data2 = uuid_k_v.join(abnormal_data_not_27).map(lambda x:x[1]).flatMapValues(lambda x:(x.split("||"))).map(lambda x:(x[1],x[0]))

    abnormal_data_27 = uuid_history.filter(lambda x:get_abnormal(x)).filter(lambda x:get_27(x))


    uuid_k_v_27 = uuid_title.select('uuid').map(lambda x:x[0]).filter(lambda x:filter_27_uuid(x))  #找出后27位相同、且以a,c,d,e,f开头的uuids
    uuid_27_l = uuid_k_v_27.collect()
    uuid_broadcast = sc.broadcast(uuid_27_l)
    def get_v(x):
        ul= []
        for i in uuid_broadcast.value:
            if x == i[36-len(x):]:
                ul.append(i)

        if len(ul) == 1:     #匹配到一个时才可以保留
            return ul[0]
        else:
            return ""


    def filter_null(x):
        if x != '':         # 过滤掉数据库中，lawlist为Null或''的行。
            return True
        return False

    normal_data3 = abnormal_data_27.mapValues(lambda x:get_v(x)).filter(lambda x:filter_null(x))

    #uuid_history_all 为标准的：uuid,history
    uuid_history_all = normal_data.union(normal_data2).union(normal_data3).map(lambda x:(x[1],x[0])).groupByKey().mapValues(lambda x:get_uuids(x))

    def get_u_t(x):
        return (x[0],x[0].encode("utf-8") + "||" + x[1].encode("utf-8"))

    a = uuid_title.select('uuid','title').map(lambda x:get_u_t(x))
    history_title_results= a.join(uuid_history_all).map(lambda x:x[1]).flatMapValues(lambda x:x.split("||")).map(lambda x:(x[1],x[0])).groupByKey().map(lambda x:(get_history_titles(x)))

    # print str(c.count()) + "======================"
    # c.foreach(p)

    # lawlist_title_id_result = lawlist_id2.join(c).map(lambda x:x[1]).flatMapValues(lambda x:(x.split("||"))).map(lambda x:(x[1],x[0])).groupByKey().map(lambda x:(get_lawlist_ids(x)))

    schema = StructType([StructField("uuid", StringType(), False),StructField("history", StringType(), False),StructField("title", StringType(), False)])

    f = sqlContext.createDataFrame(history_title_results, schema=schema)
    # , mode = "overwrite"
    # useUnicode = true & characterEncoding = utf8，指定写入mysql时的数据编码，否则会乱码。
    # print str(f.count()) + "======================"
    f.write.jdbc(url='jdbc:mysql://cdh-slave1:3306/civil?useUnicode=true&characterEncoding=utf8', table='judgment_etl_uuid_history_title_result',properties={"user": "root", "password": "HHly2017."})

    sc.stop()