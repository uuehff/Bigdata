# -*- coding: utf-8 -*-
"""
对抓取的文书内容进行数据提取
"""
import re
import pymysql
import time
from lxml import etree
import HTMLParser

# #去掉<a>标签
reg_link = re.compile(r"<a[^>]+>|</a>", flags=re.S)
#下面使用，用来替换除\n之外的空白符；当遇见一个字符时，先看是否为"\n"，是的话则失败看下一个字符，如果不是"\n"，则使用后面的规则来匹配当前字符。
reg_blank = re.compile(r'((?!\n)\s)+', flags=re.S)
# reg_part = re.compile(r'<span litigantpart></span>')  # <a type='dir' name='DSRXX'></a>, 当事人信息
# reg_process = re.compile(r'<span proceeding></span>')  # <a type='dir' name='SSJL'></a>，审理过程
# reg_argued = re.compile(r'<span argued></span>')  # <a type='dir' name='AJJBQK'></a> ，诉讼请求
# reg_fact = re.compile(r'<span fact></span>')                                         #法院查明
# reg_court = re.compile(r'<span courtconsider></span>')  # <a type='dir' name='CPYZ'></a> #法院认为
# reg_result = re.compile(r'<span result></span>')     #<a type='dir' name='PJJG'></a>    #判决结果
# doc_footer                                       #<a type='dir' name='WBWB'></a>

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
    reg_footer = re.compile(ur'\n(?:\S{0,2}审[　  ]{0,2}判|\S{0,2}执[　  ]{0,2}行员|\S{0,2}院[　  ]{0,2}长).*(?:书[　  ]{0,2}记员|\S+年\S+月)\S+', re.S)
    items = items.replace("\\n", '\n')
    footer_result = re.findall(reg_footer, items)

    if footer_result:
        # footer_result[0]中可能有特殊符号：类似？号等等，？在split的pattern中属于特殊字符，因此要替换掉再分割.
        items_tmp = items.replace(footer_result[0],"!1qw23er4!")

        lp = re.split("!1qw23er4!",items_tmp)
        doc_footer = footer_result[0].strip() + lp[1]

        doc_footer = doc_footer.replace(u"审判长",u" 审判长  ").replace(u"代理审判员", u" 代理审判员")\
            .replace(u"审判员",u" 审判员  ").replace(u"书记员", u" 书记员  ").replace(u"陪审员",u" 陪审员  ")\
            .replace(u"二",u" 二").replace(u"执行员",u" 执行员 ").replace(u"院长",u" 院长 ")
        return lp[0],doc_footer   #result,doc_footer
    else:
        return items,""


def format_content(content, b_value):
    """
    理脉网内容分段
    :param content:

    :return:
    """
    content_dict = dict()


    content_text = HTMLParser.HTMLParser().unescape(content)  # python2的代码
    # content_text = html.unescape(content)    #python3的代码

    # , "不公开理由":"",
    # ur"[\u4e00-\u9fa5]"
    # pri_reason_re = re.search(ur"不公开理由\":\"[\u4e00-\u9fa5]{0,200}\"",content_text)    #等价于下面的方式，使用三个引号‘’‘将字符串括起来。

    pri_reason_re = re.search(ur'''不公开理由":"[\u4e00-\u9fa5、：，-]{0,200}"''', content_text)
    if pri_reason_re:
        content_dict['pri_reason'] = pri_reason_re.group(0).replace(ur'''不公开理由":"''', "").replace(ur'''"''', "")

    content_text = content_text.replace("<a type='dir' name='DSRXX'></a>", "0|0|0|11").replace("<a type='dir' name='SSJL'></a>", "0|0|0|22") \
        .replace("<a type='dir' name='AJJBQK'></a>", "0|0|0|33") \
        .replace("<a type='dir' name='CPYZ'></a>", "0|0|0|44").replace("<a type='dir' name='PJJG'></a>", "0|0|0|55") \
        .replace("<a type='dir' name='WBWB'></a>", "0|0|0|66")

    content_text = re.sub(reg_link, "", content_text)  # replace后再去掉<a>标签

    rl = content_text.split("0|0|0|")

    ss = remove_html(rl[0])
    content_dict['court'] = ""
    # "法院名称":"长沙市望城区人民法院"
    court_re = re.search(ur'''法院名称":"[\u4e00-\u9fa5]{3,200}"''', content_text)
    if court_re:
        content_dict['court'] = court_re.group(0).replace(ur'''法院名称":"''', "").replace(ur'''"''', "")
    else:
        for c in b_value:
            if c in ss:
                content_dict['court'] = c
                break

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
            content_dict['result'] = re.split(ur"\\\"}\";", remove_html(i).replace("55", ""))[0]
        elif i.startswith("66"):
            content_dict['doc_footer'] = re.split(ur"\\\"}\";", remove_html(i).replace("66", ""))[0]

    return content_dict,content_text


def remove_html(html_data):
    """
    移除HTML标签
    :param html_data:
    :return:
    """
    html_item = re.sub(reg_blank, "", html_data)
    if html_item:
        item_list = etree.HTML(html_item).xpath('//text()')
        # html_text = "\n".join(item_list).strip()
        html_text = "".join(item_list).strip()
    else:
        html_text = ''
    return html_text


# def doc_items(items, b_value):
#     # id, uuid, doc_content, title,reason_type, caseid, province, court, type, casedate
#     # court,judge_type,reason_type,type,casedate
#     id = items[0]
#     uuid_old = items[1]
#     doc_content = items[2]
#
#     if not doc_content or not doc_content.startswith('$(fun'):
#         return (uuid_old)
#
#     content_text,doc_text = format_content(doc_content, b_value)
#
#     if not content_text:
#         return (uuid_old)
#
#     reason_type = items[4]
#     type = items[8]
#     casedate = items[9]
#
#     reason_type, type, casedate = get_result(reason_type,type,casedate)
#
#
#     party_info = content_text.get('member', '')
#     trial_process = content_text.get('process', '')
#     trial_request = content_text.get('request', '')
#     court_find = content_text.get('fact', '')
#     court_idea = content_text.get('idea', '')
#     judge_result = content_text.get('result', '')
#     doc_footer = content_text.get('doc_footer', '')
#     court = content_text.get('court', '')
#
#     pri_reason = content_text.get('pri_reason',"")
#     #
#     if party_info == "" and trial_process == "" and trial_request == "" and court_find == "" and court_idea == "" and judge_result == "":  # 没有当事人、判决结果的文书，没有意义！
#         court_idea = pri_reason    #如果长文本字段都没有，则将未公开理由放到当事人信息里！！
#
#     party_info = party_info.replace("\\n","\n").replace(r'''\\r''', "").replace("\\r", "")
#     court_find = pymysql.escape_string(court_find).replace("\\n","\n").replace(r'''\\r''', "").replace("\\r", "")
#     trial_process = pymysql.escape_string(trial_process).replace("\\n","\n").replace(r'''\\r''', "").replace("\\r", "")
#     trial_request = pymysql.escape_string(trial_request).replace("\\n","\n").replace(r'''\\r''', "").replace("\\r", "")
#     court_idea = pymysql.escape_string(court_idea).replace("\\n","\n").replace(r'''\\r''', "").replace("\\r", "")
#     judge_result = pymysql.escape_string(judge_result).replace("\\n","\n").replace(r'''\\r''', "").replace("\\r", "")
#     doc_footer = pymysql.escape_string(doc_footer).replace("\\n","\n").replace(r'''\\r''', "").replace("\\r", "")
#
#
#
#     uuid = unicode(UUID.uuid3(UUID.NAMESPACE_DNS2, uuid_old.encode("utf8"))).replace("-","")  # 基于平台的命名空间 + uuid确定新的uuid_,uuid_是一个对象，需要转化为字符串
#
#     court_idea_all = party_info + trial_process + trial_request + court_find + court_idea + judge_result + doc_footer
#     # 无标签下的数据处理,放入court_idea字段
#     if court_idea_all == "":
#         doc_text = remove_html(doc_text)
#         # reg_caseid = re.compile(ur'\n[(（](?:20|19|2０|2O)\S+号\S*', re.S)
#         reg_caseid = re.compile(ur'\n[(（](?:20|19|2０|2O)\S+号\S*', re.S)  # \S* 号下面有0或多个非空字符
#         doc_result = re.findall(reg_caseid, doc_text)
#
#         if doc_result:
#             doc_tmp = doc_text.replace(doc_result[0], "!1qw23er4!")
#             court_idea = re.split("!1qw23er4!", doc_tmp)[1]
#             # if court_idea == "":
#             #     return None
#
#         elif len(doc_text) < 50 and doc_text != "":  # 无标签，无案号，是不公开的数据
#             court_idea = doc_text
#         else:  # 无标签，无案号，且不是不公开的
#             # return None
#             pass
#
#         # 对最终的不正常的court_idea做处理，包含有标签和无标签两种情况得到的court_idea。
#         # c_r = re.compile(ur"[^\u4e00-\u9fa5]")  # 去除court_idea开头不为汉字的。
#         # if re.match(c_r, court_idea.strip()):
#         #     if court_idea_all == "":  # 无标签的数据，court_idea为空的。
#         #         return None
#         #     elif court_idea_all.replace(court_idea, "") == "":  # 有标签的数据，除了court_idea之外全为空的。
#         #         return None
#         #     else:  # 有标签的数据，除了court_idea之外,其他字段还有值的。
#         #         court_idea = ""
#         #     return None
#
#     judge_type = content_text.get('judge_type', '')
#
#     if judge_type.startswith(u"决定") or judge_type.startswith(u"通知") or judge_type.startswith(u"调解") or judge_type == "":
#         court_idea = party_info + "\n\n" + trial_process + "\n\n" + trial_request + "\n\n" + court_find + "\n\n" + court_idea + "\n\n" + judge_result + "\n\n" + doc_footer
#         court_idea = court_idea.replace("\n\n\n\n\n\n", "\n\n").replace("\n\n\n\n", "\n\n")
#         # party_info = ""
#         # trial_process = ""
#         # trial_request = ""
#         # court_find = ""
#         # court_idea = ""
#         # judge_result = ""
#         # doc_footer = ""
#
#
#     court_idea.replace("\\n", "\n").replace(r'''\\r''', "").replace("\\r", "")
#
#     title = items[3]
#     caseid = items[5]
#     province = items[6]
#     # return (id, uuid, party_info, trial_process, trial_request, court_find, court_idea,judge_result, doc_footer, court,uuid_old,judge_type,title,reason_type, caseid, province, type, casedate)


if __name__ == "__main__":
    print time.asctime(time.localtime(time.time()))
    conn = pymysql.connect(host='192.168.74.103', user='weiwc', passwd='HHly2017.', db='law_v2', charset='utf8')
    cursor = conn.cursor()
    sql = 'select id,html_resource from test_law_link where id = 20'  # LOCATE函数，包含||,返回大于0的数值。
    cursor.execute(sql)
    row_2 = cursor.fetchall()


    def process_html_resource(html_resource):
        return html_resource


    for row in row_2:
        law_content = row[1].split('''<div class="law-content">''')[1]
        # <div class="law-title">
        #                 中华人民共和国个人所得税法（2018修正）<a><img src="../../staticelem/img/law/lvIcon.png" style="display: none" alt=""></a>
                    # </div>

        title = law_content.split('''<!--startprint-->''')[0]

        content = law_content.split('''<!--startprint-->''')[1]
        content = content.split('''<!--remark-->''')[1]
        content = content.split('''<!--endprint-->''')[0]


        print title
        print "================================================================="
        print remove_html(title)
        print "================================================================="

        print content
        print "================================================================="
        print remove_html(content)
        print "================================================================="

        # a = '''fafa\n\n\n fgw;fk\n eqrqr  rqr q rq r '''
        # reg_blank = re.compile(r'((?!\n)\s)+', flags=re.S)
        # print re.sub(reg_blank,"#######",a)


    conn.commit()
    cursor.close()
    conn.close()
    print time.asctime(time.localtime(time.time()))