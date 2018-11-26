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
    lawyer_info = sqlContext.read.jdbc(url='jdbc:mysql://cdh5-slave3:3306/law', table='(select id,province,city,full_uid from province_city_full_uid) tmp',column='id',lowerBound=1,upperBound=501,numPartitions=1,properties={"user": "weiwc", "password": "HHly2017."})
    lawyers = sqlContext.read.jdbc(url='jdbc:mysql://cdh5-slave3:3306/law', table='(select id,law_id,area,title_short from law_rule_result2_add_article) tmp2',column='id',lowerBound=609664,upperBound=624400,numPartitions=1,properties={"user": "weiwc", "password": "HHly2017."})

    def p(x):
        print type(x)
        print type(x[0]),type(x[1]),type(x[2])
        print x[0],x[1],x[2]


    def get_area_uid(x):
        law_uid= str(x[0])
        area= x[1]
        title_short = x[2]
        # (u'\u798f\u5efa\u7701',
        #  [(None, u'24'), (u'\u8386\u7530\u5e02', u'24||24008'), (u'\u9f99\u5ca9\u5e02', u'24||24009'),
        #   (u'\u53a6\u95e8\u5e02', u'24||24003'), (u'\u6cc9\u5dde\u5e02', u'24||24005'),
        #   (u'\u5357\u5e73\u5e02', u'24||24002'), (u'\u4e09\u660e\u5e02', u'24||24001'),
        #   (u'\u6f33\u5dde\u5e02', u'24||24006'), (u'\u5b81\u5fb7\u5e02', u'24||24004'),
        #   (u'\u798f\u5dde\u5e02', u'24||24007')])

        for i in lawyer_b.value:
            if area not in i[0]:
                continue
            else:
                f_uid = ""
                for j in i[1]:
                    if j[0] is not None:
                        if j[0].replace(u"地区","").replace(u"新区","").rstrip(u"市区县") in title_short:
                            return (law_uid,j[1],i[0],j[0])
                    else:
                        f_uid = j[1]
                return (law_uid,f_uid,i[0],None)

            #注意：如果跳过if和else后，该条记录系统并非舍弃，而是默认返回None！！，因此需要自己使用filter进行过滤！！！！！

    def get_results(x):
        s = []
        for i in x[1]:
            s.append(i)
        return (x[0],s)

    lawyer_info_kv = lawyer_info.map(lambda x: (x[1],(x[2],x[3]))).groupByKey().map(lambda x:get_results(x)).collect()
    lawyer_b = sc.broadcast(lawyer_info_kv)

    result = lawyers.map(lambda x:(x[1],x[2],x[3])).map(lambda x:get_area_uid(x)).filter(lambda x:False if x is None else True)

    schema = StructType([
        StructField("law_uid", StringType(), False),
        StructField("area_uid", StringType(), True),
        StructField("province", StringType(), True),
        StructField("city", StringType(), True)
    ])
    # result.count()
    f = sqlContext.createDataFrame(result, schema=schema)
    # c = result.count()

    # f.show()
    # , mode = "overwrite"
    # d = result.collect()
    # useUnicode = true & characterEncoding = utf8，指定写入mysql时的数据编码，否则会乱码。
    f.write.jdbc(url='jdbc:mysql://cdh5-slave3:3306/law?useUnicode=true&characterEncoding=utf8', table='law_area_uid_add',properties={"user": "weiwc", "password": "HHly2017."})

    sc.stop()