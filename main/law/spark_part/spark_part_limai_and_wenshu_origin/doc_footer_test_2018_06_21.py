# -*- coding: utf-8 -*-

import re
import pymysql


def foot_get(items):

    # 正则前向否定：(?!):http://www.cnblogs.com/demonspider/p/3523196.html
    # 使用“前向否定界定符”匹配一个文件名，文件名通过 "." 分成基本名和扩展名两部分；
    # 如果想匹配扩展名不是 "bat" 的文件名？
    #匹配不以bat结尾的文件名，表达式：  .*[.](?!bat$).*$

    # 前向的意思：如果表达式 bat$ 在这里没有匹配，尝试模式的其馀部分(即.*$)；如果bat$ 匹配，整个模式将失败，将不会再尝试后面的匹配规则。
    # bat$後面的 $ 确保仅仅以bat结尾的文件名过滤掉，像 "sample.batch"这样的的能够保留。
    # 将另一个文件扩展名排除在外现在也容易；简单地将其做为可选项放在界定符中。下面的这个模式将以 "bat" 或 "exe"结尾的文件名排除在外。

    #匹配不以bat或exe结尾的文件名，表达式：  .*[.](?!bat$ | exe$).* $

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
    reg_footer = re.compile(ur'\n(?:\S{0,2}审判).*(?:书记员|\S+年\S+月)\S+', re.S)
    items = items.replace("\\n", '\n')
    footer_result = re.findall(reg_footer, items)

    if footer_result:
        # footer_result[0]中有？号，？在split的pattern中属于特殊字符，因此可以替换掉再分割.
        lp = re.split(footer_result[0].replace("?","").replace(u"？",""),items.replace("?","").replace(u"？",""))
        doc_footer = footer_result[0].strip() + lp[1]

        doc_footer = doc_footer.replace(u"审判长",u" 审判长  ").replace(u"代理审判员", u" 代理审判员")\
            .replace(u"审判员",u" 审判员  ").replace(u"书记员", u" 书记员  ").replace(u"陪审员",u" 陪审员  ")\
            .replace(u"二",u" 二")
        return lp[0],doc_footer   #result,doc_footer
    else:
        return items,""

conn=pymysql.connect(host='192.168.74.102',user='weiwc',passwd='HHly2017.',db='laws_doc_administration',charset='utf8')
cursor = conn.cursor()
# sql = 'select id,judge_result from administration_etl_v2 where id >= 28820 and id <= 28834'   #LOCATE函数，包含||,返回大于0的数值。
# sql = 'select id,judge_result from administration_etl_v2 where uuid = "5aad47c9-ca4f-472c-af31-0a0c06788ca0" '   #LOCATE函数，包含||,返回大于0的数值。
sql = 'select id,judge_result from administration_etl_v2 where uuid = "4d3e2c42-888e-4985-a79f-a7270111c2b8" '   #id= 28982
cursor.execute(sql)
row_2 = cursor.fetchall()

for i in  row_2:
    print "id===========" + str(i[0])
    print "items==========" +  i[1]
    s = foot_get(i[1])
    print "result=========" + s[0]
    print "doc_footer=====" + s[1]
    # print "==========================="



