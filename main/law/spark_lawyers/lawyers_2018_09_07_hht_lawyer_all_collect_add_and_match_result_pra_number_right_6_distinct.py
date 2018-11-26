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
    # lawyers = sqlContext.read.jdbc(url='jdbc:mysql://cdh5-slave2:3306/laws_doc_lawyers_new', table='(select * from hht_lawyer_all_collect_add where pra_number in (select pra_number from hht_lawyer_all_collect_add group by pra_number,name,org_name having(count(*) > 1))) tmp2',column='id',lowerBound=1,upperBound=45326,numPartitions=1,properties={"user": "weiwc", "password": "HHly2017."})
    lawyers = sqlContext.read.jdbc(url='jdbc:mysql://cdh5-slave2:3306/laws_doc_lawyers_new', table='(select * from hht_lawyer_all_collect_match_result_right_6_distinct ) tmp2',column='id',lowerBound=1,upperBound=386161,numPartitions=2,properties={"user": "weiwc", "password": "HHly2017."})
    # lawyers = sqlContext.read.jdbc(url='jdbc:mysql://cdh5-slave2:3306/laws_doc_lawyers_new', table='(select * from hht_lawyer_all_collect_match_result_pra_number_part_group where id in (327245,299895,147691,183256) ) tmp2',column='id',lowerBound=1,upperBound=386161,numPartitions=6,properties={"user": "weiwc", "password": "HHly2017."})
    pra_numbers = sqlContext.read.jdbc(url='jdbc:mysql://cdh5-slave2:3306/laws_doc_lawyers_new', table='(select id,pra_number from zy_lawyer_12348gov_pra_number ) tmp2',column='id',lowerBound=1,upperBound=298266,numPartitions=1,properties={"user": "weiwc", "password": "HHly2017."})
    # lawyer_info = sqlContext.read.jdbc(url='jdbc:mysql://cdh-slave1:3306/laws_doc_lawyers', table='(select * from lawyer_info) tmp',column='id',lowerBound=1,upperBound=305694,numPartitions=6,properties={"user": "root", "password": "root"})
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
    def p_(x):
        # print type(x)
        print type(x)
        print type(x[0]),type(x[1])
        print x[0],x[1]


    def get_row_result(r1, r2,org_names,pra_json_value):
        if r1.pra_course and r1.pra_course != "" and r2.org_name in r1.pra_course:
                org_names.append(r2.org_names)
                return r1,org_names
        elif r2.pra_course and r2.pra_course != "" and r1.org_name in r2.pra_course :
                org_names.append(r1.org_names)
                return r2,org_names
        elif r1.practicestatus == u"注销" and r2.practicestatus != u"注销":
            org_names.append(r1.org_names)
            return r2,org_names
        elif r1.practicestatus != u"注销" and r2.practicestatus == u"注销":
            org_names.append(r2.org_names)
            return r1,org_names
        elif r1.practicestatus == u"正常执业" and r2.practicestatus != u"正常执业":
            org_names.append(r2.org_names)
            return r1,org_names
        elif r1.practicestatus != u"正常执业" and r2.practicestatus == u"正常执业":
            org_names.append(r1.org_names)
            return r2,org_names
        elif pra_json_value.has_key(r1.pra_number):
            org_names.append(r2.org_names)
            return r1,org_names
        elif pra_json_value.has_key(r2.pra_number):
            org_names.append(r1.org_names)
            return r2,org_names
        else:
            org_names.append(r2.org_names)
            return r1,org_names

    def get_results(x):

        def min(a, b):
            return a if a <= b else b

        pra_json_value = pra_json_broad.value
        org_names = []
        rows = []
        for j in x[1]:
            rows.append(j)

        i = rows[0]  #定义一个初始值，直接定义为字符串会包报类型错误
        phone = i.phone
        qua_number = i.qua_number
        first_pra_time = i.first_pra_time
        years = i.years

        # 取出执业证号中，首次执业时间不一样的时间（省内跨所一般首次执业时间不变，省外跨所一般不一样），取最小值，进行执业年限的处理。
        if rows and len(rows) == 2:
            i,org_names =  get_row_result(rows[0],rows[1],org_names,pra_json_value)
            phone = i.phone
            qua_number = i.qua_number

            years = min(int(rows[0].pra_number[5:9]),int(rows[1].pra_number[5:9]))
            first_pra_time = years
            years = 2019 - years

        elif rows and len(rows) == 3:
            r1,org_names =  get_row_result(rows[0], rows[1],org_names,pra_json_value)
            i,org_names = get_row_result(r1,rows[2],org_names,pra_json_value)
            phone = i.phone
            qua_number = i.qua_number
            years = min(min(int(rows[0].pra_number[5:9]), int(rows[1].pra_number[5:9])),int(rows[2].pra_number[5:9]))
            first_pra_time = years
            years = 2019 - years

        #合并phone，当最终返回的row中，phone为空时，进行分组内的phone合并
        if phone is None or phone == "":
            for p in rows:
                phone = p.phone
                if phone and phone != "":
                    break
        # 合并qua_number，当最终返回的row中，qua_number为空时，进行分组内的qua_number合并
        if qua_number is None or qua_number == "":
            for p in rows:
                qua_number = p.qua_number
                if qua_number and qua_number != "":
                    break

        org_names.append(i.org_name)
        org_names.append(i.org_names)
        org_names_distinct = []
        for s in org_names:
            for ss in s.split("||"):
                org_names_distinct.append(ss)

        org_names = list(set(org_names_distinct))

        # id, name, pra_number, org_name, area, birth_date, biyexueyuan, city, edu_origin, first_pra_time, \
        # gender, id_num, mail, nation, org_identity, phone, politics, practicestatus, pra_course, pra_type, \
        # province, qua_number, qua_time, xuewei, zhuanye, \
        # years, source, years_not, first_pra_time_not, birth_date_not, pra_course_not, qua_number_not, qua_time_not,
        return (i.id,i.name,i.pra_number,i.org_name,i.area,i.birth_date,i.biyexueyuan,i.city,i.edu_origin,first_pra_time,
                i.gender,i.id_num,i.mail,i.nation,i.org_identity,phone,i.politics,i.practicestatus,i.pra_course,i.pra_type,
                i.province,qua_number,i.qua_time,i.xuewei,i.zhuanye,years,i.source,
                i.years_not,i.first_pra_time_not,i.birth_date_not,i.pra_course_not,i.qua_number_not,i.qua_time_not,"||".join(org_names))

    def get_kv(x):
        pra_number = x.pra_number
        k1 = pra_number[11:17]
        k2 = x.name
        k = k1 + k2
        return (k,x)


    def get_dict(x):
        return {x.pra_number:""}
    pra_numbers_dict =  pra_numbers.map(lambda x:get_dict(x)).collect()
    pra_json = {}
    for i in pra_numbers_dict:
        pra_json.update(i)
    pra_json_broad = sc.broadcast(pra_json)

    lawyers_kv = lawyers.map(lambda x:get_kv(x)).groupByKey()
    lawyers_result = lawyers_kv.map(lambda x:get_results(x))

    # return (
    # i.id, i.name, i.pra_number, i.org_name, i.area, i.birth_date, i.biyexueyuan, i.city, i.edu_origin,
    #  i.first_pra_time,
    # i.gender, i.id_num, i.mail, i.nation, i.org_identity, i.phone, i.politics, i.practicestatus, i.pra_course,
    # i.pra_type,
    # i.province, i.qua_number, i.qua_time, i.xuewei, i.zhuanye, i.years, i.source,
    # i.years_not, i.first_pra_time_not, i.birth_date_not, i.pra_course_not, i.qua_number_not, i.qua_time_not,
    # "||".join(org_names))

    schema = StructType([
        StructField("id", IntegerType(), False),
        StructField("name", StringType(), False),
        StructField("pra_number", StringType(), False),
        StructField("org_name", StringType(), False),
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
        StructField("years", IntegerType(), True),
        StructField("source", StringType(), True),
        StructField("years_not", StringType(), True),
        StructField("first_pra_time_not", StringType(), True),
        StructField("birth_date_not", StringType(), True),
        StructField("pra_course_not", StringType(), True),
        StructField("qua_number_not", StringType(), True),
        StructField("qua_time_not", StringType(), True),
        StructField("org_names", StringType(), True)
    ])
    f = sqlContext.createDataFrame(lawyers_result, schema=schema)
    # f.show()
    # , mode = "overwrite"
    # useUnicode = true & characterEncoding = utf8，指定写入mysql时的数据编码，否则会乱码。
    f.write.jdbc(url='jdbc:mysql://cdh5-slave2:3306/laws_doc_lawyers_new?useUnicode=true&characterEncoding=utf8', table='hht_lawyer_all_collect_match_result_right_6_distinct_result',properties={"user": "weiwc", "password": "HHly2017."})

    sc.stop()