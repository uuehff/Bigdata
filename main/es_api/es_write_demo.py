# -*- coding: utf-8 -*-
#demo: https://www.cnblogs.com/yxpblog/p/5141738.html
# https://blog.csdn.net/huochen1994/article/details/51324578

from datetime import datetime
from elasticsearch import Elasticsearch
import elasticsearch.helpers
import random

es = Elasticsearch( "cdh5-master-slave1:9200" )
package = []
for i in range( 10 ):
    row = {
        "@timestamp":datetime.now().strftime( "%Y-%m-%dT%H:%M:%S.000+0800" ),
        "http_code" : "404",
        "count" : random.randint(  1, 100 )
    }
    package.append( row )

actions = [
    {
        '_op_type': 'index',
        '_index': "http_code",
        '_type': "error_code",
        '_source': d
    }
    for d in package
]

elasticsearch.helpers.bulk( es, actions )