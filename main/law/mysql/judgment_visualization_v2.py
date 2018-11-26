# -*- coding: utf-8 -*-
import pymysql
import re


conn=pymysql.connect(host='192.168.12.34',user='root',passwd='root',db='laws_doc',charset='utf8')
cursor = conn.cursor()
sql = 'select uuid,plaintiff_info,defendant_info from tmp_lawyers where LOCATE("||",lawyer_id)=0 '   #LOCATE函数，包含||,返回大于0的数值。
cursor.execute(sql)
# row_1 = cursor.fetchone()
# row_2 = cursor.fetchmany(5)
row_2 = cursor.fetchall()
import json

for row in row_2 :
    # print row[0],row[1],row[2]
    law_office = {}
    t = {}
    t2 = {}
    if row[1] and row[1] != '':
        t = json.loads(row[1])
    if row[2] and row[2] != '':
        t2 = json.loads(row[2])
    law_office.update(t)
    law_office.update(t2)
    # if row:
        # sql = "select user,pass from tb7 where user='%s' and pass='%s'" % (user, passwd)
    sql2 = " update tmp_lawyers set law_office='" + "||".join(law_office.values()) + "' where uuid= '" + row[0] + "'"
    effect_row = cursor.execute(sql2)
conn.commit()
cursor.close()
conn.close()