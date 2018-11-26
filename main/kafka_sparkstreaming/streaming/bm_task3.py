# coding:utf-8
import json
import sys
import time
import functools
from operator import add
import logging
from collections import Counter
import heapq

from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext
from pyspark.streaming import StreamingContext

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

def calculate(values, Lave, BOW_NUM, k1=0.5, b=0.9, k3=0):
    values = values.get('value')
    scores = {}
    if len(values) >= 20000:
        return {0: 0}
    for value in values:
        get = value.get
        document_id = get('doc_id')
        document_tf, document_idf = get('tf'), get('idf')
        doc_length = get('doc_length')
        fomula_b = ((k1 + 1) * document_tf) / (
        k1 * ((1 - b) + b * (doc_length / Lave)) + document_tf)
        query_tf = (k3 + 1) * BOW_NUM / (k3 + BOW_NUM)
        bm25 = document_idf * fomula_b * query_tf
        scores[document_id] = scores.get(document_id, 0) + bm25 * BOW_NUM
    return scores

@run_time
def BM25_cores(query, total_word, N, k1=1.5, b=0.5, k3=0):        
    # document的大小
    ld = N
    # document 的平均长度
    Lave = total_word / ld
    BOW = {}
    query = query.collect()
    inverted_json = []
    for word in query:
        BOW[word] = BOW.get(word, 0) + 1
    uni_words = set(query)
    for index, word in enumerate(uni_words):
        if index == 0:
            inverted_json = sqlContext.sql("SELECT key, value FROM inverted_table WHERE key='%s' LIMIT 1" % word.encode('utf-8'))
        else:
            inverted_json_tmp = sqlContext.sql("SELECT key, value FROM inverted_table WHERE key='%s' LIMIT 1" % word.encode('utf-8'))
            inverted_json = inverted_json.unionAll(inverted_json_tmp)
    if not inverted_json:
        return 
    inverted_json = inverted_json.toJSON()
    start_time = time.time() 
    json_list = inverted_json.map(lambda x:json.loads(x))
    scores = json_list.map(lambda values: calculate(values, Lave, BOW[values.get('key')])).reduce(dic_add)
    print 'run time is:%s' % (time.time() - start_time)
    lg.info(heapq.nlargest(20, scores, key=scores.get))
    #return heapq.nlargest(20, scores, key=scores.get)

if __name__ == '__main__':
    conf = SparkConf().setAppName("bm25")
    sc = SparkContext(conf=conf)
    sqlContext = SQLContext(sc)
    ssc = StreamingContext(sc, 5)
    inverted_db = sqlContext.read.format("com.mongodb.spark.sql.DefaultSource")\
                    .option("spark.mongodb.input.uri", "mongodb://192.168.10.219:49019/lawbot.bm25_inverted")\
                    .load()
    extra_db = sqlContext.read.format("com.mongodb.spark.sql.DefaultSource")\
                    .option("spark.mongodb.input.uri", "mongodb://192.168.10.219:49019/lawbot.bm25_extra")\
                    .load()

    extra_data = extra_db.take(1)[0].asDict()
    total_word = extra_data.get('total_word')
    N = extra_data.get('N')

    # inverted_df = sqlContext.read.json('input/xaa')
    sqlContext.registerDataFrameAsTable(inverted_db, 'inverted_table')
    lg.info('start')
    # TODO 调试期间不缓存
    # 等价于inverted_db.cache()
    # sqlContext.cacheTable('inverted_table')
    # 触发cacheTable的操作
    # df = sqlContext.sql("SELECT * FROM inverted_table where key='\xe5\x8a\xb3\xe5\x8a\xa8\xe9\x98\xb2\xe6\x8a\xa4'").collect()
    query = [u'\u5f20\u67d0', u'\u8fdb\u5165', u'\u6c11\u5b85', u'\u5077\u7a83', u'\uff0c', u'\u88ab', u'\u4e3b\u4eba', u'\u53d1\u73b0', u'\u540e', u'\u4e0e', u'\u5176', u'\u4ea7\u751f', u'\u51b2\u7a81', u'\uff0c', u'\u5e76', u'\u7528', u'\u5229\u5668', u'\u628a', u'\u5176', u'\u6253', u'\u6210', u'\u91cd\u4f24', u'\u3002', u'\u672c\u6b21', u'\u5f20\u67d0', u'\u7a83\u53d6', '1000', u'\u5143', u'\u4eba\u6c11\u5e01', u'\u548c', u'\u624b\u673a', u'\u4e00', u'\u90e8', u'\u3002']
    query = sc.parallelize(query)
    score = BM25_cores(query, total_word, N)
    print score
    # sc.stop()
    
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
    ssc.awaitTermination()

    # sc.stop()
