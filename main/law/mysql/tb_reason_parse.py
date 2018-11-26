# -*- coding: utf-8 -*-
import pymysql
import re
import json


court_json = open("E:\\PycharmProjects\\data_etl\\main\\law\mysql\\court_orgin.txt","rb").read()

# print type(eval(court_json))
# for i in eval(court_json):
#     print type(i)
#     print i
# print type(court_json)
# print court_json
# conn=pymysql.connect(host='192.168.12.34',user='root',passwd='root',db='laws_doc',charset='utf8')
# conn=pymysql.connect(host='192.168.12.34',user='root',passwd='root',db='laws_doc',charset='utf8')
# cursor = conn.cursor()
# sql = 'select province,uid from court_city'
# cursor.execute(sql)
# row_1 = cursor.fetchone()
# row_2 = cursor.fetchmany(5)
# row_2 = cursor.fetchall()

# for row in eval(court_json):
#     if row:
#         # sql = "select user,pass from tb7 where user='%s' and pass='%s'" % (user, passwd)
#         sql2 = " insert into tmp_wwc_court (p,i,n) values (%s, %s, %s)"
#         cursor.execute(sql2, (row['p'], row['i'], row['n']))

# for i in range(1,50):
#     s = str(i).zfill(2)

# 为省份添加前缀0：
# for row in row_2:
#         sql2 = " update court_province set uid = '" + str(row[0]).zfill(2) + "' where id = '" + str(row[0]) + "'"
#         cursor.execute(sql2)
# 追加省份数据到court：
# for row in row_2:
#     sql2 = " insert into court (province,uid) values (%s,%s)"
#     cursor.execute(sql2, (row[0], row[1]))

# 更新pid,uid,pid_uid数据到court_city:
# conn=pymysql.connect(host='192.168.12.34',user='root',passwd='root',db='laws_doc',charset='utf8')
# cursor = conn.cursor()
# for i in range(1,32):
#     sql = 'select id,pid from court_city where pid = ' + str(i).zfill(2)
#     cursor.execute(sql)
#     row_2 = cursor.fetchall()
#     # for i2 in range(1,len(row_2)+1):
#     i = 1
#     for row in row_2:
#         sql2 = " update court_city set uid = '" + str(i).zfill(2) + "', pid_uid = '" + row[1] + str(i).zfill(2) + "' where id = '" + str(row[0]) + "'"
#         cursor.execute(sql2)
#         i +=1

# 更新pid,uid,pid_uid数据到court_city:
# conn=pymysql.connect(host='192.168.12.34',user='root',passwd='root',db='laws_doc',charset='utf8')
# cursor = conn.cursor()
# for i in range(1,32):
#     sql = 'select id,pid from court_city where pid = ' + str(i).zfill(2)
#     cursor.execute(sql)
#     row_2 = cursor.fetchall()
#     # for i2 in range(1,len(row_2)+1):
#     i = 1
#     for row in row_2:
#         sql2 = " update court_city set uid = '" + str(i).zfill(2) + "', pid_uid = '" + row[1] + str(i).zfill(2) + "' where id = '" + str(row[0]) + "'"
#         cursor.execute(sql2)
#         i +=1

# 清洗出市，原来只有县级市
conn=pymysql.connect(host='192.168.12.34',user='root',passwd='root',db='laws_doc',charset='utf8')
cursor = conn.cursor()
# sql = "select id,court_new from court_city_null where court_new like '%市%市%' "
sql = "select id,court_new from court_city_null where city = '' and court_new like '%自治区%市%' "
cursor.execute(sql)
row_2 = cursor.fetchall()
# for i2 in range(1,len(row_2)+1):
i = 0
import re
for row in row_2:
    # result = re.split(u"省|市|自治区",row[1])
    result = re.split(u"自治区|市", row[1])
    s = result[1].encode("utf-8") + "市"
    # print row[1]
    # print s
    # i += 1
    sql2 = " update court_city_null set city = '" + s + "' where id = '" + str(row[0]) + "'"
    cursor.execute(sql2)
# print i
conn.commit()
cursor.close()
conn.close()