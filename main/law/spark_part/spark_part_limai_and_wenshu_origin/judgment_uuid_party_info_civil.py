# -*- coding: utf-8 -*-

from  pyspark import SparkContext,SparkConf
from pyspark.sql import SQLContext
from pyspark.sql.types import *
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

    conf = SparkConf()
    sc = SparkContext(conf=conf)
    sqlContext = SQLContext(sc)
    # sc.setLogLevel("ERROR")  # ALL, DEBUG, ERROR, FATAL, INFO, OFF, TRACE, WARN
    id_lawyer = sqlContext.read.jdbc(url='jdbc:mysql://cdh-slave2:3306/civil', table='id_lawyer',column='id',lowerBound=0,upperBound=200000,numPartitions=3,properties={"user": "root", "password": "HHly2017."})
    tmp_lawyers = sqlContext.read.jdbc(url='jdbc:mysql://cdh-slave2:3306/civil', table='(select id,uuid,plaintiff_info,defendant_info from tmp_lawyers ) tmp',column='id',lowerBound=0,upperBound=250000,numPartitions=11,properties={"user": "root", "password": "HHly2017."})
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
    def p(x):
        print type(x)
        print type(x[0]),type(x[1]),type(x[1])
        print x
        print x[0],x[1],x[2]
    # def p2(x):
    #     k,v = x[0],x[1]
    #     print k,
    #     # print type(v)
    #     for i2 in v:
    #         print i2,
    #     print "\n"
    def filter_(x):
        if (x[1] and x[1] != '') or (x[2] and x[2] != ''):       #过滤掉数据库中，lawlist为Null或''的行。
            return True
        return False

    def filter2_(x):
        if x[1] and x[1] != '' :       #过滤掉数据库中，lawlist为Null或''的行。
            return True
        return False

    def get_reason_uids(uids):
        l = []
        for x in uids:
            l.append(x)        #将分组结果ResultIterable转换为List
        return "||".join(l)


    def trans_value(x):
        pl = []
        dl = []
        if x[1] and x[1] != '':
            plaintiff_info = json.loads(x[1])
            for k in plaintiff_info.keys():
                pl.append(k.encode("utf-8") + "|" + plaintiff_info[k].encode("utf-8"))

        if x[2] and x[2] != '':
            defendant_info = json.loads(x[2])
            for k in defendant_info.keys():
                dl.append(k.encode("utf-8") + "|" + defendant_info[k].encode("utf-8"))
        return (x[0].encode("utf-8"),"||".join(pl),"||".join(dl))


    name_law_ids = id_lawyer.map(lambda x:(x[1].encode("utf-8") + "|" + x[2].encode("utf-8"),str(x[0])))    #str(x[0])) id为int，需转化一下

    c = tmp_lawyers.map(lambda x:(x[1],x[2],x[3])).filter(lambda x:filter_(x)).map(trans_value)

    #将原告、被告两个字段分开进行转化
    uuid_plaintiff_info = c.map(lambda x:(x[0],x[1])).filter(lambda x:filter2_(x)).flatMapValues(lambda x:(x.split("||"))).map(lambda x:(x[1],x[0])).groupByKey().mapValues(lambda x:(get_reason_uids(x)))
    uuid_defendant_info = c.map(lambda x:(x[0],x[2])).filter(lambda x:filter2_(x)).flatMapValues(lambda x:(x.split("||"))).map(lambda x:(x[1],x[0])).groupByKey().mapValues(lambda x:(get_reason_uids(x)))
    # uuid_defendant_info.foreach(p)

    # 将原告、被告两个字段分别进行匹配
    uuid_plaintiff_info_result = name_law_ids.join(uuid_plaintiff_info).map(lambda x:x[1]).flatMapValues(lambda x:(x.split("||"))).map(lambda x:(x[1],x[0])).groupByKey().mapValues(lambda x:(get_reason_uids(x)))
    uuid_defendant_info_result = name_law_ids.join(uuid_defendant_info).map(lambda x:x[1]).flatMapValues(lambda x:(x.split("||"))).map(lambda x:(x[1],x[0])).groupByKey().mapValues(lambda x:(get_reason_uids(x)))
    # uuid_plaintiff_info_result.foreach(p)

    #这里需要使用fullOuterJoin基于uuid进行组合数据，fullOuterJoin功能如下，其中None代表它对应的rdd中没有当前K的记录，None就是NoneType，有可能为None的
    # 字段在构造schema时，需要设置nullable = True,允许为空，这样存入mysql后，对应的就是Null,用is null查询：
    # >> > x = sc.parallelize([("a", 1), ("b", 4)])
    # >> > y = sc.parallelize([("a", 2), ("c", 8)])
    # >> > sorted(x.fullOuterJoin(y).collect())
    # [('a', (1, 2)), ('b', (4, None)), ('c', (None, 8))]
    result_all  = uuid_plaintiff_info_result.fullOuterJoin(uuid_defendant_info_result).map(lambda x:(x[0],x[1][0],x[1][1]))  #全都是数字字母格式的str，也能直接存入mysql

    schema = StructType([StructField("uuid", StringType(), False),StructField("plaintiff_id", StringType(), True),StructField("defendant_id", StringType(), True)])
    f = sqlContext.createDataFrame(result_all, schema=schema)
    # , mode = "overwrite"
    # useUnicode = true & characterEncoding = utf8，指定写入mysql时的数据编码，否则会乱码。
    f.write.jdbc(url='jdbc:mysql://cdh-slave2:3306/civil?useUnicode=true&characterEncoding=utf8', table='party_info_result_ids',properties={"user": "root", "password": "HHly2017."})

    sc.stop()