# encoding:utf-8
import MySQLdb
import json
import multiprocessing
import numpy as np

con = MySQLdb.connect(host='192.168.12.34', user='liuf', passwd='123456', db='laws_doc', charset='utf8')
cursor = con.cursor()
# sql = "select id,punish_cate,punish_date,delay_date,control_date,lock_date,punish_money,right_date from tmp_liufang" \
#       " where punish_cate='有期徒刑' order by -punish_date desc,-delay_date desc,-punish_money desc,-right_date_num desc"
sql = "select id,punish_cate,punish_date,delay_date,control_date,lock_date,punish_money,right_date from tmp_liufang" \
      " where punish_cate='' order by -delay_date desc,-punish_money desc,-right_date_num desc"
# sql = "select id,punish_cate,punish_date,delay_date,control_date,lock_date,punish_money,right_date from tmp_liufang" \
#       " where punish_cate='管制'"
# sql ="select id,right_date from tmp_liufang"
cursor.execute(sql)
row = cursor.fetchall()
#有期徒刑
# core = np.linspace(60,90,1844263)
# 无期徒刑
# core = np.linspace(90,99,10428)
# 死刑
# core = np.linspace(99,100,3661)
# 管制
# core = np.linspace(57,59,22366)
# 拘役
# core = np.linspace(50,57,734979)
# punish_cate为空
core = np.linspace(40,50,82918)

for n in range(0,len(core)):
    cc = int(core[n] * 10000)
    # print cc
    print row[n][0], cc, row[n][1], row[n][2], row[n][3], row[n][6], row[n][7]
    sql = "update tmp_liufang set degree='%s' where id='%s'" % (cc, row[n][0])
    cursor.execute(sql)
con.commit()









# for i in row:
#     right_date_num = i[1]
#     if i[1] == u'终身':
#         right_date_num = 100
#     sql = "update tmp_liufang set right_date_num='%s' where id='%s'" % (right_date_num, i[0])
#     cursor.execute(sql)
# con.commit()


#     print i[0],i[1],i[2],i[3],i[6],i[7]
