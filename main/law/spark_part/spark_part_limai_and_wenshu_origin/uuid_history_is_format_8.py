# -*- coding: utf-8 -*-
import pymysql
import re


conn=pymysql.connect(host='192.168.12.34',user='root',passwd='root',db='laws_doc2',charset='utf8')
cursor = conn.cursor()
sql = 'select a.uuid,a.history_new,b.uuid_history from uuid_history a, uuid_history_result b where a.uuid = b.uuid'
cursor.execute(sql)
# row_1 = cursor.fetchone()
# row_2 = cursor.fetchmany(5)
row_2 = cursor.fetchall()

for row in row_2 :
    if len(row[1].split("||")) != len(row[2].split("||")):
        # sql = "select user,pass from tb7 where user='%s' and pass='%s'" % (user, passwd)
        sql2 = " update uuid_history_result set is_format ='8' where uuid= '" + row[0] + "'"
        effect_row = cursor.execute(sql2)
conn.commit()
cursor.close()
conn.close()