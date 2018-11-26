#coding=utf-8

"""
 Counts words in UTF8 encoded, '\n' delimited text received from the network every second.
 Usage: kafka_wordcount.py <zk> <topic>

 To run this on your local machine, you need to setup Kafka and create a producer first, see
 http://kafka.apache.org/documentation.html#quickstart

 and then run the example
    `$ bin/spark-submit --jars \
      external/kafka-assembly/target/scala-*/spark-streaming-kafka-assembly-*.jar \
      examples/src/main/python/streaming/kafka_wordcount.py \
      localhost:2181 test`
"""
from __future__ import print_function

import sys
from pykafka import KafkaClient
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils,Broker,KafkaMessageAndMetadata,OffsetRange,TopicAndPartition
# KafkaUtils类
# http://spark.apache.org/docs/1.6.0/api/python/pyspark.streaming.html#module-pyspark.streaming.kafka

def updateFun(values, preState):

    if preState is None:
        return sum(values)
    else:
        return sum(values) + int(preState)

def transFun(x):
    return x.map(lambda x:(x,1))


def reduceFun(x,y):
    return x+y

def trans2(rdd):

    result = rdd.map(lambda x:(x[1],x[0])).sortByKey(ascending=False).map(lambda x:(x[1],x[0]))
    # result = rdd.map(lambda x:(x[1],x[0])).sortByKey(ascending=False).map(lambda x:x[1])
    return result

def sendData(x):
    client = KafkaClient(hosts="cdh-slave2:9092", zookeeper_hosts="cdh-master:2181")
    topic = client.topics['test_in22']
    with topic.get_sync_producer() as producer:
        producer.produce(x[0].encode("utf-8") + "," + str(x[1]))

import json
def foreachFun(rdd):
    if rdd: #以下三种方式写出,注意（k,v）对应（unicode,int）需转化为 （str,str）,produce()才能写出！使用json.dumps转化！
        # rdd.foreachPartition(lambda x:sendData(x))
        # rdd.foreach(lambda x:sendData(x))
        s = json.dumps(rdd.take(4))  #[(u'haha',1),(u'heihei',1)] ——>(str) '[["haha", 1], ["heihei", 1]]'
        client = KafkaClient(hosts="cdh-slave2:9092", zookeeper_hosts="cdh-master:2181")
        topic = client.topics['test_in22']
        with topic.get_sync_producer() as producer:     #可使用异步生产方式！
            producer.produce(s)
    # [["a", 1], ["we", 1], ["ads", 1]]
    # [["a", 1], ["we", 1], ["ads", 1]]
    # [["a", 1], ["we", 1], ["ads", 1]]
    # [["a", 4], ["qw", 2], ["qwq", 1]]
    # [["a", 4], ["qw", 2], ["we", 1]]
    # [["a", 4], ["qw", 2], ["we", 1]]
    # [["we", 1], ["ew", 1], ["w", 1]]

# 测试：
# kafka-console-producer --broker-list cdh-slave2:9092 --topic test_in21
# kafka-console-consumer --zookeeper cdh-master:2181  --topic test_in22 --from-beginning

if __name__ == "__main__":
    # if len(sys.argv) != 3:
    #     print("Usage: kafka_wordcount.py <zk> <topic>", file=sys.stderr)
    #     exit(-1)

    sc = SparkContext(appName="wc002")
    sc.setLogLevel("ERROR")

    ssc = StreamingContext(sc, 5)
    ssc.checkpoint("hdfs://cdh-master:8020/checkpoint")     #提交任务的用户要有目录的读写权限！

# =====================================================================createStream方式：
    #createStream()参数：ssc, zkQuorum, groupId, topics, kafkaParams = None,storageLevel = StorageLevel.MEMORY_AND_DISK_SER_2,keyDecoder = utf8_decoder, valueDecoder = utf8_decoder

    zkQuorum = "cdh-master:2181,cdh-slave1:2181,cdh-slave2:2181"    #(hostname:port,hostname:port,..)
    topic = {"test_in21":3}        # Dict of (topic_name -> numPartitions)，numPartitions指要读取每个topic的个数！

    # ds = KafkaUtils.createStream(ssc, zkQuorum, "id_01", topics=topic)  #ds类型：  (None, u'dddddddddd')
    # ds2 = KafkaUtils.createStream(ssc, zkQuorum, "id_02", topics=topic2)  #ds类型：  (None, u'dddddddddd')
    # join_ds = ds.union(ds2).map(lambda  x: x[1])
    # lines = ds.map(lambda x: x[1]).map(lambda w: (w,1))
    # lines = ds.map(lambda x: x[1])
    # lines2 = ds2.map(lambda x: x[1])
    # lines.pprint()

#=====================================================================createDirectStream方式：
    # createDirectStream()参数：ssc, topics, kafkaParams, fromOffsets = None,keyDecoder = utf8_decoder, valueDecoder = utf8_decoder,messageHandler = None

    brokers = "cdh-slave2:9092,cdh-slave1:9092"
    ds = KafkaUtils.createDirectStream(ssc, ["test_in21"], {"metadata.broker.list": brokers})

    lines = ds.map(lambda x:x[1]).flatMap(lambda x:x.split(" ")).map(lambda w:(w,1))
    # lines.pprint()

    #updateStateByKey操作===================
    # updateDS = lines.updateStateByKey(lambda x,y:updateFun(x,y))
    # 每隔5秒统计下截止目前的所有数据中，找出频率最高的前三个词！
    updateDS = lines.updateStateByKey(lambda x,y:updateFun(x,y)).transform(trans2).foreachRDD(foreachFun)
    # updateDS.pprint()

    # transform操作=====================
    # trans = lines.transform(lambda x:transFun(x))
    # trans.pprint()

    #windows操作=====================

    # winDS = lines.window(10,5)  #参数分别对应截取RDD的个数和位置。
    # winDS.pprint()

    #每隔5秒统计下前15秒的数据中，找出出现频率最高的前三个词！
    # reduceDS = lines.reduceByKeyAndWindow(reduceFun,reduceFun,15,5).transform(trans2).foreachRDD(foreachFun)

    # lines.reduceByWindow()
    # reduceByKeyAndWindow理解： http: // humingminghz.iteye.com / blog / 2308138
    # http: // humingminghz.iteye.com / blog / 2308231
    # reduceByKeyAndWindow应用： http://blog.csdn.net/accptanggang/article/details/53081393
    # winDS = lines.reduceByKeyAndWindow(reduceFun,reduceFun,10,5)
    # winDS = lines.groupByKeyAndWindow(10,5)



    ssc.start()
    ssc.awaitTermination()