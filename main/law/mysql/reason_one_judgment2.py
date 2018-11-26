# -*- coding: utf-8 -*-
import pymysql
import re

import time

print time.asctime( time.localtime(time.time()) )
# for i in range(1,28):
#     num = i * 100000
conn=pymysql.connect(host='192.168.12.34',user='root',passwd='root',db='laws_doc2',charset='utf8')
cursor = conn.cursor()
sql = 'select uuid,reason_uid from judgment2_main_etl '   #LOCATE函数，包含||,返回大于0的数值。
cursor.execute(sql)
# row_1 = cursor.fetchone()
# row_2 = cursor.fetchmany(5)
row_2 = cursor.fetchall()
import json

reason = {u'1001':u'危害国家安全',
          u'1002':u'危害公共安全',
          u'1003':u'破坏社会主义市场经济秩序',
          u'1004':u'侵犯公民人身权利、民主权利',
          u'1005':u'侵犯财产',
          u'1006':u'妨害社会管理秩序',
          u'1007':u'危害国防利益',
          u'1008':u'贪污贿赂',
          u'1009':u'渎职',
          u'1010':u'军人违反职责'}

for row in row_2 :

    if row[1] and row[1] != "":

        reason_uid = []
        for i in row[1].split("||"):
            if len(i) == 4:
                reason_uid.append(i)

        data = []
        for j in reason_uid:
            data.append(reason.get(j))

        sql2 = " update lawyer_picture set reason_one ='" + "||".join(data) + "' where uuid = '" + str(row[0]) + "'"
        cursor.execute(sql2)
conn.commit()
cursor.close()
conn.close()
print time.asctime( time.localtime(time.time()) )