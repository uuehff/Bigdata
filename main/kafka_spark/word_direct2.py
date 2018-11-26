#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""
 Counts words in UTF8 encoded, '\n' delimited text directly received from Kafka in every 2 seconds.
 Usage: direct_kafka_wordcount.py <broker_list> <topic>

 To run this on your local machine, you need to setup Kafka and create a producer first, see
 http://kafka.apache.org/documentation.html#quickstart

 and then run the example
    `$ bin/spark-submit --jars \
      external/kafka-assembly/target/scala-*/spark-streaming-kafka-assembly-*.jar \
      examples/src/main/python/streaming/direct_kafka_wordcount.py \
      localhost:9092 test`
"""

import sys
from pyspark.sql import SQLContext
from pyspark import SparkContext,SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

from pykafka import KafkaClient
import codecs
import logging
from kafka import KafkaProducer

#log = logging.getLogger(__name__)
#def sendPartition(iter):
        #client = KafkaClient(hosts = "cdh-master-slave1:9092")
#        topic_out = client.topics['test_out3']
        #producer.send(topic, str(msg).encode('utf-8'))
#way1:

      
#        topic = 'test_out4'
#        producer = KafkaProducer(bootstrap_servers="cdh-master-slave1:9092,cdh-slave2:9092,cdh-slave3:9092")
#        for record in iter:
#            producer.send(topic, str(record).encode('utf-8'))
#        producer.close()

#way2:

#def sendPartition(iter):
#        for record1 in iter:
#            topic = 'test_out4'
#            producer = KafkaProducer(bootstrap_servers="cdh-master-slave1:9092,cdh-slave2:9092,cdh-slave3:9092")
#            break
#        for record in iter:
#            producer.send(topic, str(record).encode('utf-8'))
#       producer.close() 
#way3:       


#        record_list = []
#        for record in iter:
#            record_list.append(record)
#        if record_list:
#            topic = 'test_out4'
#            producer = KafkaProducer(bootstrap_servers="cdh-master-slave1:9092,cdh-slave2:9092,cdh-slave3:9092")
#            for record in record_list:
#                producer.send(topic, str(record).encode('utf-8'))
#            producer.close()

def sendPartition(iter):
        for record1 in iter:
            topic = 'test_out3'
            producer = KafkaProducer(bootstrap_servers="cdh-master-slave1:9092,cdh-slave2:9092,cdh-slave3:9092")
            break
        for record in iter:
            producer.send(topic, str(record).encode('utf-8'))
        producer.close()

def sendRDD(rdd):
        if not rdd.isEmpty():
            rdd.foreachPartition(sendPartition)
            #rdd.collect

if __name__ == "__main__":
#    if len(sys.argv) != 2:
#        print("Usage: direct_kafka_wordcount.py <broker_list> <topic>", file=sys.stderr)
#        exit(-1)

    #conf = SparkCdnf().setAppName('weiwc-app-direct-wordcount').setMaster("spark://cdh-master-slave1:7077").set("spark.executor.memory", "3G").set("spark.driver.memory", "2G").set("spark.executor.cores","3").set("spark.cores.max","9")
    conf = SparkConf()
    sc = SparkContext(conf=conf)
    #sc = SparkContext(appName="PythonStreamingDirectKafkaWordCount")
    #sc.setLogLevel("DEBUG") # ALL, DEBUG, ERROR, FATAL, INFO, OFF, TRACE, WARN
    #sc.setLogLevel("INFO")

#    sqlContext = SQLContext(sc)
    #df = sqlContext.read.format("com.mongodb.spark.sql.DefaultSource")\
    #               .option("spark.mongodb.input.uri", "mongodb://192.168.10.219:49019/lawbot.bm25_doc")\
    #               .load()


#    df = sqlContext.sql("select * from salaries")
    #df = sqlContext.sql("CREATE TABLE employees (id int,name string,salary double) ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'")
    #df = sc.parallelize(['hello','world'])
    #df.printSchema()
#    mongo_data = df.first().toString
    
#    logging.basicConfig(level = logging.INFO)
#    client = KafkaClient(hosts = "cdh-master-slave1:9092")
#    def sendPartition(iter):
#        client = KafkaClient(hosts = "cdh-master-slave1:9092")
#        topic_out = client.topics['test_out3']
        #producer = topic_out.get_sync_producer()
        #producer = topic_out.get_producer()
        #mongo_client = pymongo.MongoClient('mongodb://192.168.10.219:49019/')
        #be = mongo_client.lawbot.bm25_extra
        #extra_data = be.find_one()
        #total_word = extra_data.get('total_word')
        #N = extra_data.get('N')
        #producer = topic_out.get_sync_producer()
        #producer.produce(str(record).encode('utf-8') for record in iter)
        #producer.produce(['test message>>>> ' + str(i ** 2) for i in range(4)])
#        for record in iter:
#            with topic_out.get_sync_producer(required_acks=0) as producer:
            #for record in iter:
#                producer.produce(str(record).encode('utf-8')) 
#            producer.stop()
        #for record in iter:
#                 producer.produce(bytes(str(record),encoding = "utf8"))
#                tmp = '(%s %s)' % (str(record[0]), str(record[1]))
             #   tmp = '(%s>>>)' % (str(record))
             #   producer.produce(tmp.encode('utf-8'))
#                producer.produce(tmp.encode('utf-8'))
#                producer.produce(bytes(str(record),encoding = "utf8"))
        
#def BM25_cores(query, total_word, N, k1=1.5, b=0.5, k3=0) 
#score = BM25_cores(query, total_word, N)
  
    ssc = StreamingContext(sc, 1)
    brokers, topic_in, topic_out = sys.argv[1:]
    kvs = KafkaUtils.createDirectStream(ssc, [topic_in], {"metadata.broker.list": brokers})
    lines = kvs.map(lambda x: x[1])  #再加不加map的pprint结果一样。
    lines.foreachRDD(lambda rdd:rdd.foreachPartition(sendPartition))
    #lines.foreachRDD(sendRDD)
    #lines.foreachRDD(lambda rdd: None  if rdd.isEmpty() else rdd.foreachPartition(sendPartition) )
#    lines.foreachRDD(lambda rdd: None  if rdd.isEmpty() else rdd.foreachPartition(sendPartition) )
   # lines.pprint() #执行完foreachRDD才会执行打印，它的时间可以理解是启动任务的间隔时间，当有任务时，foreachRDD也会占用时间，因此这时打印的时间间隔比真实时间间隔慢，因为它一直就是0.5毫秒。
#    counts = lines.flatMap(lambda line: line.split(" ")) \
#        .map(lambda word: (word, 1)) \
#        .reduceByKey(lambda a, b: a+b).foreachRDD(lambda rdd: rdd.foreachPartition(sendPartition))
#        .reduceByKey(lambda a, b: a+b).foreachRDD(lambda rdd: rdd.foreachPartition(sendPartition))

#    counts.pprint()

    ssc.start()
    ssc.awaitTermination()
