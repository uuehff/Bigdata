# -*- coding: utf-8 -*-
import pymysql
import re

import time

print time.asctime( time.localtime(time.time()) )
# for i in range(1,28):
#     num = i * 100000
conn=pymysql.connect(host='192.168.12.34',user='root',passwd='root',db='laws_doc2',charset='utf8')
cursor = conn.cursor()
# sql = 'select uuid,party_info from lawyer_picture where id < 2'   #LOCATE函数，包含||,返回大于0的数值。
sql = 'select id,defendant_company from lawyer_picture where defendant_company is not null and defendant_company != "" and defendant_company like "%单位%" '   #LOCATE函数，包含||,返回大于0的数值。
cursor.execute(sql)
# row_1 = cursor.fetchone()
# row_2 = cursor.fetchmany(5)
row_2 = cursor.fetchall()

import re
for row in row_2 :

        # result= re.split("[" + u"，：。\n\r " + "]+",row[1])    #将当事人信息字段，按，。：换行等等分割
        result = row[1].split("||")
        defendant = []

        for i in result:
            if  i.startswith(u"单位"):
                defendant.append(i[2:])
            else:defendant.append(i)
        defendant = "||".join(defendant)

        sql2 = " update lawyer_picture set defendant_company ='" + defendant + "' where id = '" + str(row[0]) + "'"
        cursor.execute(sql2)
conn.commit()
cursor.close()
conn.close()
print time.asctime( time.localtime(time.time()) )