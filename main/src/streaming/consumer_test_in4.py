#coding=utf-8
from pykafka import KafkaClient
import codecs
import logging
import time
logging.basicConfig(level = logging.INFO)

client = KafkaClient(hosts = "cdh-master-slave1:9092,cdh-slave2:9092,cdh-slave3:9092")

#生产kafka数据，通过字符串形式
def produce_kafka_data(kafka_topic):
    with kafka_topic.get_sync_producer() as producer:
        for j in range(20):
            #time.sleep(0.1)
            for i in range(10):
                producer.produce('test message>>' + str(i ** 2))

#消费kafka数据
def consume_simple_kafka(kafka_topic, timeout):
    kafka_topic.get_balanced_consumer()
    consumer = kafka_topic.get_simple_consumer(consumer_timeout_ms = timeout)
    for message in consumer:
        if message is not None:
            print message.offset, message.value + "hello"

topic = client.topics['test_in4']
topic2 = client.topics['test_out3']
produce_kafka_data(topic)
consume_simple_kafka(topic,-1)
