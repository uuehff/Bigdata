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
    df = sqlContext.read.jdbc(url='jdbc:mysql://cdh-slave1:3306/laws_doc', table='(select id,lawyer,law_office from lawyers) tmp',column='id',lowerBound=0,upperBound=100000,numPartitions=10,properties={"user": "root", "password": "root"})
    df2 = sqlContext.read.jdbc(url='jdbc:mysql://cdh-slave1:3306/laws_doc', table='(select id,plaintiff_info,defendant_info from tmp_lawyers ) tmp2',column='id',lowerBound=0,upperBound=100000,numPartitions=10,properties={"user": "root", "password": "root"})
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
    # def p2(x):
    #     k,v = x[0],x[1]
    #     print k,
    #     # print type(v)
    #     for i2 in v:
    #         print i2,
    #     print "\n"
    def filter_(x):
        if x[0] and x[0] != '' and x[1] and x[1] != '':       #过滤掉数据库中，lawlist为Null或''的行。
            return True
        return False

    def deal_lawyer(lawyer,law_office):
        if lawyer != "" and lawyer.startswith(u"一"):
            lawyer = lawyer[1:]   #去掉第一个汉字
        s = ""
        if law_office[2] == u'省' or law_office[2] == u'市' or law_office[2] == u'县':  # 同一律师名字下，将第三个字为省、市、县去掉。
            t = []
            for i in range(0, len(law_office)):
                if i == 2:
                    continue
                t.append(law_office[i])
            s = "".join(t)
        else:
            s = law_office
        s = s.replace(u"律师事务所", "")  # 统一将结尾处理为律师事务所,去重
        s = s.replace(u"事务所", "")
        s = s + u"律师事务所"
        k_v = lawyer + "|" + s
        return k_v
    def trans(x):
        plain = []
        defen = []
        if x[1] and x[1] != "":
            js = json.loads(x[1])
            for k in js:
                plain.append(deal_lawyer(k,js[k]))

        if x[2] and x[2] != "":
            js2 = json.loads(x[2])
            for k2 in js2:
                defen.append(deal_lawyer(k2,js2[k2]))

        return (x[0],plain,defen)

    # c = df.map(lambda x:((x[3],x[1]),x[2])).filter(lambda x:filter_(x[1])).flatMapValues(lambda x:x.split(",")).map(lambda x:(x[1],x[0])).groupByKey().cache()
    lawyer_k_v = df.map(lambda x:(str(x[0]),x[1]+ "|" +x[2])).map(lambda x:(x[1],x[0]))  #（unicode,str）
    # lawyer_k_v.foreach(p_)
    tr = df2.map(lambda x:(str(x[0]),x[1],x[2])).map(lambda x:trans(x))    #（str list list），需要将id的类型int转为str，才可以join，连接。
    # tr.foreach(p)
    def get_ids(ids):
        l = []
        for x in ids:
            l.append(x)        #将分组结果ResultIterable转换为List
        return "||".join(l)
    def get_new_name(new_names):
        l = []
        for x in new_names:
            l.append(x)        #将分组结果ResultIterable转换为List
        return "||".join(l)

    #注意：这里加不加filter(filter_)过滤函数都一样，flatMapValues对value为[]进行展开时，不会返回包含该[]对应key任何记录。
    s1 = tr.map(lambda x:(x[0],x[1])).flatMapValues(lambda x:x).filter(filter_).map(lambda x:(x[1],x[0])).groupByKey().mapValues(lambda v:get_ids(v))  # (plaintiff_info,id)
    # s1.foreach(p_)

    s2 = tr.map(lambda x:(x[0],x[2])).flatMapValues(lambda x:x).filter(filter_).\
        map(lambda x:(x[1],x[0])).groupByKey().mapValues(lambda v:get_ids(v))  #（defendant_info,id）
    # s2.foreach(p_)
    result_s1 = lawyer_k_v.join(s1).map(lambda x:x[1]).flatMapValues(lambda x:(x.split("||"))).map(lambda x:(x[1],x[0])).groupByKey().mapValues(lambda x:(get_new_name(x)))
    # result_s1.foreach(p_)
    result_s2 = lawyer_k_v.join(s2).map(lambda x:x[1]).flatMapValues(lambda x:(x.split("||"))).map(lambda x:(x[1],x[0])).groupByKey().mapValues(lambda x:(get_new_name(x)))
    # result_s2.foreach(p_)
    all_result = result_s1.fullOuterJoin(result_s2).sortByKey().map(lambda x:(int(x[0]),x[1][0],x[1][1]))
    # all_result.foreach(p)

    # e = d.filter(lambda x:(filterLength(x))).map(lambda x:(x[0].split("|")[0],x[0].split("|")[1],x[1][0],x[1][1]))

    schema = StructType([StructField("id", IntegerType(), False),StructField("plaintiff_id", StringType(), True),StructField("denfendant_id", StringType(), True)])

    f = sqlContext.createDataFrame(all_result, schema=schema)
    # f.show()
    # , mode = "overwrite"
    # useUnicode = true & characterEncoding = utf8，指定写入mysql时的数据编码，否则会乱码。
    f.write.jdbc(url='jdbc:mysql://cdh-slave1:3306/laws_doc?useUnicode=true&characterEncoding=utf8', table='plain_defen_id',properties={"user": "root", "password": "root"})

    sc.stop()