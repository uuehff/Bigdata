# -*- coding: utf-8 -*-
import json
import sys
import jieba
# import pandas as pd
import matplotlib.pyplot as plt
from pyspark import SparkConf, SparkContext
from wordcloud import WordCloud

# jieba.load_userdict('E:\PycharmProjects\test1\gitlib\public_sentiment\microblog\dict.txt')   #加载词典

jieba.load_userdict('E:\\PycharmProjects\\test1\\data\\dict.txt')   #加载词典


def openFile(filename):
    '''return file content as list without any '\n'
    Args:
        full file path
    Returns:
        list which contains file content
    '''
    content = []
    with open(filename, 'r') as f:
        for line in f:
            content.append(line.strip('\n'))
    return content


def cutWord(text, stopwords):
    words = jieba.cut(text, cut_all=False)
    ww = [w for w in words if w.encode('utf-8') not in stopwords]
    return ww


def transformFromHbase(data):
    '''将HBase数据转为字典

    Args:
        data:HBase的一个cell内的数据
    Returns:
        dict
    '''
    if not data:
        return {}
    data = data.split('\n')
    tmp = {}
    for x in data:
        td = json.loads(x)
        key = '%s:%s' % (td['columnFamily'], td['qualifier'])
        tmp[key] = td['value']
    return tmp


def word_cloud(freq_word):
    '''画词云图,后续待完善'''
    wordcloud = WordCloud(font_path='C:\Python27\Lib\site-packages\matplotlib\mpl-data\fonts\ttf\simhei.ttf',
                          max_font_size=200, random_state=30).fit_words(freq_word[:100])
    # wordcloud = WordCloud( max_font_size = 50,            # 设置字体最大值
    #             random_state = 30,            # 设置有多少种随机生成状态，即有多少种配色方案
    #             ).fit_words(freq_word[:100])
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()


if __name__ == '__main__':

    conf = SparkConf().setAppName('weibo_sentiment').setMaster("local")
    sc = SparkContext(conf=conf)
    sc.setLogLevel("ERROR")

    stopword_file = 'E:\\PycharmProjects\\test1\\data\\stopword.txt'
    stopwords = openFile(stopword_file)
    # text_file = 'E:\\PycharmProjects\\test1\\data\weixin_new.csv'
    # freq_word = cutWord(text_file, stopwords)
    # print freq_word
    # word_cloud(freq_word)


    rkeyConv = "hbase.pythonconverters.ImmutableBytesWritableToStringConverter"
    rvalueConv = "hbase.pythonconverters.HBaseResultToStringConverter"
    host = '192.168.10.24'
    hbase_table = 'public_sentiment'
    rconf = {"hbase.zookeeper.quorum": host,
             "hbase.mapreduce.inputtable": hbase_table,
             # 03代表微信数据
             "hbase.mapreduce.scan.row.start": u'嫘祖杯030000',
             "hbase.mapreduce.scan.row.stop": u'嫘祖杯039999',
             }
    ps_data = sc.newAPIHadoopRDD(
        "org.apache.hadoop.hbase.mapreduce.TableInputFormat",
        "org.apache.hadoop.hbase.io.ImmutableBytesWritable",
        "org.apache.hadoop.hbase.client.Result",
        keyConverter=rkeyConv,
        valueConverter=rvalueConv,
        conf=rconf
    )

    real_data = ps_data.map(lambda x: transformFromHbase(x[1]))\
                       .map(lambda x: x.get('d:title', None))
    print real_data.collect()

    data = sc.parallelize(['the data of word', 'another data'])
    result = real_data.flatMap(lambda x: cutWord(x, stopwords))\
                      .map(lambda x: (x, 1))\
                      .reduceByKey(lambda x, y: x + y)
    print result.collect()

    sc.stop()
