# -*- coding: utf-8 -*-
import pymysql
import re


conn=pymysql.connect(host='192.168.74.102',user='weiwc',passwd='HHly2017.',db='laws_doc_lawyers_new',charset='utf8')
cursor = conn.cursor()
# sql = 'select pra_number,name,org_name from lawyer_info_new_v3  '   #LOCATE函数，包含||,返回大于0的数值。
# sql = 'select pra_number,name,org_name from lawyer_duplicate  '   #LOCATE函数，包含||,返回大于0的数值。
# sql = 'select pra_number,name,org_name,org_identity,pra_course from hht_lawyer_12348gov_v3  '   #LOCATE函数，包含||,返回大于0的数值。
sql = 'select pra_number,substr(qua_number,2,4),qua_number,name,org_name,org_identity,pra_course,nation,edu_origin,politics,birth_date,first_pra_time,qua_number,qua_time from hht_lawyer_12348gov_v3  '   #LOCATE函数，包含||,返回大于0的数值。
cursor.execute(sql)
row_2 = cursor.fetchall()

cursor2 = conn.cursor()
# pri_reason_re = re.search(ur'''[\u4e00-\u9fa5]+[.][\u4e00-\u9fa5]''',content_text)
# reg_footer = re.compile(ur'\n(?:\S{0,2}审判|\S{0,2}执行员).*(?:\S{0,2}书记员|\S+年\S+月)\S+', re.S)

# reg_name = re.compile(ur'''[\u4e00-\u9fa5]*[a-z1-9A-Z?:;,<>，。《》~！@#￥%（）()-=_+、：；&?？     ]+[\u4e00-\u9fa5]*''')
# reg_name = re.compile(ur'''[a-z1-9A-Z?:;,<>，。《》~！@#￥%-=_+、：；&?？     ]''')
# reg_name = re.compile(ur'''[a-z1-9A-Z:;,<>，。.《》
# @#%&_+-=、：；!！?？    \n]''')
# reg_pra_number = re.compile(ur'''[a-zA-Z._|!?    \n]''')
reg_org_identity = re.compile(ur'''[\u4e00-\u9fa5 a-zD-Z;,，。_+=、；!！?？    \n]''')
a=  0
for row in row_2 :
    pra_number = row[0]
    qua_number_year = row[1]
    # name = row[1]
    # org_name = row[2]
    # org_identity = row[3]
    # pra_course = row[4]
    # nation = row[5]
    # edu_origin = row[6]
    # politics = row[7]
    # birth_date = row[8]
    # first_pra_time = row[9]
    # qua_number = row[10]
    # qua_time = row[11]
    # if (re.search(reg_name,name) or len(name) < 2) and "." not  in name :
    if qua_number_year and re.search(reg_org_identity,qua_number_year) :
    # if re.search(reg_name,org_name) or len(org_name) < 9 :
        # if u"." in name :
        #     continue
        # name = name.split("(")[0]
        # sql3 = " update lawyer_info_new_v3 set name=' " + name + "' where pra_number= '" + row[0] + "'"
        # sql3 = " delete from  hht_lawyer_12348gov_v3  where pra_number= '" + row[0] + "'"
        # sql3 = " update lawyer_info_new_v3 set name=' " + name + "' where pra_number= '" + row[0] + "'"
        # cursor2.execute(sql3)
        # if row[1].repl
        print row[0],qua_number_year,row[2]
        a += 1

    # for i in ids :
    #     sql2 = "select lawyer,office from lawyer where id =  " + i
    #     cursor2.execute(sql2)
    #     one = cursor2.fetchone()
    #     orig.append(one[0] + "|" + one[1])
    # print "||".join(orig)
print a
conn.commit()
cursor.close()
conn.close()