# -*- coding: utf-8 -*-
import pymysql
import re


conn=pymysql.connect(host='192.168.12.34',user='root',passwd='root',db='laws_doc',charset='utf8')
cursor = conn.cursor()
sql = ' select lawyer,law_office,pra_course from lawyers_new where pra_course like "%转所%" '   #LOCATE函数，包含||,返回大于0的数值。
cursor.execute(sql)
row_2 = cursor.fetchall()

# 2013-02-05开始首次执业2015-09-17市内转所：广东南方福瑞德律师事务所
# 1996-04-18开始首次执业2002-05-21市内转所：广东立国律师事务所2004-08-18市内转所：广东正大元律师事务所2005-04-28市内转所：广东劳维律师事务所2007-07-18市内转所：广东卓建律师事务所2009-08-05市内转所：广东立国律师事务所2012-08-15市内转所：广东赵卢律师事务所2013-08-05跨市转所：广东创晖律师事务所
# 2006-02-22开始首次执业2007-03-20市内转所：广东法制盛邦律师事务所2009-10-28市内转所：广东沁森律师事务所2013-12-05市内转所：广东盈隆律师事务所2015-09-25市内转所：广东法制盛邦律师事务所
# 1996-11-04开始首次执业2002-05-16市内转所：广东东成律师事务所2013-01-28跨市转所：广东科韵律师事务所
# 1995-05-30开始首次执业2006-12-01市内转所：广东闻彰律师事务所

def del_pra_course(row):
    laws = []
    laws.append(row[1])
    p1 = ur'[\u4e00-\u9fa5]{1,100}事务所'  #\u4e00-\u9fa5汉字编码范围
    p2 = ur"："
    #抽取、处理pra_course中的律所
    for i in re.split(p2, row[2]):
        pattern2 = re.search(p1, i)
        if pattern2:
            laws.append(pattern2.group(0))

    #去掉律所第三个字为 省、市、县三个字。统一律所格式
    laws2 = []
    for k in laws:
        if k and k != "" and len(k) >= 3 and (k[2] == u'省' or k[2] == u'市' or k[2] == u'县'):  # 同一律师名字下，将第三个字为省、市、县去掉。
            t = []
            for j in range(0, len(k)):
                if j == 2:
                    continue
                t.append(k[j])
            k = "".join(t)
        k = k.replace(u"律师事务所", "")  # 统一将结尾处理为律师事务所,去重
        k = k.replace(u"事务所", "")
        lawyer = k + u"律师事务所"
        if lawyer != u"律师事务所" and lawyer != u"事务所":
            laws2.append(lawyer)

    #去重律所内容
    return list(set(laws2))
c = 1
for row in row_2 :
    laws = del_pra_course(row)
    for law_office in laws:
        sql2 = " insert into lawyers__lawyer_course (lawyer,law_office,lawyer_key) values (%s, %s, %s)"
        cursor.execute(sql2,(row[0],law_office,c))
    c += 1
conn.commit()
cursor.close()
conn.close()