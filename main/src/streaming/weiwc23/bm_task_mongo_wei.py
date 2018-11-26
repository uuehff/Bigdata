# coding:utf-8
import json
import sys
import time
import functools
from operator import add
import logging
from collections import Counter
import heapq

reload(sys)
sys.setdefaultencoding('utf-8')

import pymongo
from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from pykafka import KafkaClient

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(filename)s %(funcName)s[line:%(lineno)d]%(levelname)s %(message)s', filename='logging.log', filemode='a')
lg = logging.getLogger('mylog')


def run_time(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        print '%s run time is:%s' % (func.__name__, time.time()-start_time)
        return result
    return wrapper

def dic_add(dic_a, dic_b):
    return dict(Counter(dic_a) + Counter(dic_b))

def send_msg_to_kafka(msg=None, host=None, topic=None):
    client = KafkaClient(hosts="cdh-master-slave1:9092")
    topic_out = client.topics['test_out2']
    for record in iter:
        
    with topic_out.get_sync_producer() as producer:
        producer.produce(str(msg).encode('utf-8'))

def BM25_cores(query, total_word, N, k1=0.5, b=0.9, k3=0):        
    # document的大小
    # document 的平均长度
    mongo_client = pymongo.MongoClient('mongodb://192.168.10.219:49019/')
    bi = mongo_client.lawbot.bm25_inverted
    Lave = total_word / N
    query = json.loads(query)
    id = query.get("id")
    query = query.get("data")
    BOW = {}
    scores = {}
    for word in query:
        BOW[word] = BOW.get(word, 0) + 1
    uni_words = set(query)
    inverted_list = []
    for word in uni_words:
        inverted_list = bi.find_one({'key':word})
        if not inverted_list:
            continue
        values = inverted_list.get('value')
        if len(values) >= 20000:
            continue
        for value in values:
            get = value.get
            document_id = get('doc_id')
            document_tf, document_idf = get('tf'), get('idf')
            doc_length = get('doc_length')
            fomula_b = ((k1 + 1) * document_tf) / (
            k1 * ((1 - b) + b * (doc_length / Lave)) + document_tf)
            query_tf = (k3 + 1) * BOW[word] / (k3 + BOW[word])
            bm25 = document_idf * fomula_b * query_tf
            scores[document_id] = scores.get(document_id, 0) + bm25 * BOW[word]
    result = heapq.nlargest(20, scores, key=scores.get)
    send_msg_to_kafka(result)
    # return result

if __name__ == '__main__':
    # conf = SparkConf().setMaster("spark://cdh-master-slave1:7077").set("spark.executor.memory", "2G").set("spark.driver.memory", "1G").set("spark.executor.cores","2").set("spark.cores.max","4")
    # sc = SparkContext(conf=conf)

    conf = SparkConf().setAppName("bm25")
    sc = SparkContext(conf=conf)
    # sqlContext = SQLContext(sc)
    ssc = StreamingContext(sc, 0.1)
    #mongo_client = pymongo.MongoClient('mongodb://192.168.10.219:49019/')
    #bi = mongo_client.lawbot.bm25_inverted
    #be = mongo_client.lawbot.bm25_extra
    # sc.broadcast(bi)

    #extra_data = be.find_one()
    #total_word = extra_data.get('total_word')
    #N = extra_data.get('N')

    lg.info('start')
    # TODO 调试期间不缓存
    query = [u'\u5f20\u67d0', u'\u8fdb\u5165', u'\u6c11\u5b85', u'\u5077\u7a83', u'\uff0c', u'\u88ab', u'\u4e3b\u4eba', u'\u53d1\u73b0', u'\u540e', u'\u4e0e', u'\u5176', u'\u4ea7\u751f', u'\u51b2\u7a81', u'\uff0c', u'\u5e76', u'\u7528', u'\u5229\u5668', u'\u628a', u'\u5176', u'\u6253', u'\u6210', u'\u91cd\u4f24', u'\u3002', u'\u672c\u6b21', u'\u5f20\u67d0', u'\u7a83\u53d6', u'1000', u'\u5143', u'\u4eba\u6c11\u5e01', u'\u548c', u'\u624b\u673a', u'\u4e00', u'\u90e8', u'\u3002']
    query = json.dumps(query)
    # BM25_cores(query, total_word, N)
    # if len(sys.argv) < 4:
    #    brokers, topic_in, topic_out = ['cdh-master-slave1:9092', 'test_in', 'test_out']
    # else:
    brokers, topic_in, topic_out = sys.argv[1:]
    kvs = KafkaUtils.createDirectStream(ssc, [topic_in], {"metadata.broker.list": brokers})
    lines = kvs.map(lambda x: x[1])
   #  first = True
   #  lines.pprint()
    #kvs.pprint()
    lines.foreachRDD(lambda rdd: rdd.foreachPartition(lambda query:send_msg_to_kafka))
    ssc.start()
    # lines.map(lambda x: x).foreachRDD(lambda rdd: rdd.foreach(lambda x:BM25_cores(x, sc)))
    ssc.awaitTermination()

