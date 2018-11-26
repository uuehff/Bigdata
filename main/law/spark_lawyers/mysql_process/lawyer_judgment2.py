# -*- coding: utf-8 -*-
import pymysql
import re


conn=pymysql.connect(host='192.168.12.34',user='root',passwd='root',db='laws_doc',charset='utf8')

conn2=pymysql.connect(host='192.168.12.34',user='root',passwd='root',db='laws_doc2',charset='utf8')
cursor = conn2.cursor()

sql = 'select uuid,lawyer_id from tmp_lawyers'   #LOCATE函数，包含||,返回大于0的数值。
cursor.execute(sql)
# row_1 = cursor.fetchone()
# row_2 = cursor.fetchmany(5)
row_2 = cursor.fetchall()
import json

cursor2 = conn.cursor()
for row in row_2 :
    lawyer = []
    if row[1] and row[1] != "":
        s = row[1].split("||")
        for i in s:
            sql2 = 'select lawyer from lawyers where id = ' + i
            cursor2.execute(sql2)
            lawyer.append(cursor2.fetchone()[0])

        sql3 = " update tmp_lawyers set lawyer='" + "||".join(lawyer) + "' where uuid= '" + row[0] + "'"
        effect_row = cursor.execute(sql3)
conn.commit()
cursor.close()
conn.close()