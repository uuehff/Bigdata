#coding=utf-8
# 创建console_data_in话题和streaming_data_out话题，控制台模拟生产者和消费者。kafka-console-producer写入信息到console_data_in分区，
# SparkStreaming读取该分区，处理后，将结果写入streaming_data_out分区。供控制台kafka-console-consumer消费。
# kafka-topics --create --zookeeper cdh-master-slave1:2181  --replication-factor 1 --partitions 1 --topic console_data_in
# kafka-topics --create --zookeeper cdh-master-slave1:2181  --replication-factor 1 --partitions 1 --topic streaming_data_out
#
# kafka-console-producer --broker-list cdh-master-slave1:9092 --topic console_data_in
# kafka-console-consumer --zookeeper cdh-master-slave1:2181  --bootstrap-server cdh-master-slave1:9092 --topic streaming_data_out --from-beginning
#
# 直接使用控制台消费，消费控制台的生产。
# kafka-console-consumer --zookeeper cdh-master-slave1:2181  --bootstrap-server cdh-master-slave1:9092 --topic console_data_in --from-beginning


from pykafka import KafkaClient
import codecs
import logging
logging.basicConfig(level = logging.INFO)

client = KafkaClient(hosts = "cdh-master-slave1:9092,cdh-slave2:9092,cdh-slave3:9092")


def produce_kafka_data(kafka_topic):
    with kafka_topic.get_sync_producer() as producer:
        for i in range(4):
            # produce方法中，生产kafka的数据，是str(字符串)类型
            producer.produce('test message' + str(i ** 2))

#消费kafka数据
def consume_simple_kafka(kafka_topic, timeout):
    consumer = kafka_topic.get_simple_consumer(consumer_timeout_ms = timeout)
    for message in consumer:
        if message is not None:
            print message.offset, message.value + " hello"

# topic = client.topics['test_in3']
topic2 = client.topics['console_data_in']
# produce_kafka_data(topic)
consume_simple_kafka(topic2,-1)
