# -*- coding: utf-8 -*-
import os
import sys
from pyspark import SparkContext,SparkConf

import happybase
import json
import logging




# 增、删、查
# table.put(b'row-key', {b'family:qual1': b'value1',
#                        b'family:qual2': b'value2'})
# row = table.row(b'row-key')
# print(row[b'family:qual1'])  # prints 'value1'
#
# for key, data in table.rows([b'row-key-1', b'row-key-2']):
#     print(key, data)  # prints row key and data for each row
#
# for key, data in table.scan(row_prefix=b'row'):
#     print(key, data)  # prints 'value1' and 'value2'
#
# row = table.delete(b'row-key')
# =======================================================
# 针对rowkey使用过滤器，进行查询，正则匹配代码：
# create 'z2','d',SPLITS => ['0_0_2016-03','0_0_2016-06','0_0_2016-09','0_0_2016-12']
# judge_type（判决类型）：
#   判决书：0
# type（审理类型）：
#   一审：0
#   二审：1
#   三审：2
# casedate(判决时间）：
# 例如：2016 - 03 - 16
#    rowkey设计采用：judge_type + type + casedate + uuid, rowkey长度51个字节。

# 查询所有判决书：
# 查询所有判决书中一审：
# 查询所有一审：
# 查询所有判决书一审2016年3月：
# 查询所有2016年3月：
# =======================================================


logger = logging.getLogger(__name__)
# pool = happybase.ConnectionPool(10,host='cdh-slave1',port=9090,timeout=7200000)

# with pool.connection() as connection:



# conn = happybase.Connection(host='cdh-slave1',port=9090,timeout=7200000)
# t = conn.table('public_sentiment')
# t = conn.table('laws_doc:judgment')
# t = conn.table('laws_doc:label2')
# t = conn.table('laws_doc:office')
# t = conn.table('laws_doc:office_save')
# t = conn.table('t5')
# t = conn.table('z2')
# t.put(b'012016-06',{b'd:name':b'好',b'd:address':b'好'})
# t.put(b'012016-0221',{b'd:name':b'好',b'd:address':b'好'})
# t.put(b'012017-01',{b'd:name':b'好',b'd:address':b'好'})
# t = conn.table('t6')
# q = t.scan(row_prefix='嫘祖杯05',limit=5)
# d = 0
# for k,v in q:
#     d +=1
# print d
# t.put(row='hello2',data={'info:id': 'value'})

# q = t.scan(filter="SingleColumnValueFilter('f1','name',!=,'binary:v6',false,false)")
# q = t.scan(filter="RowFilter(>, 'binary:a3')")
# q = t.scan(filter="RowFilter(<, 'binary:c6') AND RowFilter(>, 'binary:a3')")
#
# q = t.scan(filter="RowFilter(=, 'regexstring:1_0$')")   #以1_0 结尾
# q = t.scan(filter="RowFilter(=, 'regexstring:^0_0_2017')")  #rowkey以0_0_2017开头
# 在过滤器中使用：
# >,  'binary:abc' 将匹配所有大于“abc”的字符
# =,  'binaryprefix:abc' 将匹配所有的前3个字母等于“abc”的字符
# !=,  'regexstring:ab*yz' 将匹配不以“ab”打头和以“yz”结尾的字符
# =,  'substring:abc123' 将匹配一切始于substring“abc123”的字符，即包括字符串abc123即可满足条件。
# 1、RowFilter：针对rowkey进行处理过滤
# q = t.scan('a1','a3',filter="RowFilter(=, 'binary:a1')")
# q = t.scan('a1','a3',filter="RowFilter(>, 'binary:a1')")
# =====
# q = t.scan('a1','a3',filter="RowFilter(=, 'binaryprefix:a')")
# q = t.scan('a1','a3',filter="RowFilter(!=, 'binaryprefix:a12')")
# ======
# q = t.scan('a1','a3',filter="RowFilter(=, 'regexstring:[a-z]\d')")
# q = t.scan('a1',filter="RowFilter(=, 'regexstring:[a-z]{2}')")
# q = t.scan('a1',filter="RowFilter(=, 'regexstring:[a-z]\d')")
# q = t.scan('a1',filter="RowFilter(!=, 'regexstring:[a-z]\d')")
# ========
# q = t.scan('a1',filter="RowFilter(=, 'substring:key')")
# q = t.scan('a1',filter="RowFilter(=, 'regexstring:^row-[\d]+')")
#大部分简单查询都可使用：scan(row_prefix = ) 或 t.scan(filter="RowFilter(=, 'substring:_0_')")
# 查询非判决书（或委托书之类，总之第一个字符不为0）中2016年6月：q = t.scan(filter="RowFilter(=, 'regexstring:^[1-9]_[0-3]_2016-06')")
# 查询所有一审：q = t.scan(filter="RowFilter(=, 'substring:_0_')")
# 查询所有2016年6月:   q = t.scan(filter="RowFilter(=, 'substring:2016-06-')")
# q = t.scan(row_prefix='0_0')
# q = t.scan(filter="RowFilter(=, 'substring:2016-06-')")
# q = t.scan(filter="RowFilter(=, 'substring:_0_')")  类似于：t.scan(row_prefix='0_0')
# q = t.scan(filter="SingleColumnValueFilter('d','doc_reason',=,'binary:1')")
# ^[1-9]_[0-3]_2016-06
# q = t.scan(filter="RowFilter(=, 'regexstring:^[0-9]_[1-3]_2016-06')")

# row_prefix="\xE4\xB8\x80\xE5\xAE\xA1_2016-03" 等同于：
# row_prefix="一审_2016-03"

# q = t.scan(row_prefix="0_2014-08",columns=["d:doc_content"],limit=3)
# q = t.scan(row_start="0_2016-02-18",row_stop="0_2016-07-21")
import time

print time.time()
# t = conn.table('laws_doc:judgment')

# t2 = t.batch()

# t = conn.table('laws_doc:office')
# t = conn.table('hbase:meta')
# columns=['d:court_new','d:duration','d:casedate_new','d:law_office','d:court_cate','d:crime_reason','d:fact_finder']
# q = t.scan(limit=10000,columns=['d:court_new','d:duration','d:casedate_new','d:law_office','d:court_cate','d:crime_reason','d:fact_finder'])
# "hbase.mapreduce.scan.row.start":"0_2010-01-04_aec2efe3-a0ff-4479-82da-97cc6529ae18",
#         "hbase.mapreduce.scan.row.stop":"0_2010-01-04_b71f3419-d05b-46d4-8454-1edf4e4d1f76",
# columns=['d:crime_reason','d:defendant_new']
# q = t.scan(row_start='0_2010-01-04_aec2efe3-a0ff-4479-82da-97cc6529ae18',row_stop='0_2010-01-04_b71f3419-d05b-46d4-8454-1edf4e4d1f76',
#            columns=['d:court_new','d:duration','d:casedate_new','d:law_office','d:court_cate','d:crime_reason','d:fact_finder_new'])
# row_start='0_2013-08',row_stop='0_2013-11-09',

conn = happybase.Connection(host='cdh-slave1',port=9090,timeout=7200000)
# conn = happybase.Connection(host='cdh-slave1',port=9090,timeout=7200000)
# pool = happybase.ConnectionPool(10,host='cdh-slave1',port=9090,timeout=7200000)

# with pool.connection() as connection:
#     t = connection.table('laws_doc:judgment')
# t = conn.table('laws_doc:user')
# q = t.scan(filter="RowFilter(<, 'binary:c6') AND RowFilter(>, 'binary:a3')")
# t = conn.table('laws_doc:judgment')
t = conn.table('laws_doc:judgment_all')
# t = conn.table('laws_doc:lawyer')
# t_batch = t.batch()

import time
print time.time()
# 4、ValueFilter（值过滤器）
# q = t.scan(filter="ValueFilter(=, 'binary:value_1')")
# q = t.scan(filter="ValueFilter(=, 'regexstring:[a-z]\d')")
#
# 5、SingleColumnValueFilter （专用过滤器）用一列的值决定是否一行数据是否被过滤
# SingleColumnValueFilter有两个构造函数：4参数和6参数的，6参数多了两个参数：boolean filterIfMissing, boolean latestVersionOnly
# 	filterIfMissing 默认false,意为当不存在指定的 "列族：列"时，是否过滤掉，false不过滤。
# 	latestVersionOnly 默认为true
#
# 使用构造函数1：q = t.scan(filter="SingleColumnValueFilter('f1','name',=, 'binary:v6')")
# 使用构造函数2：q = t.scan(filter="SingleColumnValueFilter('f1','name',!=,'binary:v6',true,true)")
# q = t.scan(row_prefix="0_2014-08",columns=["d:reason"],limit=3)
# t.put('001',data={'d:id': '12345'})
# q = t.scan()
# q = t.scan(row_start="0_2014-04-01",row_stop="0_2014-04-02",filter="QualifierFilter(=, 'binary:doc_content') AND KeyOnlyFilter()")
# q = t.scan(row_start="",row_stop="0_2014-13",filter="QualifierFilter(=, 'binary:doc_content') AND KeyOnlyFilter()")
# q = t.scan(row_start="0_2014-13",filter="QualifierFilter(=, 'binary:plaintiff_new') AND KeyOnlyFilter()")
# 批量删除，要的主要是rowkey,将有uuid的行取出（即全部数据）该行的uuid字段的字段名即‘uuid’,经测试，180万，删除需要5分钟左右。
q = t.scan(filter="KeyOnlyFilter()",limit=10)
# row_start="1971",limit=10
# columns=['d:gender','d:nation','d:edu','d:edu_new','d:suspect_num','d:birth_day','d:native_place','d:age_year','d:crml_team','d:j_adult','d:prvs'],
# filter="QualifierFilter(=, 'binary:uuid') AND KeyOnlyFilter()"
# q = t.scan(row_start="1300000",row_stop="1310100",filter="QualifierFilter(=, 'binary:uuid') AND KeyOnlyFilter()",)  #108570
# q = t.scan(filter="QualifierFilter(=, 'binary:art_digit') AND KeyOnlyFilter()")  #108570
# ["d:title","d:party_info","d:trial_process","d:trial_request","d:trial_reply","d:court_find","d:court_idea","d:judge_result"]
print time.time()
# q = t.scan(columns=["d:title","d:party_info","d:trial_process","d:trial_request","d:trial_reply","d:court_find","d:court_idea","d:judge_result"],row_prefix="2000000")
# q = t.scan(columns=["d:title","d:party_info","d:trial_process","d:trial_request","d:trial_reply","d:court_find","d:court_idea","d:judge_result"],row_prefix="2000000")
# q = t.scan(row_start="1300000",row_stop="1400000")
# gender,nation,edu,edu_new,suspect_num,birth_day,native_place,age_year,crml_team,j_adult,prvs
# q = t.scan(row_start="6",row_stop="601",limit=10)
d = 0

# row = table.row(b'row-key')
# print(row[b'family:qual1'])  # prints 'value1'
#
# for key, data in table.rows([b'row-key-1', b'row-key-2']):
#     print(key, data)  # prints row key and data for each row
# result = t.rows(
#     rows=[b"2400582",b"1399609",b"1399615",b"1399611",b"1399617",b"1399610",b"1399613",b"1399616",b"1399614",b"1399618",b"1399612",b"902203",b"902220",b"902210",b"902224",b"902207",b"902216",b"902222",b"902218",b"902225",b"902213"],
#     columns=[b"d:effective_date",b"d:effective_range"])
# q = t.scan(row_start="1",row_stop="1")

# e = {"a":34,"b":12}
# e.has_key()
# print len(result)


try:
    for k,vs in q:
        print k,vs
        for k1 in vs.keys():
            d += 1
            # print vs[k1]
            print k1
            # print "================"
        # d+=1
        # print type(vs)
        # if vs.has_key('d:update_time') or vs.has_key('d:casedate') or vs.has_key('d:record_time'):
        #     t_batch.delete(k, ['d:update_time', 'd:casedate', 'd:record_time'])
        # print k
        # print v.has_key('d:doc_content')
        # print v.has_key('d:city')
        # if v['d:doc_content'] != '':
        # print k,v['d:doc_content'],"==="
        # update_time，casedate，record_time
        # t.delete(k,['d:update_time','d:casedate','d:record_time'])
        # t_batch.delete(k,['d:effective_range','d:insert_time','d:uuids'])
        # if vs['d:title'] != '':
        #     print vs['d:title']
finally:
    print d
    print time.time()

# 1502871000.42
# 1502871006.86
# print k
    # print v[0],v[1]
    # for i in v.keys():
    #     print i
    # print "====================="
    # print k,v
    # print k,v['d:law_office']
    # print k,v['d:TIME']
    # print k,v['d:PER']
    # d +=1
    # t.delete(k,['d:id'])
#注意：读取评论内容，这里使用汉字“嫘祖杯”或它的字节串都可以！
# for k,v in t.scan(row_prefix="嫘祖杯02",columns=["d:comment"],limit=3):
#     for k2 in v.values():
#         if k2:
#             s = k2.decode("utf-8")
#             print type(s)
#             s3 = json.loads(s)
#             for j in s3.values():
#                 # print type(j)
#                 j2 = json.loads(j)
#                 print j2["pinglun_content"]

#批量删除
# d =  0
# q = t.scan(row_prefix= "嫘祖杯03")
# for k,v in q:
#     t.delete(k)
# print d

# import datetime
# import time
#
#
# def datetime_to_timestamp_in_milliseconds(d):
#     """convert a datetime object to milliseconds since Epoch.
#
#     """
#     return int(time.mktime(d.timetuple()) * 1000)
#
#
# print datetime_to_timestamp_in_milliseconds(datetime.datetime.now())
#
# print time.time()
# print time.time()
# print datetime.datetime.now().microsecond