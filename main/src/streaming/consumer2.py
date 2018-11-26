#coding=utf-8
from pykafka import KafkaClient
import codecs
import logging
import time
logging.basicConfig(level = logging.INFO)

client = KafkaClient(hosts = "cdh-master-slave1:9092,cdh-slave2:9092,cdh-slave3:9092")
client2 = KafkaClient(hosts = "cdh-slave3:9092")

query_json = '{"data": ["\\u5f20\\u67d0", "\\u8fdb\\u5165", "\\u6c11\\u5b85", "\\u5077\\u7a83", "\\uff0c", "\\u88ab", "\\u4e3b\\u4eba", "\\u53d1\\u73b0", "\\u540e", "\\u4e0e", "\\u5176", "\\u4ea7\\u751f", "\\u51b2\\u7a81", "\\uff0c", "\\u5e76", "\\u7528", "\\u5229\\u5668", "\\u628a", "\\u5176", "\\u6253", "\\u6210", "\\u91cd\\u4f24", "\\u3002", "\\u672c\\u6b21", "\\u5f20\\u67d0", "\\u7a83\\u53d6", "1000", "\\u5143", "\\u4eba\\u6c11\\u5e01", "\\u548c", "\\u624b\\u673a", "\\u4e00", "\\u90e8", "\\u3002"], "id": "1"}'

def produce_kafka_data(kafka_topic):
    with kafka_topic.get_sync_producer() as producer:
        for j in range(100):
            #time.sleep(0.1)
            for i in range(1):
                #producer.produce('test message>>' + str(i ** 2))
                producer.produce(query_json)

#消费kafka数据
def consume_simple_kafka(kafka_topic, timeout):
    consumer = kafka_topic.get_simple_consumer(consumer_timeout_ms = timeout)
    for message in consumer:
        if message is not None:
            print message.offset, message.value + "hello"

topic = client.topics['test_in3333']
topic2 = client2.topics['test_out3']
produce_kafka_data(topic)
consume_simple_kafka(topic2,-1)
