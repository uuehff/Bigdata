#coding=utf-8
from pykafka import KafkaClient


def simple_consumer_kafka(topic, timeout):
    # print topic.partitions
    #{0: <pykafka.partition.Partition at 0x381a550L (id=0)>, 1: <pykafka.partition.Partition at 0x381ab00L (id=1)>, 2: <pykafka.partition.Partition at 0x381a908L (id=2)>}
    # print topic.partitions.values()
    #[<pykafka.partition.Partition at 0x381a550L (id=0)>, <pykafka.partition.Partition at 0x381ab00L (id=1)>, <pykafka.partition.Partition at 0x381a908L (id=2)>]

    p = topic.partitions.values()[:2]  #[:2]代表0,1两个分区数据！
    # consumer = topic.get_simple_consumer(consumer_timeout_ms = timeout) #默认是全部分区！
    consumer = topic.get_simple_consumer(consumer_timeout_ms = timeout,partitions=p) #p参数必须是列表！
    for message in consumer:
        if message is not None:
            print message.offset, message.value + "======!"
    consumer.stop()


#消费kafka数据，可以指定分区
def balanced_consumer_kafka(topic,timeout):
    p = topic.partitions.values()[0]  # [0]代表0分区数据！
    # get_balanced_consumer没有partitions参数
    consumer = topic.get_balanced_consumer(consumer_group="defaultgroup",zookeeper_connect="cdh-master:2181",consumer_timeout_ms = timeout) #p参数必须是列表！
    for message in consumer:
        if message is not None:
            print message.offset, message.value + "======!"
    consumer.stop()


client = KafkaClient(hosts = "cdh-slave2:9092,cdh-slave1:9092",zookeeper_hosts="cdh-master:2181,cdh-slave1:2181,cdh-slave2:2181")
topic = client.topics['test_in21']

simple_consumer_kafka(topic,-1)

# balanced_consumer_kafka(topic,-1)
