# -*- coding: utf-8 -*-
import pymysql
import re
import uuid as UUID


conn=pymysql.connect(host='192.168.74.102',user='weiwc',passwd='HHly2017.',db='laws_doc_lawyers_new',charset='utf8')
cursor = conn.cursor()
sql = 'select id from hht_lawyer_all_collect_match_result_id_to_uuid where id >= 400000 and id <= 1000000'
cursor.execute(sql)
row_2 = cursor.fetchall()
cursor2 = conn.cursor()

for row in row_2 :
    id2 = unicode(UUID.uuid3(UUID.NAMESPACE_DNS_LAWYERS,str(row[0])))  # 基于平台的命名空间 + uuid确定新的uuid_,uuid_是一个对象，需要转化为字符串
    sql3 = " update hht_lawyer_all_collect_match_result_id_to_uuid set id2='" + id2 + "' where id= '" + str(row[0]) + "'"
    cursor2.execute(sql3)
    # print sql3
conn.commit()
cursor.close()
conn.close()