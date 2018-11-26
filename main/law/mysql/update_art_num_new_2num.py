# -*- coding: utf-8 -*-
import pymysql
import re

date_range = ["2012-*","2002-2012","1992-2002","1982-1992","1978-1982","1949-1978"]

#[u'一',u'二',u'三',u'四',u'五',u'六',u'七',u'八',u'九',u'十',u'百',u'千',u'第',u'条']
# [u'\u4e00', u'\u4e8c', u'\u4e09', u'\u56db', u'\u4e94', u'\u516d', u'\u4e03', u'\u516b', u'\u4e5d', u'\u5341', u'\u767e', u'\u5343', u'\u7b2c', u'\u6761']
# 搜索以 ‘第’开头，以‘条’结束，中间包含：1-10个[u'一',u'二',u'三',u'四',u'五',u'六',u'七',u'八',u'九',u'十',u'百',u'千']中的汉字
p1 = ur'\u7b2c[\u4e00\u4e8c\u4e09\u56db\u4e94\u516d\u4e03\u516b\u4e5d\u5341]{1}{}\u6761'
p1 = ur'\u7b2c[\u4e00\u4e8c\u4e09\u56db\u4e94\u516d\u4e03\u516b\u4e5d\u5341\u767e\u5343]{1,10}\u6761'
# 按《》切分
p2 = ur'[\u7b2c\u6761]'

m = {u'零':'0',u'一':'1',u'二':'2',u'三':'3',u'四':'4',u'五':'5',u'六':'6',u'七':'7',
     u'八':'8',u'九':'9',u'十':'10',u'百':'00',u'千':'000'}

def getLawlistID(art_num):
    if art_num and art_num != '':
        art_num = art_num.strip()       #去掉发条前后的空格

        if art_num.startswith(u"第") and art_num.endswith(u"条"): #一、二、三...
            c = re.split(p2, art_num)[1]
            if len(c) == 1:
                return m.get(c)
            elif len(c) == 2:   #十二、二十、二百、二千
                if c.startswith(u"十"):
                    return "1" + m.get(c[1])
                elif c.endswith(u"十"):
                    return m.get(c[0]) + "0"
                elif c.endswith(u"百"):
                    return m.get(c[0]) + "00"
                elif c.endswith(u"千"):
                    return m.get(c[0]) + "000"
                else :   return "0"
            elif len(c) == 3:       #二十一
                return  m.get(c[0]) + m.get(c[2])
            elif len(c) == 4:       #一百二十、一千零十、一百零二、一千二百、一千零二、
                if c.endswith(u"十"):
                    if c[1] == u"百" :
                        return m.get(c[0]) + m.get(c[2]) + "0"
                    elif c[1] == u"千" :
                        return m.get(c[0]) +  "010"        # 一千零十
                elif c.endswith(u"百"):
                    return m.get(c[0]) + m.get(c[2]) + "00"
                elif c[1] == u"百" and c[2] == u"零":
                    return m.get(c[0]) + "0" + m.get(c[3])
                elif c[1] == u"千" and c[2] == u"零":
                    return m.get(c[0]) + "00" + m.get(c[3])
                else:    return "0"
            elif len(c) == 5:  #一百二十五、一千零十一、一千零二十
                if  c[1] == u"百":
                    return m.get(c[0]) + m.get(c[2]) + m.get(c[4])
                elif c[2] == u"零" and c[3] == u"十":
                    return m.get(c[0]) + "01" + m.get(c[4])
                elif c[2] == u"零" and c.endswith(u"十"):
                    return m.get(c[0]) + "0" + m.get(c[3]) + "0"

            elif len(c) == 6:   #一千零二十一、一千一百零一，一千一百一十、
                if c[2] == u"零":
                    return m.get(c[0]) + "0" + m.get(c[3]) + m.get(c[5])
                elif c[4] == u"零":
                    return m.get(c[0]) + m.get(c[2]) + "0" + m.get(c[5])
                elif c.endswith(u"十"):
                    return m.get(c[0]) + m.get(c[2]) + m.get(c[4]) + "0"
            elif len(c) == 7:  # 一千一百一十一、
                return m.get(c[0]) + m.get(c[2]) + m.get(c[4]) + m.get(c[6])
            else:  return "0"
        else: return "0"
    else :    return "0"


import time
if __name__ == '__main__':

    print time.time()
    conn=pymysql.connect(host='192.168.12.35',user='root',passwd='HHly2017.',db='law',charset='utf8')
    cursor = conn.cursor()
    # sql = 'select id,art_num from law_rule_result2 '
    sql = 'select id,art_num from law_rule_result2 where id >= 2880870 '
    cursor.execute(sql)

    row_2 = cursor.fetchall()

    for row in row_2 :
        # id为int类型，不用%d!

        lawlist_id = getLawlistID(row[1])
        # print row[1],int(lawlist_id)


        # art_num.strip()
        sql2 = "update law_rule_result2 set art_digit='%s' where id='%s'" % (lawlist_id, row[0])
        # sql2 = " insert into effective_range_field (id,effective_range) values (%s, %s)"
        effect_row = cursor.execute(sql2)

    conn.commit()
    cursor.close()
    conn.close()
    print time.time()