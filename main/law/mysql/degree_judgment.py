# -*- coding: utf-8 -*-
import pymysql
import re

import time

print time.asctime( time.localtime(time.time()) )
# for i in range(1,28):
#     num = i * 100000
conn=pymysql.connect(host='192.168.12.34',user='root',passwd='root',db='laws_doc',charset='utf8')
cursor = conn.cursor()
sql = 'select id,punish_cate,punish_date,if_delay,delay_date,punish_money from judgment_visualization_v2 where id = 31203 '   #LOCATE函数，包含||,返回大于0的数值。
cursor.execute(sql)
# row_1 = cursor.fetchone()
# row_2 = cursor.fetchmany(5)
row_2 = cursor.fetchall()
import json


# try :
for row in row_2 :

    degree = ""
    if row[1] == u"管制":
        t = 55.0
        tmp = 0.0
        if row[3] == "1":   #缓刑的话，分数应降低
            tmp = -float(row[3])/12.0
        if row[5] and row[5] != "":
            tmp = tmp + float(row[5])/10000.0

        degree = str(int((t + tmp/2) * 100))
    elif row[1] == u"拘役":
        t = 65.0
        tmp = 0.0
        if row[3] == "1":   #缓刑时间越长，减的值就越小
            tmp = -1.0/float(row[4])
        if row[5] and row[5] != "":
            tmp = tmp + float(row[5]) / 10000.0
        degree = str(int((t + tmp/2) * 1000))

    elif row[1] == u"有期徒刑":

        t = 72.0
        tmp = 0.0
        if row[2] and row[2] != "" and row[2] != 'None':
            tmp = float(row[2])/48.0

        if row[3] == "1":  # 缓刑时间越长，减的值就越小
            tmp = -1.0/float(row[4]) + tmp
        if row[5] and row[5] != "":
            tmp = tmp + float(row[5]) / 480000.0
        degree = str(int((t + tmp / 2) * 1000))

    elif row[1] == u"无期徒刑":
        t = 82.0
        tmp = 0.0
        if row[2] and row[2] != "" and row[2] != 'None':
            tmp = float(row[2]) / 48.0

        if row[3] == "1":  # 缓刑时间越长，减的值就越小
            tmp = -1.0 / float(row[4]) + tmp
        if row[5] and row[5] != "":
            tmp = tmp + float(row[5]) / 480000.0
        degree = str(int((t + tmp / 2) * 1000))

    elif row[1] == u"死刑":
        t = 92.0
        tmp = 0.0
        if row[2] and row[2] != "" and row[2] != 'None':
            tmp = float(row[2]) / 48.0

        if row[3] == "1":  # 缓刑时间越长，减的值就越小
            tmp = -1.0 / float(row[4]) + tmp
        if row[5] and row[5] != "":
            tmp = tmp + float(row[5]) / 480000.0
        degree = str(int((t + tmp / 2) * 1000))
    else:    #row[1] == ""
        t = 50.0
        tmp = 0.0
        if row[5] and row[5] != "":
            tmp = tmp + float(row[5]) / 10000.0

        degree = str(int((t + tmp / 2) * 1000))
# finally:
    # print row,row[0]

    sql2 = " update judgment_visualization_v2 set degree='" + degree + "' where id= '" + str(row[0]) + "'"
    cursor.execute(sql2)
conn.commit()
cursor.close()
conn.close()
print time.asctime( time.localtime(time.time()) )