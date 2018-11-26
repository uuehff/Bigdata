# -*- coding: utf-8 -*-
import pymysql
import time

print time.asctime( time.localtime(time.time()) )
# conn=pymysql.connect(host='slave2',user='weiwc',passwd='HHly2017.',db='civil_v2',charset='utf8')
# conn=pymysql.connect(host='172.16.60.14',user='weiwc',passwd='HHly2017.',db='civil_v2',charset='utf8')
conn=pymysql.connect(host='192.168.74.102',user='weiwc',passwd='HHly2017.',db='docs_count',charset='utf8')
cursor = conn.cursor()

# conn2=pymysql.connect(host='192.168.74.102',user='weiwc',passwd='HHly2017.',db='laws_doc_imp_other',charset='utf8')
conn2=pymysql.connect(host='192.168.74.100',user='weiwc',passwd='HHly2017.',db='laws_doc_22',charset='utf8')
cursor2 = conn2.cursor()
# sql = 'select uuid from adju_uuid_del03 '   #LOCATE函数，包含||,返回大于0的数值。
del_sql = 'select uuid from judgment_civil'   #LOCATE函数，包含||,返回大于0的数值。
cursor.execute(del_sql)
row_2 = cursor.fetchall()
c = 0
for row in row_2 :
    c += 1
    sql = " delete from judgment where uuid = '" + row[0] + "' "
    print cursor2.execute(sql)
    sql = " delete from judgment2 where uuid = '" + row[0] + "' "
    print cursor2.execute(sql)
print c
conn.commit()
cursor.close()
conn.close()
print time.asctime( time.localtime(time.time()) )