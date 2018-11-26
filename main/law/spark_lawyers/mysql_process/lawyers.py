# -*- coding: utf-8 -*-
import pymysql
import re


conn=pymysql.connect(host='192.168.12.34',user='root',passwd='root',db='laws_doc',charset='utf8')
cursor = conn.cursor()
sql = 'select uuid,lawyer_id from judgment_main_etl where lawyer_id is not null and id >20 '   #LOCATE函数，包含||,返回大于0的数值。
cursor.execute(sql)
# row_1 = cursor.fetchone()
# row_2 = cursor.fetchmany(5)
row_2 = cursor.fetchall()
import json


cursor2 = conn.cursor()
for row in row_2 :
    ids = row[1].split("||")
    orig = []
    for i in ids :
        sql2 = "select lawyer,office from lawyer where id =  " + i
        cursor2.execute(sql2)
        one = cursor2.fetchone()
        orig.append(one[0] + "|" + one[1])
    # print "||".join(orig)
    sql3 = " update judgment_main_etl set lawyer_id='" + "||".join(orig) + "' where uuid= '" + row[0] + "'"
    cursor2.execute(sql3)
conn.commit()
cursor.close()
conn.close()