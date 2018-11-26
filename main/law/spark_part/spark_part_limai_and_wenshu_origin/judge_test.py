# -*- coding: utf-8 -*-

import re
import pymysql
import time

def foot_get(items):
    # judge_result:
    # 准许原告暨诉讼代表人撤回起诉。
    # 案件受理费50元，减半收取25元，由原告暨诉讼代表人负担。
    # 审判长吴铁梅
    # 审判员殷载媛
    # 人民陪审员肖正江
    # 二〇一七年一月十日
    # 书记员欧阳小玲

    # ?  0或1次，+ 1或多， * 0或多
    # reg_footer = re.compile(ur'\n(?:\S{0,2}审判).*(?:书记员|\S+年\S+月)\S+', re.S)
    # 附里面的当事人信息里面也有年月的匹配。
    # re.S开启了.匹配任意字符串，用(?:和)将其之间的内容作为一个整体，而不是用（），\n(?:\S{0,2}审判)，其中judge_result中的空格都已去掉，有的只是
    # 换行回车等：\f\n\r\t\v，审判前面匹配0-2个非空字符，可能匹配到代理等词，再前面是\n，是判决结果那句话与下面的换行符。
    # .*匹配任意字符，(?:书记员|\S+年\S+月)\S+，这里能匹配到“书记员，代书记员，或者多个书记员等等”，匹配到最后一个符合条件的值，
    # 拆开为：匹配到最后一个.*书记员\S+ 或 匹配到最后一个.*\S+年\S+月\S+，哪个的值在最最后，就以哪个的匹配值结尾。\S+匹配任意非空，遇空（\f\n\r\t\v）就停止。
    # reg_footer = re.compile(ur'\n(?:\S{0,2}审判|\S{0,2}执行员|\S{0,2}院长).*(?:\S{0,2}书记员|\S+年\S+月)\S+', re.S)
    reg_footer = re.compile(ur'\n(?:\S{0,2}审[　  ]{0,2}判|\S{0,2}执[　  ]{0,2}行员|\S{0,2}院[　  ]{0,2}长).*(?:书[　  ]{0,2}记员|\S+年\S+月)\S+', re.S)
    items = items.replace("\\n", '\n')
    footer_result = re.findall(reg_footer, items)

    if footer_result:
        # footer_result[0]中可能有特殊符号：类似？号等等，？在split的pattern中属于特殊字符，因此要替换掉再分割.
        items_tmp = items.replace(footer_result[0], "!1qw23er4!")

        lp = re.split("!1qw23er4!", items_tmp)
        doc_footer = footer_result[0].strip() + lp[1]

        doc_footer = doc_footer.replace(u"审判长", u" 审判长  ").replace(u"代理审判员", u" 代理审判员") \
            .replace(u"审判员", u" 审判员  ").replace(u"书记员", u" 书记员  ").replace(u"陪审员", u" 陪审员  ") \
            .replace(u"二", u" 二").replace(u"院长", u" 院长  ").replace(u"执行员", u" 执行员  ")
        return lp[0], doc_footer  # result,doc_footer
    else:
        return items, ""

def get_judge(doc_footer):
    doc_footer = doc_footer.replace(u"　", "").replace(" ", "")
    split_result = doc_footer.split("\n")
    reg_footer = re.compile(ur'(?:\S{0,2}审判|\S{0,2}院长|\S{0,2}陪审)\S{2,}')
    judge_result = ""
    l = []
    for i in split_result:
        if re.search(reg_footer, i):
            l.append(i)
    # 审判长|院长|审判员|代理审判员|人民审判员|助理审判员|陪审员|人民陪审员
    judge_result = "||".join(l).replace(u"代理审判长", "||").replace(u"审判长", "||").replace(u"代理院长", "||").replace(u"院长","||") \
        .replace(u"代理审判员", "||").replace(u"人民审判员", "||") \
        .replace(u"助理审判员", "||").replace(u"审判员", "||").replace(u"人民陪审员", "||").replace(u"代理陪审员", "||").replace(u"陪审员","||") \
        .replace("||||", "||").lstrip("||")
    s = []
    for j in judge_result.split("||"):   # 由于reg_footer
        if len(j) < 4:
            s.append(j)
    judge_result = "||".join(s)

    # reg_footer2 = re.compile(ur'(?:\S{0,2}审判|\S{0,2}院长)\S?', re.S)
    # 如果为空，说明全部有换行，例如：
    # 审判员
    # 某某某
    # if doc_footer_result == "":
    #     for i in range(len(split_result)):
    #         if re.search(reg_footer2, split_result[i]) and len(split_result[i + 1]) < 4:
    #             l.append(split_result[i + 1])
    #
    #     doc_footer_result = "||".join(l)

    return judge_result

def get_doc_footer_one_line(doc_footer):
    doc_footer = doc_footer.replace(u"　", "").replace(" ", "")
    split_result = doc_footer.split("\n")
    reg_footer = re.compile(ur'(?:\S{0,2}审判|\S{0,2}院长|\S{0,2}陪审|执行员|书记员|\S+年\S+月)\S{2,}')
    reg_footer1 = re.compile(ur'(?:\S{0,2}审判|\S{0,2}院长|\S{0,2}陪审|执行员|书记员)\S{0,1}')
    # reg_footer2 = re.compile(ur'^(?:\S{0,2}审判|\S{0,2}院长|\S{0,2}陪审)\S{2,3}', re.S)
    doc_footer_result = ""
    l = []
    for i in range(len(split_result)):
        if re.search(reg_footer, split_result[i]):
            l.append(split_result[i])
        elif re.search(reg_footer1, split_result[i]):
            if i+1 < len(split_result):
                if len(split_result[i + 1]) < 4:
                    l.append(split_result[i] + split_result[i+1].replace("\n",""))

    doc_footer_result =  "\n".join(l).replace(u"代理审判长", u" 代理审判长 ").replace(u"审判长", u" 审判长  ").replace(u"代理审判员", u" 代理审判员") \
        .replace(u"人民审判员", u" 人民审判员").replace(u"助理审判员", u" 助理审判员").replace(u"审判员", u" 审判员  ").replace(u"书记员", u" 书记员  ") \
        .replace(u"人民陪审员", u" 人民陪审员  ").replace(u"代理陪审员", u" 代理陪审员  ").replace(u"陪审员", u" 陪审员  ") \
            .replace(u"二", u" 二").replace(u"代理院长", u" 代理院长  ").replace(u"院长", u" 院长  ").replace(u"执行员", u" 执行员  ")



    return doc_footer_result

def get_result(x):
    # court_idea,judge_result,doc_footer，judge_type
    court_idea = x[1]
    judge_result = x[2].replace("?", "  ")
    doc_footer = x[3].replace("?", "  ")
    judge_type = x[4]
    doc_footer_tmp = ""

    #针对有分段的文书进行法官提取。
    if judge_type == u"判决" or judge_type == u"裁定":

        # reg_footer_tmp = re.compile(ur'\n(?:\S{0,2}审[　  ]{0,2}判|\S{0,2}执[　  ]{0,2}行员|\S{0,2}院[　  ]{0,2}长)[ ]{0,6}\S{2,}')
        reg_footer_tmp = re.compile(ur'\n(?:\S{0,2}审[　 ]{0,2}判|\S{0,2}执[　 ]{0,2}行员|\S{0,2}院[　 ]{0,2}长).*',re.S)
        ss = re.search(reg_footer_tmp,judge_result)
        if ss:
            judge_result = judge_result.replace(ss.group(0),"")
            doc_footer_tmp = ss.group(0) + "\n"

            doc_footer_tmp = doc_footer_tmp.replace(" ","").replace(u"审判长", u" 审判长  ").replace(u"代理审判员", u" 代理审判员") \
                .replace(u"审判员", u" 审判员  ").replace(u"书记员", u" 书记员  ").replace(u"陪审员", u" 陪审员  ") \
                .replace(u"二", u" 二").replace(u"院长", u" 院长  ").replace(u"执行员", u" 执行员  ")

        doc_footer = doc_footer_tmp + doc_footer
        doc_footer = get_doc_footer_one_line(doc_footer)

        judge = get_judge(doc_footer)

        court_idea.replace("?","  ")
        if judge == "":   #doc_footer和judge_result都没有提取出法官，说明可能是无法分段，整篇放到court_idea字段里。
            judge_result, doc_footer = foot_get(court_idea)
            doc_footer = get_doc_footer_one_line(doc_footer)
            judge = get_judge(doc_footer)
            return judge,None,None, court_idea

        return judge,judge_result,doc_footer,court_idea

    else:   #针对没有分段的数据提取法官。

        court_idea = court_idea.replace("?", "  ")
        # print court_idea

        judge_result, doc_footer = foot_get(court_idea)
        doc_footer = get_doc_footer_one_line(doc_footer)
        judge = get_judge(doc_footer)

        return judge,None,None,court_idea

print time.asctime(time.localtime(time.time()))
conn=pymysql.connect(host='192.168.74.102',user='weiwc',passwd='HHly2017.',db='laws_doc_adjudication',charset='utf8')
cursor = conn.cursor()
# sql = 'select id,judge_result from administration_etl_v2 where id >= 28820 and id <= 28834'   #LOCATE函数，包含||,返回大于0的数值。
# sql = 'select id,judge_result from administration_etl_v2 where uuid = "5aad47c9-ca4f-472c-af31-0a0c06788ca0" '   #LOCATE函数，包含||,返回大于0的数值。
sql = 'select id,court_idea,judge_result,doc_footer,judge_type,uuid from adjudication_civil_etl_v2 '   #id= 28982
# sql = 'select id,court_idea,judge_result,doc_footer,judge_type from administration_etl_v2 where id = 162687 or id = 162925 '   #id= 28982
cursor.execute(sql)
row_2 = cursor.fetchall()

for i in  row_2:
    # print "+++++++++++++++++++++++++++++++++++++++++++++"
    s = get_result(i)
    # print "id=========" + str(i[0])
    # judge, judge_result, doc_footer, court_idea
    # print "judge====================" + s[0]
    # print "judge_result=================" + s[1]
    # print "doc_footer==================" + s[2]
    # print "court_idea===================" + s[3]

    sql2 = " insert into judge_footer_judge_result_court_idea(id,judge,judge_result, doc_footer, court_idea,uuid) values (%s, %s, %s, %s, %s, %s)"
    cursor.execute(sql2, (i[0], s[0],s[1],s[2],s[3],i[5]))
conn.commit()
cursor.close()
conn.close()
print time.asctime(time.localtime(time.time()))
    # print "++++++++++++++++++++++++++++++++++++++++++++++"



