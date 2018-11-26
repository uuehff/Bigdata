# -*- coding: utf-8 -*-
import pymysql
import re

import time

print time.asctime( time.localtime(time.time()) )
# for i in range(1,28):
#     num = i * 100000
conn=pymysql.connect(host='192.168.74.102',user='weiwc',passwd='HHly2017.',db='laws_doc_lawyers_new',charset='utf8')
cursor = conn.cursor()
# sql = 'select SUBSTR(pra_number,6,4),years from hht_lawyer_12348gov_v3 where SUBSTR(pra_number,6,4) <= "2018" and SUBSTR(pra_number,6,4) >= "1970" '   #LOCATE函数，包含||,返回大于0的数值。
# sql = 'select pra_number,birth_date,first_pra_time,qua_time from hht_lawyer_12348gov_v3 where SUBSTR(pra_number,6,4) <= "2018" and SUBSTR(pra_number,6,4) >= "1970" '   #LOCATE函数，包含||,返回大于0的数值。
# sql = 'select pra_number,birth_date,SUBSTR(birth_date,1,4),first_pra_time,qua_time from hht_lawyer_12348gov_v3 where birth_date is not null and birth_date != "" and char_length(birth_date) > 4 '   #LOCATE函数，包含||,返回大于0的数值。
# sql = 'select pra_number,birth_date,SUBSTR(birth_date,1,4),first_pra_time,qua_time from hht_lawyer_12348gov_v3 where first_pra_time is not null and first_pra_time != ""  '   #LOCATE函数，包含||,返回大于0的数值。
# sql = 'select pra_number,birth_date,SUBSTR(birth_date,1,4),first_pra_time,qua_time from hht_lawyer_12348gov_v3 where qua_time is not null and qua_time != ""  '   #LOCATE函数，包含||,返回大于0的数值。
sql = 'select pra_number,qua_number from hht_lawyer_12348gov_v3 where qua_number is not null and qua_number != ""  '   #LOCATE函数，包含||,返回大于0的数值。
cursor.execute(sql)
row_2 = cursor.fetchall()
def is_valid_date(strdate):
    '''''判断是否是一个有效的日期字符串'''
    try:
        # if ":" in strdate:
        #     time.strptime(strdate, "%Y-%m-%d %H:%M:%S")
        # else:
        time.strptime(strdate, "%Y-%m-%d")
        return False
    except:
        return True

a = 0
# for row in row_2 :
#     if is_valid_date(row[4]):
#
#         # sql2 = " update hht_lawyer_12348gov_v3 set birth_date='" + row[2] + "' where pra_number= '" + row[0] + "'"
#         # cursor.execute(sql2)
#         print row[0],row[4]
#         a += 1
# print a

for row in row_2 :
    try:
        qua_number_year = int(row[1][1:5])
    except:
        print row[0],row[1]

conn.commit()
cursor.close()
conn.close()
print time.asctime( time.localtime(time.time()) )