# -*- coding: utf-8 -*-
######读取Hbase中的原始律师数据，存储到ES，便于排查平台律师数据

from elasticsearch import Elasticsearch
import elasticsearch.helpers
import time
import happybase


es = Elasticsearch( "cdh:cdh@13322.com@cdh5-master-slave1:9200" )

print time.asctime( time.localtime(time.time()) )


conn = happybase.Connection(host='cdh5-master-slave1', port=9090)
t = conn.table('cdh:lawyers-origin')

row_prefix = ""
for a in range(240):
    actions = []
    q = t.scan(row_start=row_prefix, limit=5000) #每5000条会重复第一条，导入ES时会自动覆盖，无影响；
    for k, v in q:
        # print k,v
        tmp_ = {}
        for j in v.keys():
            tmp_.update({j.replace("d:",""):v[j].decode("utf-8")})

        actions.append({
                '_op_type': 'index',
                '_index': "lawyers-origin",
                '_type': "default",
                '_id': k,  # 手动指定_id的值
                '_source': tmp_   #tmp_格式为：{k1:v1,k2:v2}
            })
        row_prefix = k

    try:

        elasticsearch.helpers.bulk(es, actions)
    except Exception:
        print "============a = " + str(a) + " , row_prefix = " + row_prefix
        print Exception.message()

    print time.asctime(time.localtime(time.time()))

