 # -*- coding: utf-8 -*-
import sys
from pyspark.sql import SQLContext
from pyspark import SparkContext,SparkConf
import re
import time

class SourceId(object):
    '''将数据来源映射为相应的id

    id由2位大类来源 + 4位小类来源组成.
    eg:
        新闻：'01'
            人民网：'01' + '0001' => '010001'
    '''
    news = '01'
    microblog = '02'
    wechat = '03'
    live = '04'
    forum = '05'
    wemedia = '06'

class TbName(object):
    public_sentiment = 'public_sentiment'

def filter_(x):
    p1 = ur'^[\w,.:;!，。：；！]?$'    #这里有待增加字符，如、？
    pattern1 = re.compile(p1)
    matcher1 = re.match(pattern1,x)
    if not matcher1 :
        return True
    else :
        return False

def putProducer(rowObject,source_id):
    j = rowObject.asDict() #将Row对象转化为json对象
    title_ = j.get('tie_title')
    title_result = u''
    if u'第二十九届' in title_:
        title = title_.replace(u'第二十九届',u'第29届')
        if u'四强' in title:
            title_result = title.replace(u'四强',u'4强')
        elif u'八强' in title:
            title_result = title.replace(u'八强',u'8强')
        elif u'十六强' in title:
            title_result = title.replace(u'十六强',u'16强')
        elif u'三十二强' in title:
            title_result = title.replace(u'三十二强',u'32强')
        else :
            title_result = title
    elif u'四强' in title_:
        title_result = title_.replace(u'四强',u'4强')
    elif u'八强' in title_:
        title_result = title_.replace(u'八强',u'8强')
    elif u'十六强' in title_:
        title_result = title_.replace(u'十六强',u'16强')
    elif u'三十二强' in title_:
        title_result = title_.replace(u'三十二强',u'32强')
    else :
        title_result = title_
    list_ = []
    rowkey = u'嫘祖杯%s0000%f' % (source_id, time.time())
    for key in j.keys():
        if key == 'tie_title':
            tmp_list = [rowkey,'d',key,title_result]
        else :
            tmp_list = [rowkey,'d',key,j.get(key)]
        list_.append(tmp_list)
    return list_

if __name__ == "__main__":
    if len(sys.argv) > 2:
        host = sys.argv[1]
        hbase_table = sys.argv[2]
    else:
        host = '192.168.10.24'
        hbase_table = 'tieba2'
    sparkConf = SparkConf()
    sc = SparkContext(conf=sparkConf)
    sc.setLogLevel("ERROR")  # ALL, DEBUG, ERROR, FATAL, INFO, OFF, TRACE, WARN
    #sc.setLogLevel("DEBUG")  # ALL, DEBUG, ERROR, FATAL, INFO, OFF, TRACE, WARN
    sqlContext = SQLContext(sc)

    df = sqlContext.read.json("hdfs://cdh-master-slave1:8020/data/public_sentiment/go/2017_05/baidu_tieba.txt").distinct().cache() #去重
    rdd_put = df.rdd.filter(lambda x:filter_(x.tie_content)).flatMap(lambda row : putProducer(row,'05')).cache()  #过滤单个字母、字符；转换：二十九 => 29，并返回存储到Hbase所需的数据格式
    #rdd_put = rdd.flatMap(lambda row : putProducer(row,'05'))     #转换：二十九 => 29，并返回Hbase数据格式
    # host = '192.168.10.24'
    # table = 'tieba'
    conf = {"hbase.zookeeper.quorum": host,
            "hbase.mapred.outputtable": hbase_table,
            "mapreduce.outputformat.class": "org.apache.hadoop.hbase.mapreduce.TableOutputFormat",
            "mapreduce.job.output.key.class": "org.apache.hadoop.hbase.io.ImmutableBytesWritable",
            "mapreduce.job.output.value.class": "org.apache.hadoop.io.Writable"}
    keyConv = "hbase.pythonconverters.StringToImmutableBytesWritableConverter"
    valueConv = "hbase.pythonconverters.StringListToPutConverter"
    # keyConv = "org.apache.Spark.examples.pythonconverters.StringToImmutableBytesWritableConverter"
    # valueConv = "org.apache.Spark.examples.pythonconverters.StringListToPutConverter"

    rdd_put.map(lambda x: ('', x)).saveAsNewAPIHadoopDataset(
        conf=conf,
        keyConverter=keyConv,
        valueConverter=valueConv)


    #conf = SparkConf().setAppName('weiwc-sort').setMaster("Spark://cdh-master-slave1:7077").set("Spark.executor.memory", "5G").set("Spark.executor.cores","2").set("Spark.cores.max","6").set("Spark.shuffle.io.maxRetrie","8").set("Spark.shuffle.io.retryWait","5s")

    sc.stop()
