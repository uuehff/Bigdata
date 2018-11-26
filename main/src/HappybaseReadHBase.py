# coding:utf-8
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

conn = happybase.Connection('cdh-slave1')
# t = conn.table('public_sentiment')
# t = conn.table('laws_doc:judgment')
# t = conn.table('laws_doc:label')
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
d = 0
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
# t = conn.table('laws_doc:label')
t = conn.table('laws_doc:judgment_all')
# q = t.scan(filter="RowFilter(<, 'binary:c6') AND RowFilter(>, 'binary:a3')")
import time
print time.time()
q = t.scan(columns=["d:title","d:party_info"],filter="QualifierFilter(!=, 'binary:id') AND KeyOnlyFilter()",limit=10)
# q = t.scan(row_start="1000001",row_stop="1000010")
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
# q = t.scan()
for k,v in q:
    print k,v
    # print k,v['d:TIME']
    # d +=1
    # t.delete(k,['d:id'])
    # t.delete(k)
print time.time()
print d

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