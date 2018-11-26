# -*- coding: utf-8 -*-
from elasticsearch import Elasticsearch
import elasticsearch.helpers
import time
import pymysql

es = Elasticsearch( "cdh:cdh@13322.com@cdh5-master-slave1:9200" )

print time.asctime( time.localtime(time.time()) )

conn=pymysql.connect(host='cdh5-slave2',user='weiwc',passwd='HHly2017.',db='laws_doc_adjudication',charset='utf8')
cursor = conn.cursor()
sql = 'select * from es_adjudication_civil_etl_v2_100 '   #LOCATE函数，包含||,返回大于0的数值。
cursor.execute(sql)

row2 = cursor.fetchall()


print time.asctime( time.localtime(time.time()) )
package = []

for i in row2:
    row = {
        "id": i[0],
        "uuid_old": i[1],
        "party_info": i[2],
        "trial_process": i[3],
        "trial_request": i[4],
        "court_find": i[5],
        "court_idea": i[6],
        "judge_result": i[7],
        "doc_footer": i[8],
        "court": i[9],
        "caseid": i[10],
        "uuid": i[11],
        "title": i[12],
        "lawlist": i[13],
        "reason_type": i[14],
        "type": i[15],
        "judge_type": i[16],
        "law_id": i[17],
        "reason": i[18],
        "reason_uid": i[19],
        "casedate": i[20],
        "province": i[21],
        "court_uid": i[22]
    }
    package.append(row)

actions = [
    {
        '_op_type': 'index',
        '_index': "cdh-doc",
        '_type': "civil",
        '_id':d['id'],    #手动指定_id的值
        '_source': d
    }
    for d in package
]

try:

    elasticsearch.helpers.bulk(es, actions )
except:
    print row

print time.asctime( time.localtime(time.time()) )