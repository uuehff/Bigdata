# -*- coding: utf-8 -*-
import os
import sys
from pyspark import SparkContext,SparkConf

import happybase
import json
import logging
import time

import pymysql
logger = logging.getLogger(__name__)

conn = happybase.Connection(host='cdh-slave1',port=9090,timeout=7200000)
t = conn.table('laws_doc:judgment_all')
# t = t.batch()
# t2 = conn.table('laws_doc:judgment_all_1w')
# t2 = t2.batch()

print time.asctime( time.localtime(time.time()))
#读取judgment_all一万条，写入judgment_all_1w来测试
# d = 0
# q = t.scan(row_start="00c035f9-2117-41e4-8160-56fe7c935ef9",row_stop="00c035f9-2117-41e4-8160-56fe7c935ef9",limit=10000)
# d2 = 0
# 插入所有字段
# s  = t.scan(row_start="5859fbc76d76af20083f30bd",row_stop="5859fbc76d76af20083f30bd")
# for k,v in s:
#     print k,v

conn=pymysql.connect(host='192.168.12.34',user='root',passwd='root',db='laws_doc2',charset='utf8')
cursor = conn.cursor()
sql = 'select uuid from judgment2 where is_format != 1 '   #LOCATE函数，包含||,返回大于0的数值。
cursor.execute(sql)
row_2 = cursor.fetchall()
#
for row in row_2:
    t.delete(row[0])
t.send()

# conn.commit()
# cursor.close()
# conn.close()
print time.asctime( time.localtime(time.time()) )



