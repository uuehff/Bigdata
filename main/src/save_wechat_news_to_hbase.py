# coding:utf-8
# usage:$ Spark-submit --master local group_url.py

import json
import re
import time
import sys

import happybase

from pyspark import SparkContext, SparkConf


class SourceId(object):
    '''将数据来源映射为相应的id
    id由2位大类来源 + 4位小类来源组成.
    eg:
        新闻：'01'
            人民网：'00' + '0001' => '010001'
    '''

    news = '01'    # 新闻
    microblog = '02'    # 微博
    wechat = '03'    # 微信
    live = '04'    # 直播
    forum = '05'    # 论坛、贴吧等
    wemedia = '06'    # 自媒体


class TbName(object):
    public_sentiment = 'public_sentiment'
    web_traffic = 'web_traffic'


class WechatStatements(object):
    '''微信数据的列结构'''

    official_account_intro = 'official_account_intro'  # 公众号简介
    article_intro = 'article_intro'  # 文章简介
    official_account_name = 'official_account_name'  # 公众号名称
    title = 'title'  # 文章标题
    time = 'time'  # 发布时间
    # 大部分行无以下几列信息
    history_category_rank = 'history_category_rank'
    wx_alias = 'wx_alias'
    rank = 'rank'
    uin = 'uin'
    history_yesterday_index_scores = 'history_yesterday_index_scores'
    is_weixin_verify = 'is_weixin_verify'
    qrcode = 'qrcode'
    category = 'category'
    history_rank = 'history_rank'
    history_yesterday_rank = 'history_yesterday_rank'
    wx_origin_id = 'wx_origin_id'
    yesterday_rank = 'yesterday_rank'
    fans_num_estimate = 'fans_num_estimate'
    stat_time = 'stat_time'
    index_scores = 'index_scores'
    tags = 'tags'
    company = 'company'
    is_analyse = 'is_analyse'
    history_index_scores = 'history_index_scores'
    biz = 'biz'
    avg_read_num_idx1 = 'avg_read_num_idx1'
    desc = 'desc'
    user_favorite_id = 'user_favorite_id'
    name = 'name'
    history_stat_time = 'history_stat_time'
    category_rank = 'category_rank'
    customer_type = 'customer_type'
    avatar = 'avatar'
    is_stored_by_user = 'is_stored_by_user'
    history_yesterday_index_scores = 'history_yesterday_category_rank'
    yesterday_category_rank = 'yesterday_category_rank'


class NewsStatements(object):
    '''新闻数据的列结构'''

    time = 'time'
    good = 'good'
    title = 'title'
    url = 'url'
    source = 'source'
    bad = 'bad'
    web_from = 'web_from'
    web_name = 'web_name'
    comment_list = 'coment_list'


def addJson(iterdata):
    '''将json内容合并到同一个字典中

    Args:
        iterdata:包含多个json的列表
    Returns:
        dict
    '''

    result = {}
    for data in iterdata:
        result.update(json.loads(data))
    return result


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


def transformToHbase(data, source_id):
    '''将字典转为可以储存进HBase的数据

    Args:
        data: 要转的字典
        source_id: 数据来源的id, 用作rowkey的设计
    Return：
        generator object: (rowkey, [rowkey, column_family, qualifier, value])
    '''
    if not data:
        return
    rowkey = u'嫘祖杯%s0000%f' % (source_id, time.time())
    data = cleanNewsData(data)
    for key in data.keys():
        if key == 'coment_list':
            key_data = json.dumps(data[key])
            hcolumn = 'comment_list'
        else:
            key_data = data[key]
            hcolumn = key
        if isinstance(key_data, int) or isinstance(key_data, float):
            key_data = str(key_data)
        yield rowkey, [rowkey, 'd', hcolumn, key_data]


def transferDictToHbase(dict_data, family, rowkey):
    '''将一般的字典转为可以储存进HBase的数据，字典值将被转为字符串(或者json)

    Args:
        dict_data: 字典格式的数据
        family: 列族名
        rowkey: 行关键字
    Return:
        generator object: (rowkey, [rowkey, column_family, qualifier, value])
    '''
    if not rowkey or not dict_data or not family:
        return
    for key in dict_data.keys():
        key_data = dict_data[key]
        if isinstance(key_data, str) or isinstance(key_data, unicode):
            pass
        else:
            key_data = json.dumps(key_data)
        yield rowkey, [rowkey, family, key, key_data]


def transformFromWechat(data):
    '''将微信数据转为字典

    Args:
        data: json数据
    Returns:
        dict
    '''
    if not data:
        return
    tmp = {}
    tmp.update(data.get(u'信息', {}))
    tmp['official_account_intro'] = data.get(u'公众号简介', None)
    tmp['article_intro'] = data.get(u'文章简介', None)
    tmp['official_account_name'] = data.get(u'公众号名称', None)
    tmp['title'] = data.get(u'文章标题', None)
    tmp['time'] = data.get(u'发布时间', None)
    if tmp.has_key('tags'):
        tmp['tags'] = json.dumps(tmp['tags'])
    return tmp


def cleanTitle(title):
    '''清洗标题'''
    if not title:
        return
    title = title.split('_')[0]
    title = title.split('-')[0]
    title = title.replace(u'四强', u'4强')
    title = title.replace(u'八强', u'8强')
    title = title.replace(u'第二十九届', u'第29届')
    return title


def cleanComment(comments):
    '''清洗评论：去除无中文的评论'''
    for comment in comments:
        # content 不含中文就会被删除
        if not re.findall(u'[\u4e00-\u9fff]', comment.get('content')):
            comments.remove(comment)
    return comments


def cleanNewsData(data):
    '''清洗微信数据'''
    data.update({'title': cleanTitle(data['title'])})
    if data.has_key('coment_list'):
        data.update({'coment_list': cleanComment(data['coment_list'])})
    # else:
    #     data.update({'coment_list': ''})

    return data


def readFromHappybase(host, table, **kwargs):
    '''使用happybase读HBase中的数据

    Args:
        host: HBase所在IP
        table: 要读取的表
    Returns:
        直接打印
    '''
    conn = happybase.Connection(host)
    table = conn.table(table)

    def printHbase(data):
        for key in data.keys():
            if key == 'd:comment_list':
                d_list = json.loads(data[key])
                for d in d_list:
                    for x in d.keys():
                        print d[x]
            else:
                print data[key].decode('utf-8')

    for data in table.scan():
        printHbase(data[1])
    conn.close()


if __name__ == '__main__':
    conf = SparkConf().setAppName('group_url')
    sc = SparkContext(conf=conf)
    # distinct去重
    text = sc.textFile(u'/data/public_sentiment/go/2017_05/新闻*').distinct()
    result = text.groupBy(lambda x: json.loads(x).get('url'))\
                 .map(lambda x: addJson(x[1]))

    # get source
    # source = {}
    # for x in result.collect():
    # data = json.loads(x)
    # source[data.get('source')] = source.get(data.get('source'), 0) + 1

    # # put source into hbase
    # conn = happybase.Connection('192.168.10.23')
    # conn.open()
    # table = conn.table('source_id')
    # # for i, x in enumerate(source.keys()):
    # # if x:
    # # table.put(x, {'abstract:id': '%03d' % i})

    # # get source id from hbase
    # source = {}
    # for data in table.scan():
    #     source[data[0].decode('utf-8')] = data[1].get('abstract:id')

    # data analysis
    # print result.filter(lambda x: u'名人战' in
    # json.loads(x).get('title')).count()

    # save to hbase
    if len(sys.argv) > 2:
        host = sys.argv[1]
        hbase_table = sys.argv[2]
    else:
        host = '192.168.10.24'
        hbase_table = TbName.public_sentiment
    conf = {"hbase.zookeeper.quorum": host,
            "hbase.mapred.outputtable": hbase_table,
            "mapreduce.outputformat.class": "org.apache.hadoop.hbase.mapreduce.TableOutputFormat",
            "mapreduce.job.output.key.class": "org.apache.hadoop.hbase.io.ImmutableBytesWritable",
            "mapreduce.job.output.value.class": "org.apache.hadoop.io.Writable"
            }
    keyConv = "hbase.pythonconverters.StringToImmutableBytesWritableConverter"
    valueConv = "hbase.pythonconverters.StringListToPutConverter"
    # dl= [['sparkrow1', 'cf', 'a', 'value1']]
    # sc.parallelize(dl).map(lambda x: (x[0], x))\
    #   .saveAsNewAPIHadoopDataset(conf, keyConv, valueConv)
    result.flatMap(lambda x: transformToHbase(x, SourceId.news))\
          .saveAsNewAPIHadoopDataset(conf, keyConv, valueConv)

    # 保存微信数据
    # wechat = sc.textFile('/data/public_sentiment/go/2017_05/微信*').distinct()
    # wechat.map(lambda x: transformFromWechat(json.loads(x)))\
    #       .flatMap(lambda x: transformToHbase(x, SourceId.wechat))\
    #       .saveAsNewAPIHadoopDataset(conf, keyConv, valueConv)

    # 保存网站流量数据，此处conf有更新
    # conf['hbase.mapred.outputtable'] = TbName.web_traffic
    # web_traffic = sc.textFile('/data/public_sentiment/go/2017_05/网站*').distinct()
    # web_traffic.map(json.loads).flatMap(lambda x: transferDictToHbase(
    #                                     x.get('data', None), x.get('domain', None), 'd'))\
    #            .saveAsNewAPIHadoopDataset(conf, keyConv, valueConv)

    # read from hbase
    # rkeyConv = "hbase.pythonconverters.ImmutableBytesWritableToStringConverter"
    # rvalueConv = "hbase.pythonconverters.HBaseResultToStringConverter"
    # rconf = {"hbase.zookeeper.quorum": host,
    #          "hbase.mapreduce.inputtable": hbase_table}
    # ps_data = sc.newAPIHadoopRDD(
    #     "org.apache.hadoop.hbase.mapreduce.TableInputFormat",
    #     "org.apache.hadoop.hbase.io.ImmutableBytesWritable",
    #     "org.apache.hadoop.hbase.client.Result",
    #     keyConverter=rkeyConv,
    #     valueConverter=rvalueConv,
    #     conf=rconf
    # )
    #
    # real_data = ps_data.map(lambda x: {x[0]: transformFromHbase(x[1])})
    # for v in real_data.collect():
    #     print v

    sc.stop()
