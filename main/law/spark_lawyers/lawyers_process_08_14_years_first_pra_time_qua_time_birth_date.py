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
    df = sqlContext.read.jdbc(url='jdbc:mysql://cdh5-slave2:3306/laws_doc_lawyers_new', table='(select id,pra_number,birth_date,first_pra_time,qua_number,qua_time,years from hht_lawyer_12348gov_v3 ) tmp',column='id',lowerBound=1,upperBound=342600,numPartitions=10,properties={"user": "weiwc", "password": "HHly2017."})
    # df2 = sqlContext.read.jdbc(url='jdbc:mysql://cdh-slave1:3306/laws_doc2', table='(select id,plaintiff_info,defendant_info from tmp_lawyers ) tmp2',column='id',lowerBound=0,upperBound=100000,numPartitions=10,properties={"user": "root", "password": "root"})
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
    #     print type(x)
    #     print type(x[0]),type(x[1]),type(x[2])
    #     print x[0],x[1],x[2]
    # def p_(x):
        # print type(x)
        # print x[0],x[1]
        # for i in x[1]:
        #     print type(i),i
    def p2(x):
        # k,v = x[0],x[1]
        # print k,
        # print type(v)
        for i2 in x:
            print i2,
        print "\n"


    def get_results(x):
        # id,pra_number,birth_date,first_pra_time,qua_number,qua_time,years
        # 13101201511771334
        # A20113403210528
        pra_number = x[1]  #执业证号
        birth_date = x[2]  #出生日期
        first_pra_time = x[3] #首次执业时间
        qua_number = x[4] # 资格证号
        qua_time = x[5] # 资格证获取时间
        years = x[6] # 执业年限

        pra_number_year = int(pra_number[5:9])

        if birth_date and birth_date != "":
            birth_date_year = int(birth_date[:4])
        else:
            birth_date_year = None

        if first_pra_time and first_pra_time != "":
            first_pra_time_year = int(first_pra_time[:4])
        else:
            first_pra_time_year = None

        if qua_number and qua_number != "":
            qua_number_year = int(qua_number[1:5])
        else:
            qua_number_year = None

        if qua_time and qua_time != "" :
            qua_time_year = int(qua_time[:4])
        else:
            qua_time_year = None

        #birth_date, first_pra_time, qua_time，years整体处理业务规则：
        # 执业证号、资格证号、出生日期这些是死的；不对改变，会根据是否合理要或不要；
        # 首次执业时间 原始数据合理的会保留，不合理会推算；
        # 执业年限 根据首次执业时间或执业证年限去推算；
        # 资格证获取时间 原始数据合理的会保留，不合理的不进行推算；

        # 1、 pra_number_year-birth_date_year >= 18 或者 pra_number_year - birth_date_year >= 18 认为年龄合适
        # 2、qua_number_year < first_pra_time_year 认为首次执业时间合适，否则以pra_number_year作为首次执业时间
        # 3、qua_number_year  < qua_time_year < first_pra_time_year 认为资格证获取时间合适
        # 细分如下：
        # pra_number_year不满足条件：pra_number_year < 1970 or pra_number_year > 2018
        #     qua_number存在：
        #         qua_number_year - birth_date_year >= 18 认为年龄合适
        #         qua_number_year < first_pra_time_year 认为首次执业时间合适
        #         qua_number_year  < qua_time_year < first_pra_time_year  认为资格证获取时间合适
        #     qua_number不存在：
        #         first_pra_time不为空时，以first_pra_time为准，计算years 、birth_date
        #
        # pra_number_year满足条件：
        #          qua_number_year < first_pra_time_year 认为首次执业时间合适,不合适或first_pra_time_year为空时，
        #             赋值first_pra_time = pra_number_year，以pra_number_year作为首次执业时间
        #
        #         pra_number_year - birth_date_year >= 18 认为年龄合适
        #         qua_number_year  < qua_time_year < first_pra_time_year  当qua_number不为空，
        #             符合：qua_number_year > qua_time_year or qua_time_year > first_pra_time_year认为资格证获取时间合适


        if pra_number_year < 1970 or pra_number_year > 2018 :  #执业证年份不符合常规；
            if qua_number and qua_number != "":                 #资格证号存在情况下；
                if birth_date and birth_date != "" :
                    if qua_number_year - birth_date_year < 18:
                        birth_date = ""
                else :
                    birth_date = ""
                if first_pra_time and first_pra_time != "":
                    if first_pra_time_year < qua_number_year:
                        first_pra_time = ""
                else:
                    first_pra_time = ""

                if qua_time and qua_time != "":
                    if  qua_time_year < qua_number_year:
                        qua_time = ""
                    elif first_pra_time and first_pra_time != "":
                        if qua_time_year > first_pra_time_year:
                            qua_time = ""
                else:
                    qua_time = ""

                if first_pra_time and first_pra_time != "":
                    years = 2018 - first_pra_time_year + 1
                else:
                    years = ""
            else:
                qua_number = ""   #qua_number为空时，qua_time没有意义
                qua_time = ""   #qua_number为空时，qua_time没有意义

                # first_pra_time不为空时，以first_pra_time为准，计算years 、birth_date。
                if first_pra_time and first_pra_time != "":
                    years = 2018 - first_pra_time_year + 1
                else:
                    first_pra_time = ""
                    years = ""

                if birth_date and birth_date != "" :
                    if first_pra_time and first_pra_time != "":
                        if first_pra_time_year - birth_date_year < 18:
                            birth_date = ""
                else :
                    birth_date = ""
            return (pra_number, birth_date, first_pra_time, qua_number, qua_time ,years)

        else:

            if first_pra_time and first_pra_time != "" :   #首次执业时间不为空
                if first_pra_time_year - pra_number_year < 0 and first_pra_time_year > 2018:
                    first_pra_time = str(pra_number_year)
            else:
                first_pra_time = str(pra_number_year)

            first_pra_time_year = int(first_pra_time[:4])

            if birth_date and birth_date != "":
                if pra_number_year - birth_date_year < 18:
                    birth_date = ""
            else:
                birth_date = ""


            years = 2018 - first_pra_time_year + 1

            if qua_time and qua_time != "" and qua_number and qua_number != "":  #资格证获取时间判断
                    if qua_number_year > qua_time_year or qua_time_year > first_pra_time_year:
                        qua_time = ""
            else:
                qua_time = ""

            return (pra_number, birth_date, first_pra_time, qua_number, qua_time, years)


    results = df.map(lambda x:get_results(x))

    # print "+++++++++++++++++++++" + str(results.count())
    # results.foreach(p2)
    # return (pra_number, birth_date, first_pra_time, qua_number, qua_time, years)
    schema = StructType([StructField("pra_number", StringType(), False),
                         StructField("birth_date", StringType(), True),
                         StructField("first_pra_time", StringType(), True),
                         StructField("qua_number", StringType(), True),
                         StructField("qua_time", StringType(), True),
                         StructField("years", StringType(), True)
                         ])

    f = sqlContext.createDataFrame(results, schema=schema)
    # , mode = "overwrite"
    # useUnicode = true & characterEncoding = utf8，指定写入mysql时的数据编码，否则会乱码。
    f.write.jdbc(url='jdbc:mysql://cdh5-slave2:3306/laws_doc_lawyers_new?useUnicode=true&characterEncoding=utf8', table='hht_lawyer_12348gov_v3_time_result',properties={"user": "weiwc", "password": "HHly2017."})

    sc.stop()