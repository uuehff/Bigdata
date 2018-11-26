#coding=utf-8
from pykafka import KafkaClient
import codecs
import logging
logging.basicConfig(level = logging.INFO)

client = KafkaClient(hosts = "cdh-master-slave1:9092")

#生产kafka数据，通过字符串形式
def produce_kafka_data(kafka_topic):
    with kafka_topic.get_sync_producer() as producer:
        for i in range(4):
            producer.produce('{id :  question' + str(i) + '}')
#'{id :  question' + str(i) + '}'
#'test message' + str(i ** 2)
#消费kafka数据
def consume_simple_kafka(kafka_topic, timeout):
    consumer = kafka_topic.get_simple_consumer(consumer_timeout_ms = timeout)
    for message in consumer:
        if message is not None:
            print message.offset, message.value + " answered!"

topic_in = client.topics['test_in']
topic_out = client.topics['test_out']
produce_kafka_data(topic_in)
consume_simple_kafka(topic_out,-1)
