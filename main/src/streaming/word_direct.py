import sys
from pyspark.sql import SQLContext
from pyspark import SparkContext,SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

from pykafka import KafkaClient
import codecs
import logging
from kafka import KafkaProducer

def sendPartition(iter):
        record_list = []
        for record in iter:
            record_list.append(record)
        if record_list:
            topic = 'test_out3'
            producer = KafkaProducer(bootstrap_servers="cdh-slave3:9092")
            for record in record_list:
                producer.send(topic, str(record).encode('utf-8'))
            producer.close()


def sendPartition2(iter):
        topic = 'test_out3'
        producer = KafkaProducer(bootstrap_servers="cdh-master-slave1:9092,cdh-slave2:9092,cdh-slave3:9092")
        for record in iter:
            producer.send(topic, str(record).encode('utf-8'))
        producer.close()

def sendRDD(rdd):
        if not rdd.isEmpty():
            rdd.foreachPartition(sendPartition)
            #rdd.collect

if __name__ == "__main__":
    #conf = SparkConf().setMaster("spark://cdh-master-slave1:7077").set("spark.executor.memory", "14G").set("spark.driver.memory", "10G").set("spark.executor.cores","3").set("spark.cores.max","6").set("spark.dynamicAllocation.enabled", "false").set("spark.python.worker.reuse", "true").setAppName('bm25_cache')
    #conf = SparkConf().set("spark.memory.storageFraction","0.8")
    #conf = SparkConf().setMaster("spark://cdh-master-slave1:7077").set("spark.executor.memory", "6G").set("spark.driver.memory", "6G").set("spark.executor.cores","3").set("spark.cores.max","6").set("spark.python.worker.reuse", "true").setAppName('bm25_cache_worddirect')
    #conf = SparkConf().setMaster("spark://cdh-master-slave1:7077").set("spark.driver.memory", "6G").set("spark.executor.memory", "15G").set("spark.python.worker.reuse", "true").setAppName('bm25_cache_worddirect')
    conf = SparkConf().setMaster("spark://cdh-master-slave1:7077").set("spark.python.worker.reuse", "true").setAppName('bm25_cache_worddirect').set("spark.dynamicAllocation.enabled", "false").set("spark.executor.memory", "15G").set("spark.executor.cores","3")
    sc = SparkContext(conf=conf)
    ssc = StreamingContext(sc, 0.5)
    brokers, topic_in, topic_out = sys.argv[1:]
    kvs = KafkaUtils.createDirectStream(ssc, [topic_in], {"metadata.broker.list": brokers})
    lines = kvs.map(lambda x: x[1])  #再加不加map的pprint结果一样。
    lines.foreachRDD(lambda rdd: rdd.foreachPartition(sendPartition))
    #lines.foreachRDD(sendRDD)
    #lines.foreachRDD(lambda rdd: None  if rdd.isEmpty() else rdd.foreachPartition(sendPartition) )
#    lines.foreachRDD(lambda rdd: None  if rdd.isEmpty() else rdd.foreachPartition(sendPartition) )
   # lines.pprint() #执行完foreachRDD才会执行打印，它的时间可以理解是启动任务的间隔时间，当有任务时，foreachRDD也会占用时间，因此这时打印的时间间隔比真实时间间隔慢，因为它一直就是0.5毫秒。
    ssc.start()
    ssc.awaitTermination()
