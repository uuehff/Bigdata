# -*- coding: utf-8 -*-

from pyspark import SparkContext,SparkConf
from pyspark.sql import SQLContext
import os

if __name__ == "__main__":

    PYSPARK_PYTHON = "C:\\Python27\\python.exe"    #多版本python情况下，需要配置这个变量指定使用哪个版本
    os.environ["PYSPARK_PYTHON"] = PYSPARK_PYTHON
    conf = SparkConf()
    sc = SparkContext(conf=conf)
    sqlContext = SQLContext(sc)
    r = sc.parallelize([1,2,3,4])
    print r.map(lambda x:(x,x)).collect()
