# -*- coding: utf-8 -*-

from  pyspark import SparkContext,SparkConf
from pyspark.sql import SQLContext
from pyspark.sql.types import *
import os

if __name__ == "__main__":
    # if len(sys.argv) > 2:
    #     host = sys.argv[1]
    #     hbase_table_read = sys.argv[2]
    #     hbase_table_save = sys.argv[3]
    # else:
    # host = '192.168.12.35'
    # hbase_table_read = 'laws_doc:judgment'
    # hbase_table_save = 'laws_doc:label'
    PYSPARK_PYTHON = "C:\\Python27\\python.exe"    #多版本python情况下，需要配置这个变量指定使用哪个版本
    os.environ["PYSPARK_PYTHON"] = PYSPARK_PYTHON
    conf = SparkConf()
    sc = SparkContext(conf=conf)
    sqlContext = SQLContext(sc)
    # sc.setLogLevel("ERROR")  # ALL, DEBUG, ERROR, FATAL, INFO, OFF, TRACE, WARN '(select id,uuid,plaintiff_info,defendant_info from tmp_lawyers ) tmp'
    df = sqlContext.read.jdbc(url='jdbc:mysql://cdh-slave2:3306/civil', table='(select id,lawyer,law_office from lawyers ) tmp',column='id',lowerBound=0,upperBound=70,numPartitions=7,properties={"user": "root", "password": "HHly2017."})
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
    # def filter_(x):
    #     if x[0] and x[0] != '' and x[1] and x[1] != '':       #过滤掉数据库中，lawlist为Null或''的行。
    #         return True
    #     return False
    # 丁中亚
    # 河南振廖律师事务所
    # 丁中亚
    # 河南振蓼事务所
    # 丁中亚
    # 河南振蓼律师事务所
    # 丁中亚
    # 河南省振蓼律师事务所
    # 丁中亚
    # 河南蓼阳律师事务所
    # 丁中亚
    # 浙江振蓼律师事务所
    def distinct_office(law_offices):
        l = []
        for x in law_offices:
            s = ""
            if x[2] == u'省' or x[2] == u'市' or x[2] == u'县':  #同一律师名字下，将第三个字为省、市、县去掉。
                t = []
                for i in range(0,len(x)):
                    if i == 2:
                        continue
                    t.append(x[i])
                s = "".join(t)
            else:
                s = x
            s = s.replace(u"律师事务所","")   #统一将结尾处理为律师事务所,去重
            s = s.replace(u"事务所","")
            s = s + u"律师事务所"
            l.append(s)

        return list(set(l))      #返回去重后得数组

    # x[3],x[1]),x[2] => casedate,uuid,lawlist
    # c = df.map(lambda x:((x[3],x[1]),x[2])).filter(lambda x:filter_(x[1])).flatMapValues(lambda x:x.split(",")).map(lambda x:(x[1],x[0])).groupByKey().cache()
    c = df.map(lambda x:(x[1],x[2])).groupByKey()

    d = c.flatMapValues(lambda v:distinct_office(v))
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

    schema = StructType([StructField("lawyer", StringType(), False),StructField("law_office", StringType(), False)])

    f = sqlContext.createDataFrame(d, schema=schema)
    # f.show()
    # , mode = "overwrite"
    # useUnicode = true & characterEncoding = utf8，指定写入mysql时的数据编码，否则会乱码。
    f.write.jdbc(url='jdbc:mysql://cdh-slave2:3306/civil?useUnicode=true&characterEncoding=utf8', table='lawyers2',properties={"user": "root", "password": "HHly2017."})

    sc.stop()