# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 15:35:27 2017

@author: Administrator
"""

#根据律师事务所统计结果 mysql
import MySQLdb
import MySQLdb.cursors
import pandas as pd
import json
from datetime import datetime

import sys
from pyspark import SparkContext,SparkConf
from pyspark.sql import SQLContext

# court_new,duration,casedate_new,law_office,court_cate,crime_reason,fact_finder,defendant_new,casedate_new
# [u'court_cate', u'court_new', u'crime_reason', u'duration', u'fact_finder', u'2008-04-25||'])
def extractFields(v):
    li = []
    s = v.split("\n")
    k = ""
    office = ""
    casedate_new = ""

    for i in s:
        t = json.loads(i)
        if "defendant_new" == t['qualifier']:
            k = t['value']
            # if k == '':         #过滤掉defendant_new为‘’的记录
            #     return []
            continue
        if "law_office" == t["qualifier"]:
            office = t['value']
            continue
        if "casedate_new" == t["qualifier"]:
            li.append(t['value'])
            casedate_new = t['value']
            continue
        li.append(t['value'])
    office_last = casedate_new + "||" + office
    li.append(office_last)
    fl = []
    for i in k.split("||"):
        fl.append((i, li))
    return fl

def getResult(kv):
    # casedate_new, court_cate, court_new, duration, fact_finder, id, reason,
    # [u'casedate_new', u'court_cate', u'court_new', u'crime_reason', u'duration', u'fact_finder', u'2008-04-25||']
    k = kv[0]
    v = kv[1]
    # d2.add(1)
    duration_r = {}
    court_cate = {}
    year = {}

    duration_r[u'10天以下'] = 0
    duration_r[u'10-20天'] = 0
    duration_r[u'20-30天'] = 0
    duration_r[u'30-40天'] = 0
    duration_r[u'40-50天'] = 0
    duration_r[u'50-60天'] = 0
    duration_r[u'60-70天'] = 0
    duration_r[u'70-80天'] = 0
    duration_r[u'80-90天'] = 0
    duration_r[u'90-120天'] = 0
    duration_r[u'120天以上'] = 0

    court_cate[u'最高级法院'] = 0
    court_cate[u'高级法院'] = 0
    court_cate[u'中级法院'] = 0
    court_cate[u'基层法院'] = 0

    year[u'2017年'] = 0
    year[u'2016年'] = 0
    year[u'2015年'] = 0
    year[u'2014年'] = 0
    year[u'2013年'] = 0
    year[u'2012年'] = 0
    year[u'2011年'] = 0
    year[u'2010年'] = 0
    year[u'2009年'] = 0
    year[u'2008年'] = 0
    # hbase结果：[u'casedate_new', u'court_cate', u'court_new', u'crime_reason', u'duration', u'fact_finder', u'2008-04-25||']
    reason, court, finder, office = [], [], [], []
    #
    for r in v:
        if r[3] != '':
            reason.append(r[3])
        if r[2] != '':
            court.append(r[2])
        if r[5] != '':
            finder.append(r[5])
        if r[4] != '':
            i = r[4]
            if int(i) > 0 and int(i) <= 10:
                duration_r[u'10天以下'] += 1
            if int(i) > 10 and int(i) <= 20:
                duration_r[u'10-20天'] += 1
            if int(i) > 20 and int(i) <= 30:
                duration_r[u'20-30天'] += 1
            if int(i) > 30 and int(i) <= 40:
                duration_r[u'30-40天'] += 1
            if int(i) > 40 and int(i) <= 50:
                duration_r[u'40-50天'] += 1
            if int(i) > 50 and int(i) <= 60:
                duration_r[u'50-60天'] += 1
            if int(i) > 60 and int(i) <= 70:
                duration_r[u'60-70天'] += 1
            if int(i) > 70 and int(i) <= 80:
                duration_r[u'70-80天'] += 1
            if int(i) > 80 and int(i) <= 90:
                duration_r[u'80-90天'] += 1
            if int(i) > 90 and int(i) <= 120:
                duration_r[u'90-120天'] += 1
            if int(i) > 120:
                duration_r[u'120天以上'] += 1
        if r[1] != '':
            i = r[1]
            if i == u'基层':
                court_cate[u'基层法院'] += 1
            if i == u'中级':
                court_cate[u'中级法院'] += 1
            if i == u'高级':
                court_cate[u'高级法院'] += 1
            if i == u'最高':
                court_cate[u'最高级法院'] += 1
        if r[0] != '':
            t = datetime.strptime(r[0], '%Y-%m-%d')
            t_year = t.year
            # print t_year
            if t_year == 2017:
                year[u'2017年'] += 1
            elif t_year == 2016:
                year[u'2016年'] += 1
            elif t_year == 2015:
                year[u'2015年'] += 1
            elif t_year == 2014:
                year[u'2014年'] += 1
            elif t_year == 2013:
                year[u'2013年'] += 1
            elif t_year == 2012:
                year[u'2012年'] += 1
            elif t_year == 2011:
                year[u'2011年'] += 1
            elif t_year == 2010:
                year[u'2010年'] += 1
            elif t_year == 2009:
                year[u'2009年'] += 1
            elif t_year == 2008:
                year[u'2008年'] += 1
        if r[6].split("||")[1] != '':
            office.append(r[6])

    reason_t = top_list(reason,"reason")
    office_last = top_list(office,"office")
    court_t = top_list(court,"court")
    finder_t = top_list(finder,"finder")

    # for i in court_t:
    #     print type(i),i
    #     print type(court_t),court_t

    court_t = json.dumps(court_t, ensure_ascii=False)
    reason_t = json.dumps(reason_t, ensure_ascii=False)
    finder_t = json.dumps(finder_t, ensure_ascii=False)
    office_last = json.dumps(office_last, ensure_ascii=False)

    # print type(court_t)         #<type 'unicode'>

    year = json.dumps(year, ensure_ascii=False)
    court_cate = json.dumps(court_cate, ensure_ascii=False)
    duration_r = json.dumps(duration_r, ensure_ascii=False)

    # print type(year)    #<type 'unicode'>
    # hbase中对应的字段，其中rowkey对应office：year_ten,duration,court_cat,reason_top,court_top,finder_top
    hl = []
    c = ["year_ten", "court_cate", "court_top", "duration", "finder_top", "reason_top", "office_last"]
    i = 0
    d = "d"
    for v in [year, court_cate, court_t, duration_r, finder_t, reason_t, office_last]:
        t = (k, [k, d, c[i], v])
        hl.append(t)
        i += 1
    return hl

def filter_K_Null(x):
    if x[0] != '':
        return True
    else:
        return False
import re

def top_list(data,column):
    if data:
        if column == "reason":
            rl = []
            for i in data:
                l = list(eval(i))
                for j in l:
                    rl.append(j.decode("utf8"))
            print len(rl),type(rl[0]),rl[0]
            # for i in data:
            #     for j in i.split(','):
            #         if j != '':
            #             rl.append(j)
            # di = pd.Series(rl).value_counts()[:10].to_dict()
            # for i in di.keys():         #di的key为unicode，value为int64，需要将int64转为int，才可执行json.dumps()
            #     di[i] = int(di[i])
            # return di
            return rl
        elif column == "office":
            di = pd.Series(data).value_counts()[:1].to_dict()
            for i in di.keys():  # di的key为unicode，value为int64，需要将int64转为int，才可执行json.dumps()
                di[i] = int(di[i])
            return di
        else:
            cl = []
            for i in data:
                for j in i.split('||'):
                    if j != '':
                        cl.append(j)
            di = pd.Series(cl).value_counts()[:10].to_dict()
            for i in di.keys():  # di的key为unicode，value为int64，需要将int64转为int，才可执行json.dumps()
                di[i] = int(di[i])
            return di
    else:
        return {}

    # court_list = court_list.value_counts()[:2]       #value_counts类似spark的countByValue算子，默认使用降序排序sort = True, ascending = False,
    # >> > sorted(sc.parallelize([1, 2, 1, 2, 2], 2).countByValue().items())
    # [(1, 2), (2, 3)]
def p(x):
    # print type(x)
    print x
    # print x[1][0],x[1][1],x[1][2],x[1][3]
    # for i in x[1]:
    #     print i


if __name__ == '__main__':
    if len(sys.argv) > 2:
        host = sys.argv[1]
        hbase_table = sys.argv[2]
    else:
        host = '192.168.10.24'
        hbase_table_read = 'laws_doc:judgment'
        # hbase_table_read = 'laws_doc:office'
    # 测试top_list
    # a = ["尤增良1","尤增良2","尤增良3","尤增良5","尤增良1","尤增良2","尤增良4","尤增良3","尤增良3","尤增良3","尤增良2"]
    # b = top_list(a)
    # for k in b.keys():
    #     print k,b[k]

    conf = SparkConf().setMaster("local[6]").setAppName("office")
    sc = SparkContext(conf=conf)
    sc.setLogLevel("ERROR")
    sqlContext = SQLContext(sc)

    rkeyConv = "hbase.pythonconverters.ImmutableBytesWritableToStringConverter"
    rvalueConv = "hbase.pythonconverters.HBaseResultToStringConverter"

    rconf = {
        "hbase.zookeeper.quorum": host,
        "hbase.mapreduce.inputtable": hbase_table_read,


        "hbase.mapreduce.scan.row.start":"0_2010-01-04_aec2efe3-a0ff-4479-82da-97cc6529ae18",
        "hbase.mapreduce.scan.row.stop":"0_2010-01-04_b71f3419-d05b-46d4-8454-1edf4e4d1f76",
        # "hbase.mapreduce.scan.row.stop":"0_2010-01-07_5f2fb58c-7c4a-4a4f-bf37-573690907859",
        # ['d:court_new', 'd:duration', 'd:casedate_new', 'd:law_office', 'd:court_cate', 'd:crime_reason', 'd:fact_finder']
        # hbase.mapreduce.scan.column.family
        "hbase.mapreduce.scan.columns":"d:court_new d:duration d:casedate_new d:law_office d:court_cate d:crime_reason d:fact_finder_new d:casedate_new d:defendant_new"
        # "hbase.mapreduce.scan.columns":"d:crime_reason"
        # hbase.mapreduce.scan.timestamp
        #     hbase.mapreduce.scan.timerange.start
        # hbase.mapreduce.scan.timerange.end
        #     hbase.mapreduce.scan.maxversions
        # hbase.mapreduce.scan.cacheblocks
        #     hbase.mapreduce.scan.cachedrows
        # hbase.mapreduce.scan.batchsize
    }
    result = sc.newAPIHadoopRDD(
        "org.apache.hadoop.hbase.mapreduce.TableInputFormat",
        "org.apache.hadoop.hbase.io.ImmutableBytesWritable",
        "org.apache.hadoop.hbase.client.Result",
        keyConverter=rkeyConv,
        valueConverter=rvalueConv,
        conf=rconf
    )
    # result.foreach(lambda x:p(x))
    # data = result.flatMapValues(lambda v: v.split("\n")).foreach(lambda x:p(x))
    # 天津瑞宇律师事务所    2016 - 02 - 18, 基层, 天津市滨海新区人民法院, 16, 尤增良, 6, 诈骗
    # .filter(lambda x: filter_K_Null(x))
    data = result.flatMap(lambda v: extractFields(v[1])).groupByKey() \
        .flatMap(lambda kv:getResult(kv)).sortByKey().foreach(lambda x:p(x))
        # .mapValues(json.loads).cache()         #注释掉，dataframe才有完整结构


    # casedate_new, court_cate, court_new, duration,fact_finder,id, law_office, reason,
    # id, court_new, duration, casedate_new, law_office, court_cate, reason, fact_finder
    # +------------+------------+--------------------+-------------+----+-------------+
    # | columnFamily | qualifier | row | timestamp | type | value |
    # +------------+------------+--------------------+-------------+----+-------------+
    # | d | casedate_new | 0_2016 - 02 - 18_f998... | 1500983549797 | Put | 2016 - 02 - 18 |
    # | d | court_cate | 0_2016 - 02 - 18_f998... | 1500983549797 | Put | 基层 |
    # | d | court_new | 0_2016 - 02 - 18_f998... | 1500983549797 | Put | 天津市滨海新区人民法院 |

    # tt = sqlContext.jsonRDD(data.values()).select("row","qualifier","value").groupBy()
    # tt.show()
    # tt.printSchema()
    # print ps_data1
    # ps_data1 = ps_data.map(lambda x:(x[1]))
    # hbase_table_save = 'laws_doc:office_save'
    # conf = {"hbase.zookeeper.quorum": host,
    #         "hbase.mapred.outputtable": hbase_table_save,
    #         "mapreduce.outputformat.class": "org.apache.hadoop.hbase.mapreduce.TableOutputFormat",
    #         "mapreduce.job.output.key.class": "org.apache.hadoop.hbase.io.ImmutableBytesWritable",
    #         "mapreduce.job.output.value.class": "org.apache.hadoop.io.Writable"}
    #
    # keyConv = "hbase.pythonconverters.StringToImmutableBytesWritableConverter"
    # valueConv = "hbase.pythonconverters.StringListToPutConverter"
    #
    # data.saveAsNewAPIHadoopDataset(conf=conf, keyConverter=keyConv, valueConverter=valueConv)
    sc.stop()

