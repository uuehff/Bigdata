# -*- coding: utf-8 -*-
import pymysql
import time

print time.asctime( time.localtime(time.time()) )
# conn=pymysql.connect(host='slave2',user='weiwc',passwd='HHly2017.',db='civil_v2',charset='utf8')
# conn=pymysql.connect(host='172.16.60.14',user='weiwc',passwd='HHly2017.',db='civil_v2',charset='utf8')
conn=pymysql.connect(host='192.168.10.22',user='tzp',passwd='123456',db='laws_doc',charset='utf8')
cursor = conn.cursor()
# sql = 'select uuid from adju_uuid_del03 '   #LOCATE函数，包含||,返回大于0的数值。
sql = 'select uuid_old from adju_uuid_del03 '   #LOCATE函数，包含||,返回大于0的数值。
cursor.execute(sql)
row_2 = cursor.fetchall()
for row in row_2 :
    # sql = " delete from adjudication_civil_uuid_law_id_v2 where uuid = '" + row[0] + "' "
    # sql = " delete from adjudication_civil_etl_v2 where uuid = '" + row[0] + "' "
    # sql = " delete from judgment_new_uuid_law_id_v2_result where uuid = '" + row[0] + "' "
    # sql = " delete from judgment_new_other_fields_v2_result where uuid = '" + row[0] + "' "
    sql = " delete from adjudication where uuid = '" + row[0] + "' "
    cursor.execute(sql)

conn.commit()
cursor.close()
conn.close()
print time.asctime( time.localtime(time.time()) )