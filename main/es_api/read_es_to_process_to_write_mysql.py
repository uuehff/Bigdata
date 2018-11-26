# -*- coding: utf-8 -*-
from elasticsearch import Elasticsearch
import elasticsearch.helpers
import time
import pymysql

# es = Elasticsearch( "cdh:cdh@13322.com@cdh5-master-slave1:9200" )
es = Elasticsearch( "cdh:cdh@13322.com@cdh5-slave2:9200" )

# print time.asctime( time.localtime(time.time()) )

conn=pymysql.connect(host='cdh5-slave3',user='weiwc',passwd='HHly2017.',db='law_v2',charset='utf8')
cursor = conn.cursor()

print time.asctime( time.localtime(time.time()) )

for j in range(0,533):
    print "================" + str(j)

    sql = 'select * from law_link where id > ' + str(j*500)  + ' and id <= ' + str((j+1)*500) + ''
    cursor.execute(sql)

    row2 = cursor.fetchall()
    package = []


    for i in row2:
        row = {
        "id": i[0],
        "law_id": i[1],
        "law_doc_url": i[2],
        "state": i[3],
        "cas_tit": i[4],
        "lib_id": i[5],
        "lib_name": i[6],
        "law_key_word": i[7],
        "law_title": i[8],
        "law_doc_num": i[9],
        "eff_gra_1": i[10],
        "eff_gra_2": i[11],
        "sub_cla_1": i[12],
        "sub_cla_2": i[13],
        "sub_cla_3": i[14],
        "sub_cla_4": i[15],
        "pub_date": i[16],
        "imp_date": i[7],
        "html_resource": i[18]
    }
        package.append(row)

    actions = [
        {
            '_op_type': 'index',
            '_index': "cdh-law-link-origin",
            '_type': "default",
            '_id':d['id'],    #手动指定_id的值
            '_source': d
        }
        for d in package
    ]

    try:
        elasticsearch.helpers.bulk(es, actions )
    except:
        pass
        # print row

    print time.asctime( time.localtime(time.time()) )

print time.asctime( time.localtime(time.time()) )