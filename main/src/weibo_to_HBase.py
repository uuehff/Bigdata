 # -*- coding: utf-8 -*-
import sys
from pyspark.sql import SQLContext
from pyspark import SparkContext,SparkConf
import re
import time
import json
import datetime


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

class WeiboFields(object):
#    ID = 'ID'
    info = 'info'
    name = 'name'
    guanzhu  = 'guanzhu'
    label = 'label'    
    renzheng  = 'renzheng'
    fensi = 'fensi'
    sex = 'sex'
    area = 'area'
    birth = 'birth'
    desc = 'desc'
    weibo_num = 'weibo_num'
    comment = 'comment'
    dianzan_num = 'dianzan_num'
    pinglun_content = 'pinglun_content'
    pinglun_user = 'pinglun_user'
    content = 'content'
    time = 'time'
    nicheng = 'nicheng'
    zan_num = 'zan_num'
    website = 'website'
    comment_num = 'comment_num'
    zhuanfa_num = 'zhuanfa_num'

def transform_comment_content(row,source_id):
    # acc.add(1)
    j = row.asDict()
    content = j.get('内容')
    content = content.replace(u'四强', u'4强')
    content = content.replace(u'八强', u'8强')
    content = content.replace(u'十六强', u'16强')
    content = content.replace(u'三十二强', u'32强')
    content = content.replace(u'第二十九届', u'第29届')        
    comment_num = j.get('评论数')
    list_ = []
    #由于是分布式计算，当前方法，分布到多个task上，同时计算，因此非同一条数据也有可能time.time()的值相同，导致rowkey相同，插入到同一行中，导致多Versions。
    #%d保留整数，则时间相同的会很多，rowkey也会有很多重复的。单机已验证会导致上面的问题。
    #在pycharm中同时执行如下两行代码，结果时间一样，即可验证。
    #print time.time()
    #print time.time()
    #这里不可使用累加器，因为累加器的值，只能在driver上才能取到，因此这里取不到累加器的值，加入到rowkey
    rowkey = u'嫘祖杯%s0000%s' % (source_id, j.get('网址'))      #暂且用网址，网址是唯一的

    for key in j.keys():
        if key == '内容':
                tmp_list = [rowkey,'d',WeiboFields.content,content]
        elif key == '全部评论':
            l = {}
            list_row = j.get('全部评论')
            b = filter_comment(list_row)
            if b :
                ck = 1
                for v in list_row:
                    if not filter_(v['内容']):    #匹配到内容为：,.，。时，将删除该条评论
                        comment_num = str(int(comment_num) - 1)
                    else :
                        vt = v.asDict()
                        t =  {}
                        for k in vt.keys():
                            if k == '点赞数':
                                t.update({WeiboFields.dianzan_num:vt.get(k)})
                            elif k == '内容':
                                t.update({WeiboFields.pinglun_content:vt.get(k)})
                            elif k == '评论人':
                                t.update({WeiboFields.pinglun_user:vt.get(k)})
                            else :
                                return
                        l.update({ck:json.dumps(t)})
                        ck += 1
                tmp_list = [rowkey,'d',WeiboFields.comment,json.dumps(l)]
            else :
                tmp_list = [rowkey,'d',WeiboFields.comment,'']  
        elif key == '评论数' : 
                continue
        elif key == '信息' :
                tmp_json = j.get(key).asDict()
                tmp_json.pop('认证信息','not found')
                tj = {}
                for k in tmp_json.keys():
                    if k == '昵称':
                        tj.update({WeiboFields.name:tmp_json.get(k)})
                    elif k == '关注数':
                        tj.update({WeiboFields.guanzhu:tmp_json.get(k)})
                    elif k == '标签':
                        tj.update({WeiboFields.label:tmp_json.get(k)})  
                    elif k == '认证':
                        tj.update({WeiboFields.renzheng:tmp_json.get(k)})
                    elif k == '粉丝数':
                        tj.update({WeiboFields.fensi:tmp_json.get(k)}) 
                    elif k == '性别':
                        tj.update({WeiboFields.sex:tmp_json.get(k)})
                    elif k == '地区':
                        tj.update({WeiboFields.area:tmp_json.get(k)})
                    elif k == '生日':
                        tj.update({WeiboFields.birth:tmp_json.get(k)})
                    elif k == '简介':
                        tj.update({WeiboFields.desc:tmp_json.get(k)})
                    else :
                        tj.update({WeiboFields.weibo_num:tmp_json.get(k)})
                tmp_list = [rowkey,'d',WeiboFields.info,json.dumps(tj)]
        
        elif key == '发布时间' :
                t_value = j.get(key).split(' ')[0].replace(u'年','-').replace(u'月','-').replace(u'日','')
                tmp_list = [rowkey,'d',WeiboFields.time,t_value]
        elif key == '昵称' :
                tmp_list = [rowkey,'d',WeiboFields.nicheng,j.get(key)]
        elif key == '点赞数' :
                tmp_list = [rowkey,'d',WeiboFields.zan_num,j.get(key)]
        elif key == '网址' :
                tmp_list = [rowkey,'d',WeiboFields.website,j.get(key)]
        elif key == '转发数' :
                tmp_list = [rowkey,'d',WeiboFields.zhuanfa_num,j.get(key)]
        else :
                tmp_list = [rowkey,'d',key,j.get(key)]
        list_.append(tmp_list)
    list_.append([rowkey,'d',WeiboFields.comment_num,comment_num]) 
    #评论数受全部评论的影响，在全部评论中，有对评论数进行减少，因此在最后添加。
    return list_

def filter_comment(comment):
    #comment = row['全部评论']  #filter中不能直接传递row
    #comment结构：[Row(内容="",点赞数="",评论人=""),Row()]
    #过滤commet为空，或不为空，但每个Row的"内容"都类似为，。？，被正则表达式过滤掉。只要有一个Row的内容不为，。？，则会返回true。
    if len(comment) > 0:
        b = False
        for r in comment:
            b = filter_(r['内容'])
            if b:
                break
        if b:
            return b
        else :
            return False
    else :
        return False
def filter_(x):
    #p1 = ur'^[\w,.:;!，。：；！]?$'
    p1 = ur'^[\d,.:;!、，。：；！？?_]*[a-zA-Z]?[\d,.:;!、，。：；！？?_]*$'
    #过滤掉类似：，,.。和 a12,.、和 ？1 ，a 等
    #只要包含汉字或至少两个英文字母，就不会被过滤掉
    pattern1 = re.compile(p1)
    matcher1 = re.match(pattern1,x)
    if not matcher1 :
        return True
    else :
        return False

if __name__ == "__main__":
    if len(sys.argv) > 2:
        host = sys.argv[1]
        hbase_table = sys.argv[2]
    else:
        host = '192.168.10.24'
        hbase_table = 'weibo'
    sparkConf = SparkConf()
    sc = SparkContext(conf=sparkConf)
    sc.setLogLevel("ERROR")  # ALL, DEBUG, ERROR, FATAL, INFO, OFF, TRACE, WARN
    acc = sc.accumulator(0)
    sqlContext = SQLContext(sc)

    #rdd_ = sqlContext.read.json("/user/weiwc/data/test_weibo.txt").distinct().cache()
    rdd_ = sqlContext.read.json("hdfs://cdh-master-slave1:8020/data/public_sentiment/go/2017_05/weibo_list.json").distinct().cache()
    #rdd_hbase = rdd_.rdd.coalesce(3).filter(lambda row :filter_comment(row['全部评论'])).cache() #去重
#    rdd_put = df.rdd.filter(lambda x:filter_(x.tie_content)).flatMap(lambda row : putProducer(row,'05')).cache()  #过滤单个字母、字符；转换：二十九 => 29，并返回存储到Hbase所需的数据格式
    conf = {"hbase.zookeeper.quorum": host,
        "hbase.mapred.outputtable": hbase_table,
        "mapreduce.outputformat.class": "org.apache.hadoop.hbase.mapreduce.TableOutputFormat",
        "mapreduce.job.output.key.class": "org.apache.hadoop.hbase.io.ImmutableBytesWritable",
        "mapreduce.job.output.value.class": "org.apache.hadoop.io.Writable"}
    keyConv = "hbase.pythonconverters.StringToImmutableBytesWritableConverter"
    valueConv = "hbase.pythonconverters.StringListToPutConverter"

    rdd2 = rdd_.rdd.coalesce(3).flatMap(lambda row : transform_comment_content(row,'02')).map(lambda x: (x[0], x)).cache()
    #验证使用time.time()的情况下，rowkey的重复性
    # rdd2_ = rdd_.rdd.coalesce(3).cache()
    # print rdd2_.getNumPartitions()
    # rdd2 = rdd2_.flatMap(lambda row : transform_comment_content(row,'02')).map(lambda x: (x[0],x)).cache()
    # rdd3 = rdd2.groupBy(lambda x:x[0]).cache()
    # # def p(x):
    # #     l= []
    # #     for v in x[1]:
    # #         l.append(v)
    # #     print x[0],l
    # #
    # # rdd3.foreach(lambda x: p(x))
    # # print rdd3.count()
    # print "====================================" + str(rdd3.count())
    # print acc.value
    rdd2.saveAsNewAPIHadoopDataset(conf=conf,keyConverter=keyConv,valueConverter=valueConv)
    #sc.setLogLevel("DEBUG")  # ALL, DEBUG, ERROR, FATAL, INFO, OFF, TRACE, WARN

    sc.stop()
