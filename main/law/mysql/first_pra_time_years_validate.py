# -*- coding: utf-8 -*-
import pymysql
import re

import time

print time.asctime( time.localtime(time.time()) )
# for i in range(1,28):
#     num = i * 100000
conn=pymysql.connect(host='cdh-slave1',user='root',passwd='HHly2017.',db='laws_doc_v2',charset='utf8')
# conn=pymysql.connect(host='cdh-slave1',user='weiwc',passwd='HHly2017.',db='laws_doc_lawyers',charset='utf8')
cursor = conn.cursor()
# sql = 'select id,char_no,first_pra_time from lawyers where (char_no != "" and char_no is not null) or (first_pra_time != "" and first_pra_time is not null)'   #LOCATE函数，包含||,返回大于0的数值。
sql = 'select id,char_no,first_pra_time,birthday from lawyers '   #LOCATE函数，包含||,返回大于0的数值。
# sql = 'select id,char_no,first_pra_time,birthday from lawyers where id in (384487,387249,38885,390207,396374,411044,42399,425893,463716,476305,486837,4995,501338,520269,531926,411044,531926,295929,327797,351357,355121,357441,360495,364716,367451,374385,152018,157630,163019,165621,179858,194179,208716,226563,248030,260206,268834,105317) order by id '   #LOCATE函数，包含||,返回大于0的数值。
cursor.execute(sql)
row_2 = cursor.fetchall()
def get_valid_date(char_no,first_pra_time):
    '''''判断是否是一个有效的日期字符串'''
    try:
        if first_pra_time and first_pra_time != "":
            if len(first_pra_time) == 4 and int(first_pra_time) > 1949 and int(first_pra_time) < 2019:
                return first_pra_time
            elif len(first_pra_time) == 7:
                time.strptime(first_pra_time, "%Y-%m")
                return first_pra_time
            elif len(first_pra_time) == 10:
                time.strptime(first_pra_time, "%Y-%m-%d")
                return first_pra_time
            elif char_no and char_no != "" and len(char_no) == 17 and int(char_no[5:9]) > 1949 and int(char_no[5:9]) < 2019:
                return char_no[5:9]
            else:
                return ""
        elif char_no and char_no != "" and len(char_no) == 17 and int(char_no[5:9]) > 1949 and int(char_no[5:9]) < 2019:
                return char_no[5:9]
        else:
            return ""
    except:
        try:
            if char_no and char_no != "" :
                if len(char_no) == 17 and int(char_no[5:9]) > 1949 and int(char_no[5:9]) < 2019:
                    return ""
            else:
                return ""
        except:
            return ""
def get_birthday(birth):
    try:
        if birth and birth != "":
            if len(birth) == 4 and int(birth) > 1900 and int(birth) < 2019:
                return birth
            elif len(birth) == 6 and "-" in birth:
                time.strptime(birth, "%Y-%m")
                return birth.replace("-","-0")
            elif len(birth) == 7:
                time.strptime(birth, "%Y-%m")
                return birth
            elif len(birth) == 8 and "-" in birth:
                time.strptime(birth, "%Y-%m-%d")
                return birth.replace("-","-0")
            elif len(birth) == 9:
                time.strptime(birth, "%Y-%m-%d")
                if len(birth.split("-")[1]) == 1:
                    return birth.split("-")[0] + "-0" + birth.split("-")[1] + "-" + birth.split("-")[2]
                else:
                    return birth.split("-")[0] + "-" + birth.split("-")[1] + "-0" + birth.split("-")[2]
            elif len(birth) == 10:
                time.strptime(birth, "%Y-%m-%d")
                return birth
            else:
                return ""
        else:
            return ""
    except:
        return ""
for row in row_2 :
    first_pra_time = get_valid_date(row[1],row[2])
    years = ""
    if first_pra_time != "":
        years = str(2018-int(first_pra_time[0:4]))
    try:
        births = get_birthday(row[3])

        sql2 = " update lawyers set first_pra_time='%s', birthday ='%s', years = '%s' where id = '%s'" % (first_pra_time, births,years,row[0])
        # print sql2
        cursor.execute(sql2)
    except:
        print sql2

conn.commit()
cursor.close()
conn.close()
print time.asctime( time.localtime(time.time()) )