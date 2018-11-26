# -*- coding: utf-8 -*-
import pymysql
import re


conn=pymysql.connect(host='192.168.74.102',user='weiwc',passwd='HHly2017.',db='laws_doc_lawyers_new',charset='utf8')
cursor = conn.cursor()
sql = ' select id,org_name,annualass from hht_lawyer_jiangsu_annualass '
cursor.execute(sql)
row_2 = cursor.fetchall()

# [{'year': '2016', 'audit': '称职', 'audit_office': '江苏沉浮律师事务所'},
#  {'year': '2017', 'audit': '', 'audit_office': '江苏沉浮律师事务所'}]

def get_org_names(row1,row2):
    #python中使用{}时，不要加\，(\{\})
    # p1 = re.compile(ur'：[\u4e00-\u9fa5()]{1,20}\u4e8b\u52a1\u6240',re.S)  #\u4e00-\u9fa5汉字编码范围,匹配 ：“业2009-”这样的数据
    ll = []
    ann = eval(row2)
    for i in ann:
        # print type(i.get('audit_office'))
        # print type(i)
        if row1 != i.get('audit_office').decode("utf-8"):
            ll.append(i.get('audit_office').decode("utf-8"))
    if not ll :
        return ""
    else:
        return "||".join(list(set(ll)))

for row in row_2 :
    org_names = get_org_names(row[1],row[2])
    if org_names == "":
        continue

    sql2 = " update hht_lawyer_jiangsu_annualass set org_names='" + org_names + "' where id= '" + str(row[0]) + "'"
    print row[1],sql2
    effect_row = cursor.execute(sql2)
conn.commit()
cursor.close()
conn.close()
