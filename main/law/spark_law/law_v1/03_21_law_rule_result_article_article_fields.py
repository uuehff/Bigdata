# -*- coding: utf-8 -*-

from  pyspark import SparkContext,SparkConf
from pyspark.sql import SQLContext
from pyspark.sql.types import *
import re

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
    df = sqlContext.read.jdbc(url='jdbc:mysql://cdh5-slave3:3306/law', table='(select id,article from law_rule_result_article ) tmp',column='id',lowerBound=1,upperBound=624401,numPartitions=90,properties={"user": "weiwc", "password": "HHly2017."})
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
    # def p2(x):
    #     k,v = x[0],x[1]
    #     print k,
    #     # print type(v)
    #     for i2 in v:
    #         print i2,
    #     print "\n"
    def get_results(x):
        id = x[0]
        article = []
        if x[1] and x[1] != "":
            for i in x[1].split("<br/>"):
                article.append(i.split(u"关联法规")[0])
        return (id,"<br/>".join(article))


    results = df.map(lambda x:x).map(lambda x:get_results(x))

    schema = StructType([StructField("id", IntegerType(), False),
                         StructField("article", StringType(), True)])

    f = sqlContext.createDataFrame(results, schema=schema)
    # , mode = "overwrite"
    # useUnicode = true & characterEncoding = utf8，指定写入mysql时的数据编码，否则会乱码。
    f.write.jdbc(url='jdbc:mysql://cdh5-slave3:3306/law?useUnicode=true&characterEncoding=utf8', table='law_rule_result2_article_article_fields',properties={"user": "weiwc", "password": "HHly2017."})

    sc.stop()