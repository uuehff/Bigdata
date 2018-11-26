# coding:utf-8

import json

import jieba
import numpy as np

from pyspark import SparkContext, SparkConf


jieba.load_userdict(
    '/home/caitinggui/project/public_sentiment/microblog/dict.txt')   # 加载词典
# https://zhuanlan.zhihu.com/p/23225934


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


def judegOdd(num):
    if (num % 2) == 0:
        return 'even'
    else:
        return 'odd'


def sentimentScoreList(dataset, most_degree, very_degree, more_degree,
                       ish_degree):
    # 将一个评论分句
    seg_sentence = dataset.split('。')

    # 一句的情感值
    count1 = []
    # 整个评论的情感值
    count2 = []
    for sen in seg_sentence:  # 循环遍历每一个评论
        cutword = jieba.lcut(sen, cut_all=False)  # 把句子进行分词，以列表的形式返回
        segtmp = [w for w in cutword if w.encode('utf-8') not in stop_word]
        i = 0  # 记录扫描到的词的位置
        a = 0  # 记录情感词的位置
        poscount = 0  # 积极词的第一次分值
        poscount2 = 0  # 积极词反转后的分值
        poscount3 = 0  # 积极词的最后分值（包括叹号的分值）
        negcount = 0
        negcount2 = 0
        negcount3 = 0
        for word in segtmp:
            if word.encode('utf-8') in positive_word:  # 判断词语是否是情感词
                poscount += 1
                # 否定词的个数
                c = 0
                for w in segtmp[a:i]:  # 扫描情感词前的程度词
                    if w.encode('utf-8') in most_degree:
                        poscount *= 4.0
                    elif w.encode('utf-8') in very_degree:
                        poscount *= 3.0
                    elif w.encode('utf-8') in more_degree:
                        poscount *= 2.0
                    elif w.encode('utf-8') in ish_degree:
                        poscount *= 0.5
                    elif w.encode('utf-8') in deny_word:
                        c += 1
                if judegOdd(c) == 'odd':  # 扫描情感词前的否定词数
                    poscount *= -1.0
                    poscount2 += poscount
                    poscount = 0
                    poscount3 = poscount + poscount2 + poscount3
                    poscount2 = 0
                else:
                    poscount3 = poscount + poscount2 + poscount3
                    poscount = 0
                a = i + 1  # 情感词的位置变化

            elif word.encode('utf-8') in negative_word:  # 消极情感的分析，与上面一致
                negcount += 1
                d = 0
                for w in segtmp[a:i]:
                    if w.encode('utf-8') in most_degree:
                        negcount *= 4.0
                    elif w.encode('utf-8') in very_degree:
                        negcount *= 3.0
                    elif w.encode('utf-8') in more_degree:
                        negcount *= 2.0
                    elif w.encode('utf-8') in ish_degree:
                        negcount *= 0.5
                    elif w.encode('utf-8') in degree_word:
                        d += 1
                if judegOdd(d) == 'odd':
                    negcount *= -1.0
                    negcount2 += negcount
                    negcount = 0
                    negcount3 = negcount + negcount2 + negcount3
                    negcount2 = 0
                else:
                    negcount3 = negcount + negcount2 + negcount3
                    negcount = 0
                a = i + 1
            elif word.encode('utf-8') == '！' or word.encode('utf-8') == '!':  # 判断句子是否有感叹号
                for w2 in segtmp[::-1]:  # 扫描感叹号前的情感词，发现后权值+2，然后退出循环
                    if w2.encode('utf-8') in positive_word or w2.encode('utf-8') in negative_word:
                        poscount3 += 2
                        negcount3 += 2
                        break
            elif word.encode('utf-8') == '？' or word.encode('utf-8') == '?':  # 判断句子是否有问号
                for w2 in segtmp[::-1]:
                    if w2.encode('utf-8') in positive_word or w2.encode('utf-8') in negative_word:
                        negcount3 += 2
                        break
            i += 1  # 扫描词位置前移

            # 以下是防止出现负数的情况
            pos_count = 0
            neg_count = 0
            if poscount3 < 0 and negcount3 > 0:
                neg_count += negcount3 - poscount3
                pos_count = 0
            elif negcount3 < 0 and poscount3 > 0:
                pos_count = poscount3 - negcount3
                neg_count = 0
            elif poscount3 < 0 and negcount3 < 0:
                neg_count = -poscount3
                pos_count = -negcount3
            else:
                pos_count = poscount3
                neg_count = negcount3

            count1.append([pos_count, neg_count])
        count2.append(count1)
        count1 = []

    return count2, segtmp


def sentimentScore(senti_score_list):
    score = []
    for review in senti_score_list:
        score_array = np.array(review)
        Pos = np.sum(score_array[:, 0])
        Neg = np.sum(score_array[:, 1])
        AvgPos = np.mean(score_array[:, 0])
        AvgPos = float('%.1f' % AvgPos)
        AvgNeg = np.mean(score_array[:, 1])
        AvgNeg = float('%.1f' % AvgNeg)
        StdPos = np.std(score_array[:, 0])
        StdPos = float('%.1f' % StdPos)
        StdNeg = np.std(score_array[:, 1])
        StdNeg = float('%.1f' % StdNeg)
        score.append([Pos, Neg, AvgPos, AvgNeg, StdPos, StdNeg])
    return score


# data = '你就是个王八蛋，混账玩意!你们的手机真不好用！非常生气，我非常郁闷！！！！'
# data = '如果食宿自理的话主办方花不了几块钱吧?'
# count2, segtmp = sentimentScoreList(data)


# print count2
# for w in segtmp:
#     print w
# data2= '我好开心啊，非常非常非常高兴！今天我得了一百分，我很兴奋开心，愉快，开心'
# data = raw_input("输入：")
# print(sentimentScore(sentimentScoreList(data2)))
# print sentimentScore(count2)

if __name__ == '__main__':
    conf = SparkConf().setAppName('weibo_sentiment').setMaster('local')
    # conf = SparkConf().setMaster("Spark://cdh-master-slave1:7077").set("Spark.executor.memory", "15G").set("Spark.driver.memory", "12G").set("Spark.executor.cores","1").set("Spark.cores.max","2").set("Spark.dynamicAllocation.enabled", "false").set("Spark.python.worker.reuse", "true").setAppName('bm25_cache')
    sc = SparkContext(conf=conf)

    path = '/home/caitinggui/project/public_sentiment/microblog/'
    deny_word = openFile(path + 'negation.txt')
    positive_word = openFile(path + 'positive.txt')
    negative_word = openFile(path + 'negative.txt')
    stop_word = openFile(path + 'stopword.txt')
    degree_word = openFile(path + 'degree.txt')

    # spark广播变量
    # words between 'extreme' and 'very' in degree.txt
    most_degree = sc.broadcast(degree_word[degree_word.index(
        'extreme') + 1: degree_word.index('very')])  # 权重4，即在情感词前乘以4
    very_degree = sc.broadcast(degree_word[degree_word.index(
        'very') + 1: degree_word.index('more')])  # 权重3
    more_degree = sc.broadcast(degree_word[degree_word.index(
        'more') + 1: degree_word.index('ish')])  # 权重2
    ish_degree = sc.broadcast(degree_word[degree_word.index(
        'ish') + 1: degree_word.index('last')])  # 权重0.5

    data = '连笑也就是这个样子了！李钦诚和杨鼎新拿冠军了，连笑也拿不着'
    comment = sc.parallelize([data])
    print comment.collect()
    print comment.map(lambda x: sentimentScoreList(x, most_degree.value,
                                                   very_degree.value,
                                                   more_degree.value,
                                                   ish_degree.value))\
                 .map(lambda x: sentimentScore(x[0])).collect()

    # read from hbase
#     host = '192.168.10.23'
    # hbase_table = 'public_sentiment'
    # rkeyConv = "hbase.pythonconverters.ImmutableBytesWritableToStringConverter"
    # rvalueConv = "hbase.pythonconverters.HBaseResultToStringConverter"
    # rconf = {"hbase.zookeeper.quorum": host,
    # "hbase.mapreduce.inputtable": hbase_table,
    # "hbase.mapreduce.scan.row.start": u'嫘祖杯020000',
    # "hbase.mapreduce.scan.row.stop": u'嫘祖杯029999',
    # }
    # ps_data = sc.newAPIHadoopRDD(
    # "org.apache.hadoop.hbase.mapreduce.TableInputFormat",
    # "org.apache.hadoop.hbase.io.ImmutableBytesWritable",
    # "org.apache.hadoop.hbase.client.Result",
    # keyConverter=rkeyConv,
    # valueConverter=rvalueConv,
    # conf=rconf
    # )

    # real_data = ps_data.map(lambda x: {x[0]: transformFromHbase(x[1])})
#     print real_data.take(10)
    sc.stop()
