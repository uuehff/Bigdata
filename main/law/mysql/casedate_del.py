# -*- coding: utf-8 -*-
import pymysql
import re

import time

print time.asctime( time.localtime(time.time()) )
# for i in range(1,28):
#     num = i * 100000
conn=pymysql.connect(host='192.168.12.34',user='root',passwd='root',db='laws_doc_new',charset='utf8')
cursor = conn.cursor()
sql = 'select id,uuid,casedate from judgment_new where casedate != "" and casedate is not null'   #LOCATE函数，包含||,返回大于0的数值。
cursor.execute(sql)
# row_1 = cursor.fetchone()
# row_2 = cursor.fetchmany(5)
row_2 = cursor.fetchall()
import json
def is_valid_date(strdate):
    '''''判断是否是一个有效的日期字符串'''
    try:
        # if ":" in strdate:
        #     time.strptime(strdate, "%Y-%m-%d %H:%M:%S")
        # else:
        time.strptime(strdate, "%Y-%m-%d")
        return False
    except:
        return True
for row in row_2 :
    if is_valid_date(row[2]):
        sql2 = " insert into casedate_validate (id,uuid,casedate) values (%s, %s, %s)"
        cursor.execute(sql2,(row[0],row[1],row[2]))

conn.commit()
cursor.close()
conn.close()
print time.asctime( time.localtime(time.time()) )