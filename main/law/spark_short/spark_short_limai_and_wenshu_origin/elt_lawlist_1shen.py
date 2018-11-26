# -*- coding: utf-8 -*-
import pymysql
import re
import time

def etl(p1,p2,lawlist):
    if lawlist and len(lawlist) > 0:
        # if not (lawlist.startswith("[") and lawlist.endswith("]")):
        #     o = ""
        #     for i in lawlist:
        #         if i == "[":
        #             break
        #         o = o + '"'
        #     start = o + "["
        #     end = "]" + o
        #     lawlist = lawlist.replace(start,"[").replace(end,"]")
        l = list(eval(lawlist))

        if l :
            tl = []
            for i in l:
                r1 = re.split(p2, i.decode("utf-8"))
                if len(r1) > 2:
                    r2 = re.search(p1, r1[2])
                    if r2:
                        tl.append((r1[1] + "|" + r2.group(0)))
            # print  list(set(tl))
            return list(set(tl))
    else :
        return []

# conn=pymysql.connect(host='192.168.10.24',user='root',passwd='root',db='laws_doc',charset='utf8')
conn=pymysql.connect(host='localhost',user='root',passwd='root',db='laws_doc',charset='utf8')
cursor = conn.cursor()
# 1876056-2127296
# id >= 1876056 and id <= 2127296
# sql = 'select uuid,lawlist from judgment where id >= 1900000 and id <= 2127296 '
sql = 'select uuid,lawlist from tb_doc where id <= 1 '
cursor.execute(sql)
# row_1 = cursor.fetchone()
# row_2 = cursor.fetchmany(5)
row_2 = cursor.fetchall()
print "read mysql success... %s" % time.time()
#[u'一',u'二',u'三',u'四',u'五',u'六',u'七',u'八',u'九',u'十',u'百',u'千',u'第',u'条']
# [u'\u4e00', u'\u4e8c', u'\u4e09', u'\u56db', u'\u4e94', u'\u516d', u'\u4e03', u'\u516b', u'\u4e5d', u'\u5341', u'\u767e', u'\u5343', u'\u7b2c', u'\u6761']
# 搜索以 ‘第’开头，以‘条’结束，中间包含：1-10个[u'一',u'二',u'三',u'四',u'五',u'六',u'七',u'八',u'九',u'十',u'百',u'千']中的汉字
p1 = ur'\u7b2c[\u4e00\u4e8c\u4e09\u56db\u4e94\u516d\u4e03\u516b\u4e5d\u5341\u767e\u5343]{1,10}\u6761'
# 按《》切分
p2 = ur'[\u300a\u300b]'
for row in row_2 :
    s1 = etl(p1,p2,row[1])
    # for i in s1:
    #     print i
    # print type(",".join(s1))
    if s1:
        # sql = "select user,pass from tb7 where user='%s' and pass='%s'" % (user, passwd)
        # sql2 = " update tmp_weiwenchao set lawlist='" + ",".join(s1) + "' where uuid= '" + row[0] + "'"
        # cursor.execute(sql2)
        print ",".join(s1)
    conn.commit()
print "execute success... %s" % time.time()
cursor.close()
conn.close()