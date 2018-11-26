# -*- coding: utf-8 -*-
import pymysql
import re


conn=pymysql.connect(host='192.168.74.102',user='weiwc',passwd='HHly2017.',db='laws_doc_lawyers_new',charset='utf8')
cursor = conn.cursor()
sql = ' select a.id,a.org_names,b.org_names from hht_lawyer_all_collect_match_result a ' \
      'join hht_lawyer_jiangsu_annualass b ' \
      'on a.pra_number = b.pra_number and a.name = b.name and a.org_name = b.org_name '
cursor.execute(sql)
row_2 = cursor.fetchall()

# [{'year': '2016', 'audit': '称职', 'audit_office': '江苏沉浮律师事务所'},
#  {'year': '2017', 'audit': '', 'audit_office': '江苏沉浮律师事务所'}]

def get_org_names(row1,row2):
    ll = []
    for i in row1.split("||"):
        ll.append(i)

    for j in row2.split("||"):
        ll.append(j)

    return "||".join(list(set(ll)))
c = 0
for row in row_2 :
    c += 1
    org_names = get_org_names(row[1],row[2])

    sql2 = " update hht_lawyer_all_collect_match_result set org_names='" + org_names + "' where id= '" + str(row[0]) + "'"
    print row[0],row[1],row[2],sql2
    effect_row = cursor.execute(sql2)
print c
conn.commit()
cursor.close()
conn.close()
