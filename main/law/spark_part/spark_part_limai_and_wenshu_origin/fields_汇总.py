# -*- coding: utf-8 -*-
import pymysql
import re


conn=pymysql.connect(host='192.168.12.34',user='root',passwd='root',db='laws_doc2',charset='utf8')
cursor = conn.cursor()
# tmp_wxy_sql = "select COLUMN_NAME from INFORMATION_SCHEMA.Columns where table_name = 'tmp_wxy' and table_schema='laws_doc2'"
# tmp_raolu_sql = "select COLUMN_NAME from INFORMATION_SCHEMA.Columns where table_name = 'tmp_raolu' and table_schema='laws_doc2'"
# tmp_hzj_sql = "select COLUMN_NAME from INFORMATION_SCHEMA.Columns where table_name = 'tmp_hzj' and table_schema='laws_doc2'"
judgment_etl_sql = "select COLUMN_NAME from INFORMATION_SCHEMA.Columns where table_name = 'judgment2_etl' and table_schema='laws_doc2'"
# judgment2_etl_sql = "select COLUMN_NAME from INFORMATION_SCHEMA.Columns where table_name = 'tmp_hzj' and table_schema='laws_doc2'"
cursor.execute(judgment_etl_sql)
# row_1 = cursor.fetchone()
# row_2 = cursor.fetchmany(5)
row_2 = cursor.fetchall()
fields= []
for row in row_2 :
    fields.append(row[0].encode("utf-8"))
print ",".join(fields)

conn.commit()
cursor.close()
conn.close()