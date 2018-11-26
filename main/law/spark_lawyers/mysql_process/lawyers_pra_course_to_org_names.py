# -*- coding: utf-8 -*-
import pymysql
import re


conn=pymysql.connect(host='192.168.74.102',user='weiwc',passwd='HHly2017.',db='laws_doc_lawyers_new',charset='utf8')
cursor = conn.cursor()
sql = ' select id,pra_course,org_names,org_name from hht_lawyer_all_collect_match_result  '   #LOCATE函数，包含||,返回大于0的数值。
cursor.execute(sql)
row_2 = cursor.fetchall()

# 2013-02-05开始首次执业2015-09-17市内转所：广东南方福瑞德律师事务所
# 1996-04-18开始首次执业2002-05-21市内转所：广东立国律师事务所2004-08-18市内转所：广东正大元律师事务所2005-04-28市内转所：广东劳维律师事务所2007-07-18市内转所：广东卓建律师事务所2009-08-05市内转所：广东立国律师事务所2012-08-15市内转所：广东赵卢律师事务所2013-08-05跨市转所：广东创晖律师事务所
# 2006-02-22开始首次执业2007-03-20市内转所：广东法制盛邦律师事务所2009-10-28市内转所：广东沁森律师事务所2013-12-05市内转所：广东盈隆律师事务所2015-09-25市内转所：广东法制盛邦律师事务所
# 1996-11-04开始首次执业2002-05-16市内转所：广东东成律师事务所2013-01-28跨市转所：广东科韵律师事务所
# 1995-05-30开始首次执业2006-12-01市内转所：广东闻彰律师事务所

def get_org_names(row1):
    #python中使用{}时，不要加\，(\{\})
    p1 = re.compile(ur'：[\u4e00-\u9fa5()]{1,20}\u4e8b\u52a1\u6240',re.S)  #\u4e00-\u9fa5汉字编码范围,匹配 ：“业2009-”这样的数据
    ll = []
    if row1 and row1 != "":
        result_list = re.findall(p1,row1)
        for i in result_list:
            ll.append(i.replace(u"：",""))
        return ll
    else:
        return ll

for row in row_2 :
    org_name = []
    if row[2] and row[2] != "":
        org_name = row[2].split("||")

    pra_course_org_name = get_org_names(row[1])
    result = pra_course_org_name + org_name
    result.append(row[3])


    # print row[0],pra_course_org_name
    sql2 = " update hht_lawyer_all_collect_match_result set org_names='" + "||".join(list(set(result))) + "' where id= '" + str(row[0]) + "'"
    effect_row = cursor.execute(sql2)
conn.commit()
cursor.close()
conn.close()
