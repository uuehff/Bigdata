# -*- coding: utf-8 -*-
import pymysql
import time

print time.asctime( time.localtime(time.time()) )
# conn=pymysql.connect(host='slave2',user='weiwc',passwd='HHly2017.',db='civil_v2',charset='utf8')
# conn=pymysql.connect(host='172.16.60.14',user='weiwc',passwd='HHly2017.',db='civil_v2',charset='utf8')
conn=pymysql.connect(host='slave2',user='weiwc',passwd='HHly2017.',db='judgment_v2',charset='utf8')
cursor = conn.cursor()

# conn2=pymysql.connect(host='192.168.74.102',user='weiwc',passwd='HHly2017.',db='laws_doc_imp_other',charset='utf8')
# conn2=pymysql.connect(host='192.168.74.102',user='weiwc',passwd='HHly2017.',db='laws_doc_judgment',charset='utf8')
# cursor2 = conn2.cursor()
# sql = 'select uuid from adju_uuid_del03 '   #LOCATE函数，包含||,返回大于0的数值。
del_sql = 'select uuid from judgment_civil'   #LOCATE函数，包含||,返回大于0的数值。
cursor.execute(del_sql)
row_2 = cursor.fetchall()
c = 0
for row in row_2 :
    c += 1
    sql = " delete from judgment_etl_v2 where uuid = '" + row[0] + "' "
    cursor.execute(sql)
    sql = " delete from judgment_etl_v2_court_cate_judge_footer where uuid = '" + row[0] + "' "
    cursor.execute(sql)
    sql = " delete from judgment_etl_v2_field where uuid = '" + row[0] + "' "
    cursor.execute(sql)
    sql = " delete from judgment_etl_v2_lawyer where uuid = '" + row[0] + "' "
    cursor.execute(sql)
    sql = " delete from judgment_etl_v2_organization where uuid = '" + row[0] + "' "
    cursor.execute(sql)
    sql = " delete from judgment_keshihua_only where uuid = '" + row[0] + "' "
    cursor.execute(sql)
    sql = " delete from judgment_visualization_v2_only where uuid = '" + row[0] + "' "
    cursor.execute(sql)
    sql = " delete from judgment_other_fields_v2 where uuid = '" + row[0] + "' "
    cursor.execute(sql)
    sql = " delete from judgment_uuid_law_id_v2 where uuid = '" + row[0] + "' "
    cursor.execute(sql)
    sql = " delete from judgment2_etl_v2 where uuid = '" + row[0] + "' "
    cursor.execute(sql)
    sql = " delete from judgment2_etl_v2_court_cate_judge_footer where uuid = '" + row[0] + "' "
    cursor.execute(sql)
    sql = " delete from judgment2_etl_v2_field where uuid = '" + row[0] + "' "
    cursor.execute(sql)
    sql = " delete from judgment2_etl_v2_lawyer where uuid = '" + row[0] + "' "
    cursor.execute(sql)
    sql = " delete from judgment2_etl_v2_organization where uuid = '" + row[0] + "' "
    cursor.execute(sql)
    sql = " delete from judgment2_keshihua_only where uuid = '" + row[0] + "' "
    cursor.execute(sql)
    sql = " delete from judgment2_visualization_v2_only where uuid = '" + row[0] + "' "
    cursor.execute(sql)
    sql = " delete from judgment2_other_fields_v2 where uuid = '" + row[0] + "' "
    cursor.execute(sql)
    sql = " delete from judgment2_uuid_law_id_v2 where uuid = '" + row[0] + "' "
    cursor.execute(sql)
print c
conn.commit()
cursor.close()
conn.close()
print time.asctime( time.localtime(time.time()) )