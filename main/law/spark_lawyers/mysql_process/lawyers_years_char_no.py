# -*- coding: utf-8 -*-
import pymysql
import re


conn=pymysql.connect(host='192.168.12.34',user='root',passwd='root',db='laws_doc',charset='utf8')
cursor = conn.cursor()
# sql = 'select uuid,plaintiff_info,defendant_info from tmp_lawyers where LOCATE("||",lawyer_id)=0 '   #LOCATE函数，包含||,返回大于0的数值。
# cursor.execute(sql)
# row_1 = cursor.fetchone()
# row_2 = cursor.fetchmany(5)
# row_2 = cursor.fetchall()
import json


file = open("E:\data\lawers.txt")
# lines = file.readlines(2)
for line in file:
    if line and line != "":
        x = json.loads(line)
        l = []
        for i in x.keys():
            if i == 'char_no':
                l.append(x[i])

            elif i == 'law_name':
                s = x[i]
                if x[i][2] == u'省' or x[i][2] == u'市' or x[i][2] == u'县':  # 同一律师名字下，将第三个字为省、市、县去掉。
                    t = []
                    for j in range(0, len(x[i])):
                        if j == 2:
                            continue
                        t.append(x[i][j])
                    s = "".join(t)

                s = s.replace(u"律师事务所", "")  # 统一将结尾处理为律师事务所,去重
                s = s.replace(u"事务所", "")
                s = s + u"律师事务所"
                l.append(s)
            elif i == 'name' :
                name = x[i]
                if x[i].startswith(u"一"):
                    name = x[i][1:]
                l.append(name)
            elif i == 'years':
                years = '2018'
                if x[i] and x[i] != '':
                    years = str(2018-int(x[i]))
                l.append(years)
    try :
        #跳过唯一索引引起的报错
        sql2 = " insert ignore into lawyers_ (char_no,law_office,lawyer,years) values (%s, %s, %s, %s)"
        cursor.execute(sql2,l)
    finally:
        pass

        # print "||".join(l)
        # print line
    # print

file.close()

# for row in row_2 :
#     # print row[0],row[1],row[2]
#     law_office = {}
#     t = {}
#     t2 = {}
#     if row[1] and row[1] != '':
#         t = json.loads(row[1])
#     if row[2] and row[2] != '':
#         t2 = json.loads(row[2])
#     law_office.update(t)
#     law_office.update(t2)
#     # if row:
#         # sql = "select user,pass from tb7 where user='%s' and pass='%s'" % (user, passwd)
#     sql2 = " update tmp_lawyers set law_office='" + "||".join(law_office.values()) + "' where uuid= '" + row[0] + "'"
#     effect_row = cursor.execute(sql2)
conn.commit()
cursor.close()
conn.close()