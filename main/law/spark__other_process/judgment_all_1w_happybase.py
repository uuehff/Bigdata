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
t2 = conn.table('laws_doc:judgment_all_1w')

print time.asctime( time.localtime(time.time()) )
#读取judgment_all一万条，写入judgment_all_1w来测试
d = 0
q = t.scan(limit=10)
d2 = 0
# 插入所有字段

try:
    with t2.batch(batch_size=10000) as t_batch:
        for k, v in q:
            # print k,v
            d +=1
            data = {}
            for k1 in v.keys():
                data.update({k1:v[k1]})
            t_batch.put(k, data=data)
            # if v.has_key("d:defendant_company"):   #387
            #     d +=1
    raise ValueError("Something went wrong!")  #此句写在with语句的代码块里，抛出异常，except截获，不要写在for循环里，否则循环直接结束。
except ValueError:
    pass
finally:
    print d
    print d2
    print time.asctime( time.localtime(time.time()) )



