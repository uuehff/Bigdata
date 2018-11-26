# coding:utf-8
import json
import sys
import time
import functools
from operator import add
import logging
from collections import Counter
import heapq

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

def send_msg_to_kafka(msg, host=None, topic=None):
    client = KafkaClient(hosts="cdh-master-slave1:9092")
    topic_out = client.topics['test_out']
    with topic_out.get_sync_producer() as producer:
        # for record in iter:
            tmp = '(%s>>>)' % (str(msg))
            producer.produce(tmp.encode('utf-8'))

def calculate_value(value):
    Lave=149; k1=0.5; b=0.9; k3=0;
    BOW_NUM = value[0]
    get = value[1].get
    document_id = get('doc_id')
    document_tf, document_idf = get('tf'), get('idf')
    doc_length = get('doc_length')
    fomula_b = ((k1 + 1) * document_tf) / (
    k1 * ((1 - b) + b * (doc_length / Lave)) + document_tf)
    query_tf = (k3 + 1) * BOW_NUM / (k3 + BOW_NUM)
    bm25 = document_idf * fomula_b * query_tf * BOW_NUM
    return (document_id, bm25)
    
def calculate(values, Lave, BOW_NUM, k1=0.5, b=0.9, k3=0):
    values_tmp = values.get('value')
    values_rdd = sc.parallelize(values_tmp)
    return values.map(lambda value: calculate_value(value, Lave, BOW_NUM, k1,\
                                                    b, k3))

# @run_time
def BM25_cores(msg, bi2):        
    # document的大小
    # document 的平均长度
    total_word=100; N=12; k1=1.5; b=0.5; k3=0;
    Lave = total_word / N
    BOW = {}
    inverted_json = []
    # query: '{"id":"12", "data":["23", "34"]}'
    tmp = '%s' % str(msg)
    query = json.loads(tmp).get('data')
    for word in query:
        BOW[word] = BOW.get(word, 0) + 1
    uni_words = set(query)
    inverted_list = []
    for word in uni_words:
        inverted_data = bi2.find_one({'key':word})
        if inverted_data and len(inverted_data.get('value')) < 20000:
            inverted_list.append(inverted_data)
    #json_list = sc2.parallelize(inverted_list, 35*2) 
    '''
    start_time = time.time()
    scores = json_list.map(lambda values: (BOW[values.get('key')], values.get('value')))\
                      .flatMapValues(lambda x: x)\
                      .map(calculate_value)\
                      .reduceByKey(add)
    result = scores.top(20, key=lambda x:x[1])
    # print 'run time is:%s' % (time.time() - start_time)
    # return result
    '''
#    send_msg_to_kafka(inverted_json)

if __name__ == '__main__':
    conf = SparkConf().setMaster("spark://cdh-master-slave1:7077").set("spark.executor.memory", "2G").set("spark.driver.memory", "1G").set("spark.executor.cores","2").set("spark.cores.max","4")
    # sc = SparkContext(conf=conf)

    # conf = SparkConf().setAppName("bm25")
    sc = SparkContext(conf=conf)
    sqlContext = SQLContext(sc)
    ssc = StreamingContext(sc, 5)
    mongo_client = pymongo.MongoClient('mongodb://192.168.10.219:49019/')
    bi = mongo_client.lawbot.bm25_inverted
    be = mongo_client.lawbot.bm25_extra
    # sc.broadcast(bi)

    extra_data = be.find_one()
    total_word = extra_data.get('total_word')
    N = extra_data.get('N')


    lg.info('start')
    # TODO 调试期间不缓存
    # 等价于inverted_db.cache()
    # sqlContext.cacheTable('inverted_table')
    # 触发cacheTable的操作
    # df = sqlContext.sql("SELECT * FROM inverted_table where key='\xe5\x8a\xb3\xe5\x8a\xa8\xe9\x98\xb2\xe6\x8a\xa4'").collect()
    query = [u'\u5f20\u67d0', u'\u8fdb\u5165', u'\u6c11\u5b85', u'\u5077\u7a83', u'\uff0c', u'\u88ab', u'\u4e3b\u4eba', u'\u53d1\u73b0', u'\u540e', u'\u4e0e', u'\u5176', u'\u4ea7\u751f', u'\u51b2\u7a81', u'\uff0c', u'\u5e76', u'\u7528', u'\u5229\u5668', u'\u628a', u'\u5176', u'\u6253', u'\u6210', u'\u91cd\u4f24', u'\u3002', u'\u672c\u6b21', u'\u5f20\u67d0', u'\u7a83\u53d6', '1000', u'\u5143', u'\u4eba\u6c11\u5e01', u'\u548c', u'\u624b\u673a', u'\u4e00', u'\u90e8', u'\u3002']
    query = [u'\u88ab\u544a\u4eba', u'\u8521\u519b', u'\u4ee5', u'\u975e\u6cd5', u'\u5360\u6709', u'\u4e3a', u'\u76ee\u7684', u'\uff0c', u'\u591a\u6b21', u'\u5165', u'\u6237', u'\u76d7\u7a83', u'\u4ed6\u4eba', u'\u8d22\u7269', u'\uff0c', u'\u5176', u'\u884c\u4e3a', u'\u5df2', u'\u6784\u6210', u'\u76d7\u7a83\u7f6a', u'\u3002', u'\u516c\u8bc9', u'\u673a\u5173', u'\u6307\u63a7', u'\u88ab\u544a\u4eba', u'\u8521\u519b\u72af', u'\u62a2\u52ab\u7f6a', u'\uff0c', u'\u867d', u'\u63d0\u4f9b', u'\u4e86', u'\u88ab\u5bb3\u4eba', u'\u9648\u8ff0', u'\u548c', u'\u8bc1\u4eba', u'\u8bc1\u8a00', u'\u4e88\u4ee5', u'\u8bc1\u5b9e', u'\uff0c', u'\u4f46', u'\u56e0', u'\u8bc1\u4eba', u'\u8bc1\u8a00', u'\u5747', u'\u7cfb', u'\u4ece', u'\u88ab\u5bb3\u4eba\u5904', u'\u83b7\u77e5', u'\uff0c', u'\u7cfb', u'\u4f20\u6765', u'\u8bc1\u636e', u'\uff0c', u'\u4e0e', u'\u88ab\u544a\u4eba', u'\u4ec5', u'\u5b9e\u65bd', u'\u76d7\u7a83', u'\u884c\u4e3a', u'\u7684', u'\u4f9b\u8ff0', u'\u76f8', u'\u77db\u76fe', u'\uff0c', u'\u4e14', u'\u65e0', u'\u5176\u5b83', u'\u8bc1\u636e', u'\u76f8\u5370\u8bc1', u'\uff0c', u'\u65e0\u6cd5', u'\u5f62\u6210', u'\u8bc1\u636e', u'\u9501\u94fe', u'\u3002', u'\u5728', u'\u4e0a\u8ff0', u'\u8bc1\u636e', u'\u76f8', u'\u77db\u76fe', u'\u7684', u'\u60c5\u51b5', u'\u4e0b', u'\uff0c', u'\u672c\u9662', u'\u4ece', u'\u6709\u5229\u4e8e', u'\u88ab\u544a\u4eba', u'\u7684', u'\u539f\u5219', u'\u51fa\u53d1', u'\uff0c', u'\u91c7\u4fe1', u'\u88ab\u544a\u4eba', u'\u7684', u'\u4f9b\u8ff0', u'\uff0c', u'\u5373', u'\u672c\u9662', u'\u8ba4\u5b9a', u'\u88ab\u544a\u4eba', u'\u5b9e\u65bd', u'\u4e86', u'\u5165', u'\u6237', u'\u76d7\u7a83', u'\u884c\u4e3a', u'\uff0c', u'\u516c\u8bc9', u'\u673a\u5173', u'\u6307\u63a7', u'\u88ab\u544a\u4eba', u'\u72af', u'\u62a2\u52ab\u7f6a', u'\u4e0d', u'\u80fd', u'\u6210\u7acb', u'\u3002', u'\u6545', u'\u5bf9', u'\u88ab\u544a\u4eba', u'\u8521\u519b', u'\u53ca\u5176', u'\u8fa9\u62a4\u4eba', u'\u63d0\u51fa', u'\u88ab\u544a\u4eba', u'\u8521\u519b', u'\u884c\u4e3a', u'\u4e0d', u'\u6784\u6210', u'\u62a2\u52ab\u7f6a', u'\u7684', u'\u8fa9\u89e3', u'\u8fa9\u62a4', u'\u610f\u89c1', u'\uff0c', u'\u672c\u9662', u'\u4e88\u4ee5', u'\u91c7\u7eb3']
    # score = BM25_cores(query, total_word, N)
    # if len(sys.argv) < 4:
    #    brokers, topic_in, topic_out = ['cdh-master-slave1:9092', 'test_in', 'test_out']
    # else:
    brokers, topic_in, topic_out = sys.argv[1:]
    kvs = KafkaUtils.createDirectStream(ssc, [topic_in], {"metadata.broker.list": brokers})
    lines = kvs.map(lambda x: x[1])
    # lines.pprint()
    #kvs.pprint()
    lines.map(lambda x: x).foreachRDD(lambda rdd: rdd.foreach(lambda x:BM25_cores(x, bi)))
    ssc.start()
    # lines.map(lambda x: x).foreachRDD(lambda rdd: rdd.foreach(lambda x:BM25_cores(x, sc)))
    ssc.awaitTermination()

    # sc.stop()
    ''' 
    # lines是输入的一个集合，在这个脚本中，要求每个元素都是Unicode
    if len(sys.argv) > 3:
        host = sys.argv[1]
        port = sys.argv[2]
    else:
        host = 'localhost'
        port = 11118
    lines = ssc.socketTextStream(host, port)
    lg.info('lines:%s' % lines)
    lines.pprint()
    # querys = lines.map(lambda line: line.split(" "))
    lines.foreachRDD(lambda query: BM25_cores(query, total_word, N))
    ssc.start()
    '''
    '''
    while True:
        try:
            querys = lines.map(lambda line: line.split(' '))
            querys.pprint()
            result = querys.map(lambda line: BM25_cores(line))
            lg.info('result %s' % result)
            result.foreachRDD(lambda x: lg.info(x.take(3)))
        except Exception, e:
            lg.error('lines.map error:%s' % e)
    '''
    # result.foreachRDD(lambda x: lg.info(x.reduceByKey(add).top(10, key=lambda x:x)))
    # wr = result.reduceByKey(add)
    # wr.pprint()
    # result.pprint()
    # result.foreachRDD(lambda x: lg.info(x.reduceByKey(add).top(20, key=lambda x: x)))
    # ssc.awaitTermination()

    # sc.stop()
