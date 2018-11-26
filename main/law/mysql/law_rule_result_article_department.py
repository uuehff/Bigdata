# -*- coding: utf-8 -*-
import pymysql
import re

import time

print time.asctime( time.localtime(time.time()) )
# for i in range(1,28):
#     num = i * 100000
conn=pymysql.connect(host='192.168.12.35',user='root',passwd='HHly2017.',db='law',charset='utf8')
cursor = conn.cursor()
# sql = 'select uuid,party_info from lawyer_picture where id < 2'   #LOCATE函数，包含||,返回大于0的数值。
# sql = 'select id,department from law_rule_result_article where department is not null and department !="" '
sql = 'select id,department from law_rule_result2 where department is not null and department !="" '
cursor.execute(sql)
# row_1 = cursor.fetchone()
# row_2 = cursor.fetchmany(5)
row_2 = cursor.fetchall()

import re
for row in row_2 :

    # if row[1] and row[1] != "":
        result= re.split("[" + u"，：；。 、" + "]+",row[1])
        depart = []
        for i in result:
            depart.append(i)

        sql2 = " update law_rule_result2 set department ='" + "||".join(depart) + "' where id = '" + str(row[0]) + "'"
        cursor.execute(sql2)
conn.commit()
cursor.close()
conn.close()
print time.asctime( time.localtime(time.time()) )