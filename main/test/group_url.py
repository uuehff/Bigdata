# -*- coding: utf-8 -*-
# usage:$ Spark-submit --master local group_url.py

import json

from pyspark import SparkContext, SparkConf

import happybase


def add_json(iterdata):
    result = {}
    for data in iterdata:
        result.update(json.loads(data))
    return result


def transform_from_hbase(data):
    if not data:
        return {}
    data = data.split('\n')
    tmp = {}
    for x in data:
        td = json.loads(x)
        key = '%s:%s' % (td['columnFamily'], td['qualifier'])
        tmp[key] = td['value']
    return tmp


def transform_to_hbase(data, source_id):
    if not data:
        return
    try:
        rowkey = u'嫘祖杯' + ''.join(data['time'].split('-'))\
            + source_id[data['source']]
    except Exception:
        return
    for key in data.keys():
        if key == 'coment_list':
            key_data = json.dumps(data[key])
            hcolumn = 'comment_list'
        else:
            key_data = data[key]
            hcolumn = key
        yield rowkey, [rowkey, 'd', hcolumn, key_data]


if __name__ == '__main__':
    conf = SparkConf().setAppName('test').set("Spark.shuffle.io.maxRetries","15").set("Spark.shuffle.io.retryWait","3s")
    #.set("Spark.shuffle.io.retryWait","4s")
    sc = SparkContext(conf=conf)
    sc.setLogLevel("ERROR")
    text = sc.textFile('hdfs://cdh-master-slave1:8020/user/caitinggui/input/wei*')
    result = text.groupBy(lambda x: json.loads(x).get('url'),6)\
                .map(lambda x : (x[0],1)).reduceByKey(lambda x,y : x+y)
                # .map(lambda x: add_json(x[1]))
    # print result.getNumPartitions()
    # print result.take(1)
    print result.count()

    # # put source into hbase
    # conn = happybase.Connection('192.168.10.23')
    # conn.open()
    # table = conn.table('source_id')
    # source = {}
    # for data in table.scan():
    #     source[data[0].decode('utf-8')] = data[1].get('abstract:id')

    # save to hbase
    # host = '192.168.10.24'
    # hbase_table = 'test'
    # conf = {"hbase.zookeeper.quorum": host,
    #         "hbase.mapred.outputtable": hbase_table,
    #         "mapreduce.outputformat.class": "org.apache.hadoop.hbase.mapreduce.TableOutputFormat",
    #         "mapreduce.job.output.key.class": "org.apache.hadoop.hbase.io.ImmutableBytesWritable",
    #         "mapreduce.job.output.value.class": "org.apache.hadoop.io.Writable"
    #         }
    # keyConv = "hbase.pythonconverters.StringToImmutableBytesWritableConverter"
    # valueConv = "hbase.pythonconverters.StringListToPutConverter"
    # result.flatMap(lambda x: transform_to_hbase(x, source))\
    #       .saveAsNewAPIHadoopDataset(conf, keyConv, valueConv)

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
    # real_data = ps_data.flatMapValues(lambda v: v.split('\n'))\
    #                    .mapValues(json.loads)
    # real_data = ps_data.map(lambda x: (x[0].decode('string_escape').decode('utf-8'),
    # x[1].decode('string_escape').decode('string_escape').decode('utf-8').split('\n')))\
    #                             .flatMapValues(lambda v: v.split('\n'))\
    #                             .mapValues(json.loads)

    # real_data = ps_data.map(lambda x: {x[0]: transform_from_hbase(x[1])})
    # for v in real_data.collect():
    #     print v

    sc.stop()
