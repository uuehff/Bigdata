# -*- coding: utf-8 -*-
import pymysql
import re


conn=pymysql.connect(host='192.168.12.34',user='root',passwd='root',db='laws_doc',charset='utf8')
cursor = conn.cursor()
sql = 'select id,char_no,gender,pra_type,first_pra_time from lawyers_new where char_no is not null and char_no != "" and CHAR_LENGTH(char_no) = 17'   #LOCATE函数，包含||,返回大于0的数值。
cursor.execute(sql)
# row_1 = cursor.fetchone()
# row_2 = cursor.fetchmany(5)
row_2 = cursor.fetchall()
import json

for row in row_2 :
    pra_types = {1:ur"专职律师",2:ur"兼职律师",3:ur"香港居民律师",4:ur"澳门居民律师",5:ur"台湾居民律师",6:ur"公职律师",
            7:ur"公司律师",8:ur"法律援助律师",9:ur"军队律师"}
    s = row[1]
    pra_type = ""
    if not row[3] or row[3] == "":
        if int(s[9]) >= 1 and int(s[9]) <= 9:    #排除key不存在的情况
            pra_type = pra_types[int(s[9])]
    else:pra_type =row[3]

    if s[10] == "0":gender = u"男"
    else:gender = u"女"

    if not row[4] or row[4] == "":
        first_pra_time = s[6:10]
    else:first_pra_time = row[4]

# sql3 = "update lancome15_order_online set statstatus=11 where oid = '%s' and uid = '%s' and gid = '%s' and ogn = %d "  % ( goid, guid, ggid, gogn)
# sql2 = " select * from lancome15_order_online where otime <='%s' and uid = '%s' and gid = '%s' and ogn >= %d and amount >= \
               # %d order by otime desc limit 1" % (fotime, fuid, fgid, fogn, famount)
    try:
        sql2 = " update lawyers_new set gender = '%s' , pra_type = '%s' , first_pra_time = '%s' where id= %d " % (gender,pra_type,first_pra_time,row[0])
        effect_row = cursor.execute(sql2)
    except:
        print sql2
        print row[0],row[1],gender,pra_type,first_pra_time
conn.commit()
cursor.close()
conn.close()