# -*- coding: utf-8 -*-

from  pyspark import SparkContext,SparkConf
from pyspark.sql import SQLContext
from pyspark.sql.types import *
import os
import time

import re
if __name__ == "__main__":

    conf = SparkConf()
    sc = SparkContext(conf=conf)
    sqlContext = SQLContext(sc)

    # PYSPARK_PYTHON = "C:\\Python27\\python.exe"    #多版本python情况下，需要配置这个变量指定使用哪个版本
    # os.environ["PYSPARK_PYTHON"] = PYSPARK_PYTHON

    def p(x):
        print type(x),type(x[0]),type(x[1])
        # print type(x)
        # print type(x[0]),type(x[1])
        # print x[0],x[1][0],x[1][1]

    def filter_(casedate):
        if casedate and casedate != '':       #过滤掉数据库中，lawlist为Null或''的行。
            try:
                time.strptime(casedate, "%Y-%m-%d")
                return False
            except:
                return True
        else:
            return False

    # judgment_new：556万,3030306	3392975
    df = sqlContext.read.jdbc(url='jdbc:mysql://cdh-slave1:3306/civil',
                               table='(select id,casedate from judgment_civil_all  ) tmp',
                               column='id', lowerBound=1, upperBound=11295123, numPartitions=100,
                               properties={"user": "weiwc", "password": "HHly2017."})


    # acc = sc.accumulator(0)
    # print "df.count()======================" + str(df.count())
    uuid_reason = df.map(lambda x:filter_(x[1])).count()    #title_trial_process
    print "======================uuid_reason : " + str(uuid_reason)

    sc.stop()