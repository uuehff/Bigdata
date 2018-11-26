# -*- coding: utf-8 -*-
import pymysql
import re


conn=pymysql.connect(host='192.168.10.24',user='test',passwd='123456',db='laws_doc',charset='utf8')
cursor = conn.cursor()
sql = 'select uuid,lawlist from judgment where id > 500000 and id <= 2000000'
cursor.execute(sql)
# row_1 = cursor.fetchone()
# row_2 = cursor.fetchmany(5)
row_2 = cursor

for row in row_2 :
    if row:
        # sql = "select user,pass from tb7 where user='%s' and pass='%s'" % (user, passwd)
        sql2 = " update tmp_weiwenchao set lawlist='" + ",".join() + "' where uuid= '" + row[0] + "'"
        effect_row = cursor.execute(sql2)
conn.commit()
cursor.close()
conn.close()