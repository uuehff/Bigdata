# -*- coding: utf-8 -*-
import pymysql
import re

import time

print time.asctime( time.localtime(time.time()) )
# for i in range(1,28):
#     num = i * 100000
# conn=pymysql.connect(host='192.168.12.34',user='root',passwd='root',db='laws_doc_mediate',charset='utf8')
conn=pymysql.connect(host='cdh-slave1',user='weiwc',passwd='HHly2017.',db='laws_doc_mediate',charset='utf8')
cursor = conn.cursor()
sql = 'select id,uuid,doc_footer from mediate_civil_etl where doc_footer != "" and doc_footer is not null '   #LOCATE函数，包含||,返回大于0的数值。
# sql = 'select id,uuid,doc_footer from mediate_civil_etl where uuid  in (select uuid from casedate_validate where casedate = "") order by id'   #LOCATE函数，包含||,返回大于0的数值。

cursor.execute(sql)
# row_1 = cursor.fetchone()
# row_2 = cursor.fetchmany(5)
row_2 = cursor.fetchall()

def get_date(j,a):
    d = re.split(ur"年|月|日", j)
    if len(d) == 4:
        if len(d[0]) == 4:
            year = a.get(d[0][0], "a") + a.get(d[0][1], "a") + a.get(d[0][2], "a") + a.get(d[0][3], "a")
            m = a.get(d[1], "aa")
            if len(m) == 1:
                m = "0" + m
            day = a.get(d[2], "aa")
            if len(day) == 1:
                day = "0" + day
            elif day == "aa" and d[2].startswith(u"十"):
                day = "1" + a.get(d[2][1], "a")
            elif day == "aa" and d[2].startswith(u"二十"):
                day = "2" + a.get(d[2][2], "a")
            strdate = year + "-" + m + "-" + day
            try:
                time.strptime(strdate, "%Y-%m-%d")
                return strdate
            except:
                return ""
    else:
        return ""

def get_casedate(doc_footer):
    a = {u"O": "0",u"o": "0",u"Ο": "0",u"Ｏ": "0",u"0": "0",u"○": "0", u"〇": "0", u"０": "0", u"元": "1", u"一": "1", u"二": "2", u"三": "3", u"四": "4", u"五": "5",
         u"六": "6", u"七": "7", u"八": "8", u"九": "9", u"十": "10", u"十一": "11", u"十二": "12", u"二十": "20", u"三十": "30",
         u"三十一": "31"}
    s = re.split('[\n]',doc_footer)
    if len(s) < 2:
        d = re.split(ur"O|o|Ο|〇|0|○|Ｏ|０|日", doc_footer)
        if len(d) > 2:
            return get_date(u"二〇" + d[1].replace(" ","") + u"日",a)
        else: return ""
    else:
        for i in s:
            j = i.replace(" ", "")
            if (j.startswith(u"一") or j.startswith(u"二")) and u"日" in j:
                return get_date(j,a)
            elif u"年" in j and u"月" in j and u"日" in j:
                j1 = re.split(ur"二O|二o|二Ο|二〇|二0|二○|二Ｏ|二０|日", doc_footer)
                j2 = u"二〇" + j1[1] + u"日"
                return get_date(j2,a)
            else: continue
        return ""

# 审判员  尹明月
#  二〇一七 二月 二十一日
#  书记员  展晓敏


 # 审判员  亢水清 二0一七年三月 二日
 # 书记员  靳淑荣

# 审判员  赵小双
#  二○一六年十 二月月 二十日
#  书记员  段责义

# 审判员  许军华
#  二○一五年五月十五无
#  书记员  刘绮薇

#  审判员  杨立新
#  二〇一五年一月十九日 书记员  张晓月

#  审判长  吴宏
#  审判员  祝春雄
#  代理 审判员  孙楚楚
# （） 二○一五年十一月 二十五日
#  书记员  俞渊


 # 审判员  马志霞
 # 二0一六年 二0一六年六月 二十四日
 # 书记员  陈建力

#  代理 审判员  庞芸 二Ｏ一一年四月 二十一日 书记员  王燕
#  代理 审判员  庞芸 二Ｏ一一年四月 二十一日
#   二Ｏ一一年四月 二十一日 书记员  王燕
cc = 0
def casedate_get(doc_footer):
    # [u'一',u'二',u'三',u'四',u'五',u'六',u'七',u'八',u'九',u'十',u'百',u'千',u'第',u'条']
    # [u'\u4e00', u'\u4e8c', u'\u4e09', u'\u56db', u'\u4e94', u'\u516d', u'\u4e03', u'\u516b', u'\u4e5d', u'\u5341', u'\u767e', u'\u5343', u'\u7b2c', u'\u6761']
    # 搜索以 ‘第’开头，以‘条’结束，中间包含：1-10个[u'一',u'二',u'三',u'四',u'五',u'六',u'七',u'八',u'九',u'十',u'百',u'千']中的汉字

    a = {u"О": "0",u"O": "0",u"o": "0",u"Ο": "0",u"Ｏ": "0", u"0": "0", u"○": "0", u"〇": "0", u"０": "0", u"元": "1", u"一": "1", u"二": "2", u"三": "3", u"四": "4",u"五": "5",u"六": "6", u"七": "7", u"八": "8", u"九": "9", u"十": "10", u"十一": "11", u"十二": "12", u"二十": "20", u"三十": "30",u"三十一": "31"}

    p1 = ur'[一二][ ]{0,8}[ОOoΟＯ0○〇０九][ ]{0,8}[ОOoΟＯ0○〇０一二九][ ]{0,8}[ОOoΟＯ0○〇０一二三四五六七八九][ ]{0,8}年[ ]{0,8}年{0,1}[ ]{0,8}[元一二三四五六七八九十][ ]{0,8}[一二]{0,1}[ ]{0,8}月[ ]{0,8}月{0,1}[ ]{0,8}[一二三四五六七八九十][ ]{0,8}[一二三四五六七八九十]{0,1}[ ]{0,8}[一二三四五六七八九十]{0,1}'
    r2 = re.search(p1, doc_footer)

    if r2:
        j = r2.group(0).replace(" ","").replace(u"年年",u"年").replace(u"月月",u"月") + u"日"
        return get_date(j,a)
    else:
        return ""

for row in row_2 :
    doc_footer = row[2]
    casedate = casedate_get(doc_footer)
    # sql2 = " insert into casedate_validate (id,uuid,casedate) values (%s, %s, %s)"
    sql2 = " insert into casedate_update (id,uuid,casedate) values (%s, %s, %s)"
    cursor.execute(sql2,(row[0],row[1],casedate))
print cc

conn.commit()
cursor.close()
conn.close()
print time.asctime( time.localtime(time.time()) )