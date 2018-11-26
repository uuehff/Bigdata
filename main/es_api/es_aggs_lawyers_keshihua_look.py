# -*- coding: utf-8 -*-
from elasticsearch import Elasticsearch
import elasticsearch.helpers
import time
import pymysql
import json

es = Elasticsearch( "cdh:cdh@13322.com@cdh5-slave2:9200" )

#合并两个字典，相同key的元素，value相加；
def merje_json(dica,dicb):
    dic = {}
    for key in dica:
        if dicb.get(key):
            dic[key] = dica[key] + dicb[key]
        else:
            dic[key] = dica[key]
    for key in dicb:
        if dica.get(key):
            pass
        else:
            dic[key] = dicb[key]

    return dic

print time.asctime( time.localtime(time.time()) )

# search(self, index=None, doc_type=None, body=None, params=None)
with open("query/query_sql",'r') as load_f:
    query_sql = json.load(load_f)
    wenshu_body = query_sql['lawyer_keshihua_look']
    lawyer_body = query_sql['get_lawyer_name']

# wenshu_body.update()
lawyer_body.update()


#获取当前律师自己的姓名，在合作律师中进行删除，但当前律师代理的公司，没有在合作公司中删除，（因此合作公司=律师自己代理的公司+和自己代理的公司合作的公司）
lawyer_name = es.search(index="lawyer_v4",body=lawyer_body)['hits']['hits'][0]['_source']['name']

#当使用_source参数时，_source参数会覆盖body参数中设置的_source值；
result = es.search(index="laws",body=wenshu_body)

#作为原告时的合作律师
aggs_plaintiff_id_plaintiffs = {}
for i in result['aggregations']['aggs_plaintiff_id'][u'合作律师']['buckets']:
    aggs_plaintiff_id_plaintiffs.update({i['key']:i['doc_count']})

#作为被告时的合作律师
aggs_defendant_id_plaintiffs = {}
for j in result['aggregations']['aggs_defendant_id'][u'合作律师']['buckets']:
    aggs_defendant_id_plaintiffs.update({j['key']:j['doc_count']})

#作为原告时的合作公司
aggs_plaintiff_id_org_plaintiffs = {}
for m in result['aggregations']['aggs_plaintiff_id'][u'合作公司']['buckets']:
    aggs_plaintiff_id_org_plaintiffs.update({m['key']:m['doc_count']})

#作为被告时的合作公司
aggs_defendant_id_org_plaintiffs = {}
for n in result['aggregations']['aggs_defendant_id'][u'合作公司']['buckets']:
    aggs_defendant_id_org_plaintiffs.update({n['key']:n['doc_count']})



#作为原告时的对垒律师
aggs_plaintiff_id_defendants = {}
for i0 in result['aggregations']['aggs_plaintiff_id'][u'对垒律师']['buckets']:
    aggs_plaintiff_id_defendants.update({i0['key']:i0['doc_count']})
#作为被告时的对垒律师
aggs_defendant_id_defendants = {}
for j0 in result['aggregations']['aggs_defendant_id'][u'对垒律师']['buckets']:
    aggs_defendant_id_defendants.update({j0['key']:j0['doc_count']})

#作为原告时的对垒公司
aggs_plaintiff_id_org_defendants = {}
for m0 in result['aggregations']['aggs_plaintiff_id'][u'对垒公司']['buckets']:
    aggs_plaintiff_id_org_defendants.update({m0['key']:m0['doc_count']})
#作为被告时的对垒公司
aggs_defendant_id_org_defendants = {}
for n0 in result['aggregations']['aggs_defendant_id'][u'对垒公司']['buckets']:
    aggs_defendant_id_org_defendants.update({n0['key']:n0['doc_count']})


#对结果按count进行排序
#合作律师,按count降序
plaintiffs = merje_json(aggs_plaintiff_id_plaintiffs,aggs_defendant_id_plaintiffs)
#删除当前律师名
del plaintiffs[lawyer_name]

if plaintiffs:
    plaintiffs = sorted(plaintiffs.items(),key=lambda x:x[1],reverse = True)

#合作公司,按count降序
org_plaintiffs = merje_json(aggs_plaintiff_id_org_plaintiffs,aggs_defendant_id_org_plaintiffs)
if org_plaintiffs:
    org_plaintiffs = sorted(org_plaintiffs.items(),key = lambda x:x[1],reverse = True)

#对垒律师,按count降序
defendants = merje_json(aggs_plaintiff_id_defendants,aggs_defendant_id_defendants)
if defendants:
    defendants = sorted(defendants.items(),key = lambda x:x[1],reverse = True)

#对垒公司,按count降序
org_defendants = merje_json(aggs_plaintiff_id_org_defendants,aggs_defendant_id_org_defendants)
if org_defendants:
    org_defendants = sorted(org_defendants.items(),key = lambda x:x[1],reverse = True)
print "==================合作律师如下:"
for a in plaintiffs:
    print a[0] + " : " + str(a[1])

print "====================对垒律师如下:"
for b in defendants:
    print b[0] + " : " + str(b[1])

print "====================合作公司如下:"
for c in org_plaintiffs:
    print c[0] + " : " + str(c[1])

print "====================对垒公司如下:"
for d in org_defendants:
    print d[0] + " : " + str(d[1])


print time.asctime( time.localtime(time.time()) )



