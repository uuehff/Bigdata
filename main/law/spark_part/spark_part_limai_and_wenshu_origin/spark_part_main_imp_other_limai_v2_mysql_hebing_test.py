# -*- coding: utf-8 -*-
"""
对抓取的文书内容进行数据提取
"""
import re
from pyspark import SparkContext,SparkConf
from pyspark.sql import SQLContext
from pyspark.sql.types import *
import json
import pymysql
from lxml import etree
import HTMLParser
import uuid as UUID

reg_link = re.compile(r"<a[^>]+>|</a>", flags=re.S)
reg_blank = re.compile(r'((?!\n)\s)*', flags=re.S)
reg_part = re.compile(r'<span litigantpart></span>')
reg_process = re.compile(r'<span proceeding></span>')
reg_argued = re.compile(r'<span argued></span>')
reg_fact = re.compile(r'<span fact></span>')
reg_court = re.compile(r'<span courtconsider></span>')
reg_result = re.compile(r'<span result></span>')

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
    reg_footer = re.compile(ur'\n(?:\S{0,2}审判).*(?:书记员|\S+年\S+月)\S+', re.S)
    items = items.replace("\\n", '\n')
    footer_result = re.findall(reg_footer, items)

    if footer_result:
        # footer_result[0]中可能有特殊符号：类似？号等等，？在split的pattern中属于特殊字符，因此要替换掉再分割.
        items_tmp = items.replace(footer_result[0],"!1qw23er4!")

        lp = re.split("!1qw23er4!",items_tmp)
        doc_footer = footer_result[0].strip() + lp[1]

        doc_footer = doc_footer.replace(u"审判长",u" 审判长  ").replace(u"代理审判员", u" 代理审判员")\
            .replace(u"审判员",u" 审判员  ").replace(u"书记员", u" 书记员  ").replace(u"陪审员",u" 陪审员  ")\
            .replace(u"二",u" 二")
        return lp[0],doc_footer   #result,doc_footer
    else:
        return items,""

def remove_html(html_data):
    """
    移除HTML标签
    :param html_data:
    :return:
    """
    html_item = re.sub(reg_blank, "", html_data)
    if html_item:
        item_list = etree.HTML(html_item).xpath('//text()')
        html_text = "\n".join(item_list).strip()
    else:
        html_text = ''
    return html_text

def format_content(content):
    """
    理脉网内容分段
    :param content:
    :return:
    """
    # reg_link = re.compile(r"<a[^>]+>|</a>", flags=re.S)
    # reg_blank = re.compile(r'((?!\n)\s)*', flags=re.S)

    content_dict = dict()
    content_text = HTMLParser.HTMLParser().unescape(content)
    # content_text = html.unescape(content)
    print content_text
    content_text = re.sub(reg_link, "", content_text)

    print content_text

    # content_text = content_text.replace("<span litigantpart></span>","0|0|0|11").replace("<span proceeding></span>","0|0|0|22").replace("<span argued></span>","0|0|0|33") \
    #     .replace("<span fact></span>", "0|0|0|44").replace("<span courtconsider></span>", "0|0|0|55") \
    #     .replace("<span result></span>", "0|0|0|66")
    #
    # rl = content_text.split("0|0|0|")
    # for i in rl:
    #     if i.startswith("11"):
    #         content_dict['member'] = remove_html(i).replace("11","")
    #     elif i.startswith("22"):
    #         content_dict['process'] = remove_html(i).replace("22","")
    #     elif i.startswith("33"):
    #         content_dict['request'] = remove_html(i).replace("33","")
    #     elif i.startswith("44"):
    #         content_dict['fact'] = remove_html(i).replace("44","")
    #     elif i.startswith("55"):
    #         content_dict['idea'] = remove_html(i).replace("55","")
    #     elif i.startswith("66"):
    #         content_dict['result'] = remove_html(i).replace("66","")

    content_text = content_text.replace("<a type='dir' name='DSRXX'></a>", "0|0|0|11").replace(
        "<a type='dir' name='SSJL'></a>", "0|0|0|22") \
        .replace("<a type='dir' name='AJJBQK'></a>", "0|0|0|33") \
        .replace("<a type='dir' name='CPYZ'></a>", "0|0|0|44").replace("<a type='dir' name='PJJG'></a>", "0|0|0|55") \
        .replace("<a type='dir' name='WBWB'></a>", "0|0|0|66")

    rl = content_text.split("0|0|0|")
    for i in rl:
        if i.startswith("11"):
            content_dict['member'] = remove_html(i).replace("11", "")
        elif i.startswith("22"):
            content_dict['process'] = remove_html(i).replace("22", "")
        elif i.startswith("33"):
            content_dict['request'] = remove_html(i).replace("33", "")
        elif i.startswith("44"):
            content_dict['idea'] = remove_html(i).replace("44", "")
        elif i.startswith("55"):
            content_dict['result'] = remove_html(i).replace("55", "")
        elif i.startswith("66"):
            content_dict['doc_footer'] = remove_html(i).replace("66", "")

    return content_dict,content_text

def doc_items(items):
    id = items[0]
    uuid = items[1]
    doc_content = items[2]
    caseid = items[3]
    title = items[4]
    court = items[5]
    lawlist = items[6]
    reason_type = items[7]
    type = items[8]
    judge_type = items[9]

    if not doc_content or not doc_content.endswith('/div&gt;'):
        return None

    content_text,doc_text = format_content(doc_content)
    # if not content_text:
    #     return None

    # 格式化后的内容
    # content = content_text.get('content')
    # if len(content) < 120:
    #     return None

    party_info = content_text.get('member', '').replace("\\n","\n")
    trial_process = content_text.get('process', '')
    trial_request = content_text.get('request', '')
    court_find = content_text.get('fact', '')
    court_idea = content_text.get('idea', '')
    judge_result = content_text.get('result', '')

    uuid_ = unicode(UUID.uuid3(UUID.NAMESPACE_DNS2, uuid.encode("utf8"))).replace("-","")  # 基于平台的命名空间 + uuid确定新的uuid_,uuid_是一个对象，需要转化为字符串

    court_find = pymysql.escape_string(court_find).replace("\\n","\n")
    trial_process = pymysql.escape_string(trial_process).replace("\\n","\n")
    trial_request = pymysql.escape_string(trial_request).replace("\\n","\n")
    court_idea = pymysql.escape_string(court_idea).replace("\\n","\n")
    judge_result = pymysql.escape_string(judge_result).replace("\\n","\n")
    judge_result, doc_footer = foot_get(judge_result)


    if judge_type.startswith(u"决定") or judge_type.startswith(u"通知"):
        court_idea_all = party_info  + trial_process + trial_request + court_find + court_idea + judge_result + doc_footer
        if court_idea_all != "":
            court_idea = party_info + "\n\n" + trial_process +"\n\n" + trial_request +"\n\n" + court_find +"\n\n" + court_idea +"\n\n" + judge_result +"\n\n" + doc_footer
            court_idea = court_idea.replace("\n\n\n\n\n\n","\n\n").replace("\n\n\n\n","\n\n")
            # return (id,uuid,party_info,trial_process,trial_request,court_find,court_idea,judge_result,doc_footer,uuid_,caseid,title,court,lawlist,u"执行",type,judge_type)

        else:
            print "3333333333333333333333"
            doc_text = remove_html(doc_text)
            print doc_text
            reg_caseid = re.compile(ur'\n[(（](?:20|19|2０|2O)\S+号\S*', re.S)
            # reg_caseid = re.compile(ur'\n(?:（20)\S+号\S*', re.S) #\S* 号下面有0或多个非空字符
            doc_result = re.findall(reg_caseid, doc_text)

            if doc_result:
                doc_tmp = doc_text.replace(doc_result[0], "!1qw23er4!")
                court_idea = re.split("!1qw23er4!", doc_tmp)[1]
            else:
                court_idea = doc_text

            # return (id,uuid,party_info,trial_process,trial_request,court_find,court_idea,judge_result,doc_footer,uuid_,caseid,title,court,lawlist,u"执行",type,judge_type)

            # print "doc_text=============" + doc_text
            # print "doc_text============" + doc_text
            # print "court_idea============" + court_idea

            # for i in remove_html(doc_text).split("\n"):
            #     print "0====" + i
    else:
        ""
        # return (id,uuid,party_info,trial_process,trial_request,court_find,court_idea,judge_result,doc_footer,uuid_,caseid,title,court,lawlist,u"执行",type,judge_type)

    items_dict = dict(party_info=party_info, trial_process=trial_process, trial_request=trial_request,
                      court_find=court_find, court_idea=court_idea, judge_result=judge_result, is_format=1,doc_footer=doc_footer)
    for j in items_dict.keys():
        print j,":::::::",items_dict[j]

if __name__ == "__main__":
    conn = pymysql.connect(host='192.168.10.22', user='tzp', passwd='123456', db='laws_doc',charset='utf8')
    # conn = pymysql.connect(host='192.168.74.102', user='weiwc', passwd='HHly2017.', db='laws_doc',charset='utf8')
    cursor = conn.cursor()
    # sql = 'select id,judge_result from administration_etl_v2 where id >= 28820 and id <= 28834'   #LOCATE函数，包含||,返回大于0的数值。
    # sql = 'select id,judge_result from administration_etl_v2 where uuid = "5aad47c9-ca4f-472c-af31-0a0c06788ca0" '   #LOCATE函数，包含||,返回大于0的数值。
    # sql = 'select id,uuid,doc_content,caseid,title,court,lawlist,reason_type,type,judge_type from imp_other where id = 4302837 '  # id= 4302821
    sql = 'select id,uuid,doc_content from adjudication where id = 1 '  # id= 4302821
    cursor.execute(sql)
    row_2 = cursor.fetchall()

    for i in row_2:
        # doc_items(i)
        format_content(i[2])
