# -*- coding: utf-8 -*-
from elasticsearch import Elasticsearch
import elasticsearch.helpers
import time
import pymysql
import json

# es = Elasticsearch( "cdh:cdh@13322.com@cdh5-master-slave1:9200" )
es = Elasticsearch( "cdh:cdh@13322.com@cdh5-slave2:9200" )

# print time.asctime( time.localtime(time.time()) )

conn=pymysql.connect(host='cdh5-slave3',user='weiwc',passwd='HHly2017.',db='law_v2',charset='utf8')
cursor = conn.cursor()

print time.asctime( time.localtime(time.time()) )

# search(self, index=None, doc_type=None, body=None, params=None)
with open("query/query_sql",'r') as load_f:
    body = json.load(load_f)['law_link_sql']


# ["id","law_id","law_doc_url","html_resource"]
# _source = ["id","law_id","law_doc_url","html_resource"]


#当使用_source参数时，_source参数会覆盖body参数中设置的_source值；
result = es.search(index="cdh-law-link",body=body)

# 输出查询到的结果
# batch = []
# sql = " insert into svd01 (id,law_id,law_doc_url,html_resource) values (%s, %s, %s, %s)"
for hit in result['hits']['hits']:
    record = (hit['_source']['id'],hit['_source']['law_id'],hit['_source']['law_doc_url'],hit['_source']['html_resource'])
    print record[0]
#     batch.append(record)
#     if len(batch) == 500:
#         cursor.executemany(sql,batch)
#         batch = []
# cursor.executemany(sql,batch)

print time.asctime( time.localtime(time.time()) )


