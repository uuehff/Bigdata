 # -*- coding: utf-8 -*-
#import findspark
#findspark.init("/opt/cloudera/parcels/CDH-5.10.1-1.cdh5.10.1.p0.10/lib/spark/")
import sys
from pyspark.sql import SQLContext
from pyspark import SparkContext,SparkConf
conf = SparkConf().setAppName('weiwc-sort').setMaster("spark://cdh-master-slave1:7077").set("spark.executor.memory", "5G").set("spark.executor.cores","2").set("spark.cores.max","6").set("spark.shuffle.io.maxRetrie","8").set("spark.shuffle.io.retryWait","5s")
#conf = SparkConf()
#conf = SparkConf().setAppName('test').set("spark.shuffle.file.buffer","64k").set("spark.shuffle.io.maxRetries","5").set("spark.shuffle.io.retryWait","4s")

sc = SparkContext(conf=conf)

#sc.setLogLevel("DEBUG")
data = sc.textFile("/user/weiwc/data/t1.txt",3)
data.glom().collect()
m1 = data.groupBy(lambda x: x.split(" ")[0],2).cache()
m1.saveAsTextFile(sys.argv[1])

#sc.setLogLevel("DEBUG") # ALL, DEBUG, ERROR, FATAL, INFO, OFF, TRACE, WARN
#sc.setLogLevel("WARN")
#sqlContext = SQLContext(sc)
# create and load dataframe from MongoDB URI
#df = sqlContext.read.format("com.mongodb.spark.sql.DefaultSource")\
#                    .option("spark.mongodb.input.uri", "mongodb://192.168.10.219:49019/lawbot.bm25_doc")\
#                    .load()
# print data frame schema
#df.printSchema()
# print first dataframe row
#df.first()

#df.filter(df["key"]=="诈骗").show()
