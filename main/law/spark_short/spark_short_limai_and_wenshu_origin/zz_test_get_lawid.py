# -*- coding: utf-8 -*-
import pymysql
import re

import time

print time.asctime( time.localtime(time.time()) )

def etl_lawlist(p1, p2, lawlist):
    if lawlist and lawlist.strip() != '':
        # if not (lawlist.strip().startswith("[") and lawlist.strip().endswith("]")):  # 去掉前后的所有"
        r1 = re.findall(ur'"{0,5}\["{0,5}', lawlist.strip())
        r2 = re.findall(ur'"{0,5}\]"{0,5}', lawlist.strip())
        if r1 and r2:
            start = r1.pop(0)
            end = r2.pop()
            lawlist = lawlist.strip().replace(start, "").replace(end, "")
            # l = list(eval(lawlist.strip()))                 #有脏数据不能直接使用eval()

            l = lawlist.split(
                '","')  # lawlist类似于：《最高人民法院关于审理建设工程施工合同纠纷案件适用法律问题的解释》第三条", "《中华人民共和国合同法》第九十七条", "最高人民法院关于审理建设工程施工合同纠纷案件适用法律问题的解释》第十条", "《中华人民共和国合同法》第九十八条
            if l:
                tl = []
                for i in l:
                    r1 = re.split(p2, i)
                    if len(r1) > 2:  # 确保既有《，又有》
                        r2 = re.search(p1, r1[2])
                        if r2:  # 判断是否找到了条
                            tl.append(r1[1] + "|" + r2.group(0))
                return list(set(tl))  # 去重
            return []
        return []
    return []

conn=pymysql.connect(host='192.168.74.102',user='weiwc',passwd='HHly2017.',db='laws_doc_zhangye_v2',charset='utf8')
cursor = conn.cursor()
sql = 'select id,uuid,lawlist from uuid_law_id_zhangye_civil_v4 where id < 1935990 '   #LOCATE函数，包含||,返回大于0的数值。
cursor.execute(sql)
row_2 = cursor.fetchall()

p1 = ur'\u7b2c[\u4e00\u4e8c\u4e09\u56db\u4e94\u516d\u4e03\u516b\u4e5d\u5341\u767e\u5343]{1,10}\u6761'
p2 = ur'[\u300a\u300b]'  # 按《》切分

for row in row_2 :
    lawlist = row[2]
    print etl_lawlist(p1,p2,lawlist)
    for i in etl_lawlist(p1,p2,lawlist):
        print i

    # sql2 = " insert into casedate_validate (id,uuid,casedate) values (%s, %s, %s)"
    # cursor.execute(sql2,(row[0],row[1],row[2]))

conn.commit()
cursor.close()
conn.close()
print time.asctime( time.localtime(time.time()) )





