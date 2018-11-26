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
    lawyers = sqlContext.read.jdbc(url='jdbc:mysql://cdh5-slave2:3306/laws_doc_lawyers_new', table='(select * from hht_lawyer_all_collect_add where pra_number in (select pra_number from hht_lawyer_all_collect_add group by pra_number,name,org_name having(count(*) > 1))) tmp2',column='id',lowerBound=1,upperBound=45326,numPartitions=1,properties={"user": "weiwc", "password": "HHly2017."})
    # lawyer_info = sqlContext.read.jdbc(url='jdbc:mysql://cdh-slave1:3306/laws_doc_lawyers', table='(select * from lawyer_info) tmp',column='id',lowerBound=1,upperBound=305694,numPartitions=8,properties={"user": "root", "password": "root"})
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
        print x
        print type(x[0]),type(x[1]),type(x[2])
        print x[0],x[1],x[2]
    def p_(x):
        # print type(x)
        print type(x)
        print type(x[0]),type(x[1])
        print x[0],x[1]

    def get_results(x):
        name = ""
        pra_number = ""
        org_name = ""
        age = ""
        area = ""
        birth_date = ""
        biyexueyuan = ""
        city = ""
        edu_origin = ""
        first_pra_time = ""
        gender = ""
        id_num = ""
        mail = ""
        nation = ""
        org_identity = ""
        phone = ""
        politics = ""
        practicestatus = ""
        pra_course = ""
        pra_type = ""
        province = ""
        qua_number = ""
        qua_time = ""
        xuewei = ""
        zhuanye = ""
        years = ""
        for i in x[1]:
            name = (name if (name != "") else i.name)
            pra_number = (pra_number if (pra_number != "") else i.pra_number)
            org_name = (org_name if (org_name != "") else i.org_name)
            age = (age if (age != "") else i.age)
            area = (area if (area != "") else i.area)
            birth_date = (birth_date if (birth_date != "") else i.birth_date)
            biyexueyuan = (biyexueyuan if (biyexueyuan != "") else i.biyexueyuan)
            city = (city if (city != "") else i.city)
            edu_origin = (edu_origin if (edu_origin != "") else i.edu_origin)
            first_pra_time = (first_pra_time if (first_pra_time != "") else i.first_pra_time)
            gender = (gender if (gender != "") else i.gender)
            id_num = (id_num if (id_num != "") else i.id_num)
            mail = (mail if (mail != "") else i.mail)
            nation = (nation if (nation != "") else i.nation)
            org_identity = (org_identity if (org_identity != "") else i.org_identity)
            phone = (phone if (phone != "") else i.phone)
            politics = (politics if (politics != "") else i.politics)
            practicestatus = (practicestatus if (practicestatus != "") else i.practicestatus)
            pra_course = (pra_course if (pra_course != "") else i.pra_course)
            pra_type = (pra_type if (pra_type != "") else i.pra_type)
            province = (province if (province != "") else i.province)
            qua_number = (qua_number if (qua_number != "") else i.qua_number)
            qua_time = (qua_time if (qua_time != "") else i.qua_time)
            xuewei = (xuewei if (xuewei != "") else i.xuewei)
            zhuanye = (zhuanye if (zhuanye != "") else i.zhuanye)
            years = (years if (years != "") else i.years)
        return (name,pra_number,org_name,age,area,birth_date,biyexueyuan,city,edu_origin,first_pra_time,gender,id_num,mail,nation,org_identity,phone,politics,practicestatus,pra_course,pra_type,province,qua_number,qua_time,xuewei,zhuanye,years)

    lawyers_kv = lawyers.map(lambda x:x).map(lambda x:(x[1]+"||"+x[2]+"||"+x[3],x))
    lawyers_result = lawyers_kv.groupByKey().map(lambda x:get_results(x))
    # lawyer_info_kv.foreach(p)
    # print lawyer_info_kv.count()

    # result = lawyers_kv.fullOuterJoin(lawyer_info_kv).map(lambda x:x[1]).map(lambda x:get_result(x)).cache()
    # result1 = result.filter(lambda x: False if x[0] == 0 else True)
    # result2 = result.filter(lambda x: True if x[0] == 0 else False).map(lambda x:(x[0],x)).groupByKey().flatMap(lambda x:get_results(x[1]))
    # result_all = result1.union(result2)

    # print "==================result1" + str(result1.count())
    # print "==================result2" + str(result2.count())
    # print "==================id_count0" + str(id_count0.value)
    # print "==================id_count" + str(id_count.value)
    # print "==================id_count1" + str(id_count1.value)
    # print "==================id_count2" + str(id_count2.value)


    schema = StructType([
        StructField("name", StringType(), False),
        StructField("pra_number", StringType(), False),
        StructField("org_name", StringType(), False),
        StructField("age", StringType(), True),
        StructField("area", StringType(), True),
        StructField("birth_date", StringType(), True),
        StructField("biyexueyuan", StringType(), True),
        StructField("city", StringType(), True),
        StructField("edu_origin", StringType(), True),
        StructField("first_pra_time", StringType(), True),
        StructField("gender", StringType(), True),
        StructField("id_num", StringType(), True),
        StructField("mail", StringType(), True),
        StructField("nation", StringType(), True),
        StructField("org_identity", StringType(), True),
        StructField("phone", StringType(), True),
        StructField("politics", StringType(), True),
        StructField("practicestatus", StringType(), True),
        StructField("pra_course", StringType(), True),
        StructField("pra_type", StringType(), True),
        StructField("province", StringType(), True),
        StructField("qua_number", StringType(), True),
        StructField("qua_time", StringType(), True),
        StructField("xuewei", StringType(), True),
        StructField("zhuanye", StringType(), True),
        StructField("years", IntegerType(), True)
    ])

    f = sqlContext.createDataFrame(lawyers_result, schema=schema)
    # f.show()
    # , mode = "overwrite"
    # useUnicode = true & characterEncoding = utf8，指定写入mysql时的数据编码，否则会乱码。
    f.write.jdbc(url='jdbc:mysql://cdh5-slave2:3306/laws_doc_lawyers_new?useUnicode=true&characterEncoding=utf8', table='hht_lawyer_all_collect_add_distinct',properties={"user": "weiwc", "password": "HHly2017."})

    sc.stop()