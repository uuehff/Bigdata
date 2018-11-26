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

for j in range(0,2312):
    print "================" + str(j)

    sql = 'select * from law_area_link where id > ' + str(j*1000)  + ' and id <= ' + str((j+1)*1000) + ''
    cursor.execute(sql)

    row2 = cursor.fetchall()
    package = []


    for i in row2:
        row = {
        "id": i[0],
        "area_id": i[1],
        "area_name": i[2],
        "law_id": i[3],
        "law_doc_url": i[4],
        "state": i[5],
        "cas_tit": i[6],
        "lib_id": i[7],
        "lib_name": i[8],
        "law_key_word": i[9],
        "law_title": i[10],
        "law_doc_num": i[11],
        "eff_gra_1": i[12],
        "eff_gra_2": i[13],
        "sub_cla_1": i[14],
        "sub_cla_2": i[15],
        "sub_cla_3": i[16],
        "sub_cla_4": i[17],
        "pub_date": i[18],
        "imp_date": i[19],
        "html_resource": i[20]
    }
        package.append(row)

    actions = [
        {
            '_op_type': 'index',
            '_index': "cdh-law-area-link-origin",
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