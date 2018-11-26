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
    PYSPARK_PYTHON = "C:\\Python27\\python.exe"    #多版本python情况下，需要配置这个变量指定使用哪个版本
    os.environ["PYSPARK_PYTHON"] = PYSPARK_PYTHON
    conf = SparkConf()
    sc = SparkContext(conf=conf)
    sqlContext = SQLContext(sc)
    # sc.setLogLevel("ERROR")  # ALL, DEBUG, ERROR, FATAL, INFO, OFF, TRACE, WARN '(select id,uuid,plaintiff_info,defendant_info from tmp_lawyers ) tmp'
    #
    # df = sqlContext.read.jdbc(url='jdbc:mysql://cdh-slave2:3306/law', table='(select id,lawlist_id from law_rule_result2 where art_digit is not null) tmp',column='id',lowerBound=0,upperBound=2800000,numPartitions=10,properties={"user": "root", "password": "HHly2017."})
    df = sqlContext.read.jdbc(url='jdbc:mysql://cdh-slave1:3306/laws_doc', table='(select * from lawyer_info5 ) tmp2',column='id',lowerBound=0,upperBound=2800000,numPartitions=10,properties={"user": "root", "password": "root"})
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
        print type(x),x
        # for i in x:
        #     print i
    # def p_(x):
    #     # print type(x)
    #     print type(x)
    #     print type(x[0]),type(x[1])
    #     print x[0],x[1]

    def trans(x):
        # Row(id=95069, name=u'\u738b\u5176\u4f2f', pra_number=u'16101200110511000', gender=u'\u7537', nation=u'',
        #     edu_origin=u'\u5927\u4e13', politics=u'\u4e2d\u5171\u515a\u5458',
        #     org_name=u'\u9655\u897f\u8bfa\u5c14\u5f8b\u5e08\u4e8b\u52a1\u6240', org_identity=u'',
        #     pra_type=u'\u4e13\u804c\u5f8b\u5e08', pra_course=u'', first_pra_time=u'', qua_number=u'', qua_time=u'')
        # Row(id=95070, name=u'\u738b\u5176\u4f2f', pra_number=u'16101200110511000', gender=u'\u7537', nation=u'',
        #     edu_origin=u'\u672c\u79d1', politics=u'\u4e2d\u5171\u515a\u5458',
        #     org_name=u'\u9655\u897f\u8bfa\u5c14\u5f8b\u5e08\u4e8b\u52a1\u6240', org_identity=u'',
        #     pra_type=u'\u4e13\u804c\u5f8b\u5e08', pra_course=u'', first_pra_time=u'', qua_number=u'', qua_time=u'')
        # (
        name = x[0][0]   #x[0]为分组后的key
        pra_number = x[0][1]
        org_name = x[0][2]

        gender = ""
        nation = ""
        edu_origin = ""
        politics = ""
        org_identity = ""
        pra_type = ""
        pra_course = ""
        first_pra_time = ""
        qua_number = ""
        qua_time = ""
        for row in x[1]:
            if gender == "":
                gender = row.gender
            if nation == "":
                nation = row.nation
            if edu_origin == "":
                edu_origin = row.edu_origin
            if politics == "":
                politics = row.politics
            if org_identity == "":
                org_identity = row.org_identity
            if pra_type == "":
                pra_type = row.pra_type
            if pra_course == "":
                pra_course = row.pra_course
            if first_pra_time == "":
                first_pra_time = row.first_pra_time
            if qua_number == "":
                qua_number = row.qua_number
            if qua_time == "":
                qua_time = row.qua_time
        # print gender
        # print name, pra_number, gender, nation, edu_origin, politics, org_name, org_identity, pra_type, pra_course, first_pra_time, qua_number, qua_time
        return (name, pra_number, gender, nation, edu_origin, politics, org_name, org_identity, pra_type, pra_course, first_pra_time, qua_number, qua_time)


    result = df.map(lambda x:x).groupBy(lambda x:(x[1],x[2],x[7])).map(lambda x:trans(x))

    schema = StructType([StructField("name", StringType(), False),
                         StructField("pra_number", StringType(), True),
                         StructField("gender", StringType(), True)
                            , StructField("nation", StringType(), True)
                            , StructField("edu_origin", StringType(), True)
                            , StructField("politics", StringType(), True)
                            ,StructField("org_name", StringType(), False)
                            , StructField("org_identity", StringType(), True)
                            , StructField("pra_type", StringType(), True)
                            , StructField("pra_course", StringType(), True)
                            , StructField("first_pra_time", StringType(), True)
                            , StructField("qua_number", StringType(), True)
                            , StructField("qua_time", StringType(), True)
                         ])

    f = sqlContext.createDataFrame(result, schema=schema)
    # f.show()
    # , mode = "overwrite"
    # useUnicode = true & characterEncoding = utf8，指定写入mysql时的数据编码，否则会乱码。
    f.write.jdbc(url='jdbc:mysql://cdh-slave1:3306/laws_doc?useUnicode=true&characterEncoding=utf8', table='lawyer_info6',properties={"user": "root", "password": "root"})

    sc.stop()