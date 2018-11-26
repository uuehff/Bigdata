#coding=utf-8
import pymongo
from pykafka import KafkaClient
import codecs
import logging
logging.basicConfig(level = logging.INFO)

client = KafkaClient(hosts = "cdh-master-slave1:9092")

#生产kafka数据，通过字符串形式
def produce_kafka_data(kafka_topic, msg='{"id":"1", "data":["300.00", "1000"]}'):
    with kafka_topic.get_sync_producer() as producer:
        producer.produce(str(msg).encode('utf-8'))
#'{id :  question' + str(i) + '}'
#'test message' + str(i ** 2)
#消费kafka数据
def consume_simple_kafka(kafka_topic, timeout):
    consumer = kafka_topic.get_simple_consumer(consumer_timeout_ms = timeout)
    for message in consumer:
        if message is not None:
            print message.offset, message.value + "hello"

topic_in = client.topics['test_in3']
topic_out = client.topics['test_out3']

'''
query = [u'\u5f20\u67d0', u'\u8fdb\u5165', u'\u6c11\u5b85', u'\u5077\u7a83', u'\uff0c', u'\u88ab', u'\u4e3b\u4eba', u'\u53d1\u73b0', u'\u540e', u'\u4e0e', u'\u5176', u'\u4ea7\u751f', u'\u51b2\u7a81', u'\uff0c', u'\u5e76', u'\u7528', u'\u5229\u5668', u'\u628a', u'\u5176', u'\u6253', u'\u6210', u'\u91cd\u4f24', u'\u3002', u'\u672c\u6b21', u'\u5f20\u67d0', u'\u7a83\u53d6', '1000', u'\u5143', u'\u4eba\u6c11\u5e01', u'\u548c', u'\u624b\u673a', u'\u4e00', u'\u90e8', u'\u3002']
mongo_client = pymongo.MongoClient('mongodb://192.168.10.219:49019/')
bi = mongo_client.lawbot.bm25_inverted

BOW = {}
for word in query:
    BOW[word] = BOW.get(word, 0) + 1
uni_words = set(query)
inverted_list = []
for word in uni_words:
    inverted_data = bi.find_one({'key':word})
    if inverted_data and len(inverted_data.get('value')) < 20000:
        inverted_list.append(inverted_data)
'''
produce_kafka_data(topic_in)
consume_simple_kafka(topic_out,-1)
