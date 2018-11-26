# -*- coding:utf-8 -*-

# import datetime
# import html
import re

import multiprocessing
import xlrd
from lxml import etree
import HTMLParser
import pymysql
import json


def as_text(v):
    if v is None:
        return None
    elif isinstance(v, unicode):
        return v
    elif isinstance(v, str):
        return v.decode('utf-8', errors='ignore')
    else:
        raise ValueError('Invalid type %r' % type(v))


def format_html(content):
    """去除html符号"""

    html_parser = HTMLParser.HTMLParser()
    content_text = html_parser.unescape(content)
    selector = etree.HTML(content_text)
    source_data = selector.xpath('string(*)')
    source_data = str(source_data.encode("utf-8"))

    return source_data


def text_replace(content_text):
    """ 文本规范化"""
    content_text = content_text
    content_text = content_text.replace(' ','')
    content_text = content_text.replace("　","")
    content_text = content_text.replace("	","")
    content_text = content_text.strip()
    content_text = content_text.replace('<<', '《')
    content_text = content_text.replace('>>', '》')
    content_text = content_text.replace('〈〈', '《')
    content_text = content_text.replace('〉〉', '》')
    content_text = content_text.replace(':','：')
    content_text = content_text.replace(',', '，')
    content_text = content_text.replace('.', '。')

    return content_text

tt_n = 0
wrong_n = 0


def divide_para(para):
    """分段"""
    global right_n,wrong_n
    divide_result = []
    a1 = re.compile(ur"([^\n。]{1,100}(?<=指控).[\u4e00-\u9fa5].*(?:审理终结).)|((?:本院认为|本庭认为).+?[\u4e00-\u9fa5].*(?:判[决处]如下).)")
    # a2 = re.compile(ur"([^\n。]{0,50}(?:指控).[\u4e00-\u9fa5].*(?:审理终结|无异议).{0,100}[\n。])|([^\n。]{0,200}(?:判[决处]如下).)")
    # a1 = re.compile(ur"([^\n。]{0,50}(?:指控).[\u4e00-\u9fa5].*(?:审理终结).{0,100}[\n。])|([^\n。]{0,200}(?:判[决处]如下).)")
    # a3 = re.compile(ur"((?:判决结果).*(?=判决理由)|(?:法律依据).+$)")
    f1 = re.split(a1, para)
    a = 0
    b = 0
    if len(f1) == 7:
        # print "divide right:"
        for i in f1:
            a += 1
            # print a
            # print i
        # f2 = re.split(a2, para)
        divide_result.append(f1[0])  # 0 参与人信息
        divide_result.append(f1[1])  # 1 审理过程
        divide_result.append(f1[3])  # 2 诉方/辩方/事实认定（事实调查）
        divide_result.append(f1[-2]) # 3 法院观点/法律条例

        divide_result.append(f1[-1]) # 4 审判结果
        # print divide_result[-1]
        # print "\n"
    else:
        divide_result = ["None"]
        # print "wrong: ",para,"\n"
        wrong_n += 1
    return divide_result

wrong_divide = 0

# 读取标准案由列表
data = xlrd.open_workbook("tb_reason.xlsx")
table = data.sheet_by_name("tb_reason")
law_list = [table.cell(i,ord('B')-ord('A')).value for i in range(1,505)]

# 读取案由替换列表
data2 = xlrd.open_workbook("replace.xlsx")
table2 = data2.sheet_by_name("replace")
law_list_doc = [table2.cell(i,ord('B')-ord('A')).value for i in range(1,4538)]
law_list_stand = [table2.cell(i,ord('D')-ord('A')).value for i in range(1,4538)]
len_law = len(law_list_doc)


def get_org_and_reason(divide_result):
    """获取审理流程 trial_process, 第二段"""
    """获取人民检察院 doc_oriligigation，从第二段获取"""
    """获取审判员 fact_finder， 从第二段获取"""

    """获取判决结果 judg_result,第五段"""
    """获取案由 doc_reason，从第五段获取"""
    """获取审判长 judge_chief，从第五段获取"""
    """获取审批团成员 judge_member，从第五段获取"""

    global wrong_divide,law_list,law_list_stand,len_law
    trial_pro = ""
    result = ""
    crime_reason = ""
    oriligigation = ""
    finder = ""
    judge_result = ""
    judge_chief = ""
    judge_member = ""

    org_res = ""
    finder_res = ""
    finder_res2 = ""
    chief_res = ""
    member_res = ""
    crime_res = ""
    judge_res = ""
    footer_res = ""
    footer = ""
    org_search = re.compile(ur"[^\n，]{0,50}(?:检察院)")
    org_search2 = re.compile(ur"(?<=某|男|女).*?(?:检察院)")
    finder_search = re.compile(ur'(?<=检察员|检察长|检查员)[\u4e00-\u9fa5].*?(?=出庭|.被告人)')
    finder_search2 = re.compile(ur'(?<=指派)[\u4e00-\u9fa5].*?(?=出庭|.被告人)')
    # person_search = re.compile(ur"(?<=被告人)[\u4e00-\u9fa5].*?(?=犯)")
    crime_search = re.compile(ur"(?<=犯)(.*?)(?:罪[(\W.)，])")
    judge_search = re.compile(ur"[\u4e00-\u9fa5].*?(?:.副本.{1,5}份).")
    # chief_search = re.compile(ur"(?<=审判长)[\u4e00-\u9fa5]+?(?=代理审判员|助理审判员|审判员|二〇|一九|人民陪审员|人民审判员)")
    chief_search = re.compile(ur"(?<=审判长).{0,1}?[\u4e00-\u9fa5]+?.{0,1}(?=代理审判员|助理审判员|审判员|人民陪审员|人民审判员|二〇|一九|二零|$)")
    member_search = re.compile(ur"(?<=审判员|陪审员).{0,1}?[\u4e00-\u9fa5]+?.{0,1}(?=二〇|二○|二Ｏ|二О|一九|二０|二0|二零)")
    footer_search = re.compile(ur"(代理){0,1}(?:审判).*?((?:$)|(?=附|本案|相关|法律))")
    # footer_search = re.compile(ur'(代理){0,1}(?:审判).*(?:书记员|\S+年\S+月)\S+', re.S)

    # member_search2 = re.compile(ur'(?<=书记员).{0,3}[\u4e00-\u9fa5]+?.{0,3}(?=附：|附相关法|$)')

    if len(divide_result) == 5:
        trial_pro = divide_result[1]
        # print trial_pro, "\n"
        result = divide_result[-1]
        # print result,"\n"
        if trial_pro:
            org_res = re.search(org_search,trial_pro)
            finder_res = re.search(finder_search,trial_pro)
            finder_res2 = re.search(finder_search2,trial_pro)
            # person_res = re.search(person_search,trial_pro)
        if result:
            # print result,"\n"
            f = re.findall(crime_search, result)
            crime_res = list(set(f))
            judge_res = re.search(judge_search, result)
            chief_res = re.search(chief_search,result)
            member_res = re.search(member_search,result)
            footer_res = re.search(footer_search,result)
            # member_res2 = re.search(member_search2,result)
        if footer_res:
            footer = footer_res.group(0)
            footer = footer.replace("u3000","")


        if member_res:
            judge_member = member_res.group(0)
            judge_member = judge_member.replace("（".decode("utf-8"), "")
            judge_member = judge_member.replace("）".decode("utf-8"), "")
            judge_member = judge_member.replace("代理审判员".decode("utf-8"),"||")
            judge_member = judge_member.replace("人民陪审员".decode("utf-8"), "||")
            judge_member = judge_member.replace("人民赔审员".decode("utf-8"), "||")
            judge_member = judge_member.replace("人民审判员".decode("utf-8"), "||")
            judge_member = judge_member.replace("审判员".decode("utf-8"),"||")
            judge_member = judge_member.replace("陪审员".decode("utf-8"),"||")

        #     print judge_member
        # else:
        #     print result

        if chief_res: # 获取审判长
            judge_chief = chief_res.group(0)
            judge_chief = judge_chief.replace("（".decode("utf-8"),"")
            judge_chief = judge_chief.replace("）".decode("utf-8"),"")

        if judge_res: # 获取判决结果
            judge_result = judge_res.group(0)
        # else:
        #     print result

        if org_res: # 提取人民检察院
            oriligigation = org_res.group(0)
            org_new = re.search(org_search2,oriligigation)
            if org_new:
                oriligigation = org_new.group(0)
        cri_lst = []
        if crime_res: # 提取案由
            for i in crime_res:
                if i in law_list:
                    if i != "":
                        cri_lst.append(i)
                elif i in law_list_doc:
                    for j in range(len_law):
                        if i == law_list_doc[j]:
                            i = law_list_stand[j]
                            if i != "":
                                cri_lst.append(i)
            cri_lst = list(set(cri_lst))
            if cri_lst:
                crime_reason = cri_lst[0]
                if len(cri_lst) > 1:
                    for i in cri_lst[1:]:
                        crime_reason += "||"
                        crime_reason += i
            # print crime_reason
            # print "\n"


        if finder_res:  # 提取检察员
            finder = finder_res.group(0)
            finder = finder.replace("助理".decode("utf-8"), "")
            finder = finder.replace("代理".decode("utf-8"),"")
            finder = finder.replace("检察员".decode("utf-8"),"")
            finder = finder.replace("检察".decode("utf-8"), "")
            finder = finder.replace("依法".decode("utf-8"), "")
            finder = finder.replace("指派".decode("utf-8"), "")
            finder = finder.replace("、".decode("utf-8"),"||")
            finder = finder.replace("，".decode("utf-8"), "||")
            if "书记员".decode("utf-8") in finder:
                new_finder = re.search(ur"[\u4e00-\u9fa5].*?(?=[||])",finder)
                if new_finder:
                    finder = new_finder.group(0)
            if "附带民事诉讼".decode("utf-8") in finder:
                new_finder = re.search(ur"[\u4e00-\u9fa5].*?(?=[||])",finder)
                if new_finder:
                    finder = new_finder.group(0)

        elif finder_res2:
            finder = finder_res2.group(0)
            finder = finder.replace("检察".decode("utf-8"), "")

            wrong_divide += 1
    # print crime_reason
    return oriligigation,finder,crime_reason,trial_pro,judge_result,judge_chief,judge_member,footer


def reason_format(divide_result):
    list_reason = []

    person_search = re.compile(ur"(?<=被告人)[\u4e00-\u9fa5].*?(?=犯)")
    crime_search = re.compile(ur"(?<=犯)(.*?)(?:罪[(\W.)，])")

    reg_reason = re.compile(
        ur'(?:被告人|被告|告人)([^\s,，]+?)(?=犯[^罪])|(?:犯+)([^罪][\w、)(）（]+?)(?:被告|[,，。；]|判[处决][^、]|有期|罪[、的处]|宣告|单处|免[于予]|一案|事实|依法|\n)')

    reg_reason2 = re.compile(ur"(?:被告人|被告|告人)([^\s,，]+?)(?=犯[^罪])|(?:犯+)([^罪].+?)(?:被告|[,，。；]|判[处决][^、]|有期|罪[、的处]|宣告|单处|免[于予]|一案|事实|依法|\n)")

    reg_title = re.compile(ur'(?:被告人|被告|告人)(\w+?)，\S+?犯(\S+?)罪')
    reg_title2 = re.compile(ur"(?<=被告人)[\u4e00-\u9fa5].*?犯(.*?)(?:罪[(\W.)，])")
    if len(divide_result) == 5:
        result = divide_result[-1]
        list_reason = dict()
        reason_data = re.findall(reg_reason2, result)


        id_list = []
    #
        # if not reason_data:
        #     reason_data = re.findall(reg_title, result)
        #     if reason_data:
        #         item = [(reason_data[0][0], ''), ('', reason_data[0][1])]
        #         reason_data = item

        if reason_data:
            for index, reason_item in enumerate(reason_data):
                if reason_item[0]:
                    id_list.append(index)

            for index_num, num in enumerate(id_list):
                reason_list = []
                if index_num < len(id_list) - 1:
                    for item in reason_data[num + 1:id_list[index_num + 1]]:
                        if item[1]:
                            if len(item[1]) < 25 and u"一款" not in item[1] and u"二款" not in item[1] and u"三款" not in item[1]\
                                    and u"的罪分别处罚" not in item[1] and u"。" not in item[1] and u"，" not in item[1] and u"的全部罪行处罚" not in item[1] and u"或者" not in item[1] \
                                    and u"上述任一类" not in item[1] and u"论处" not in item[1] and u"应当" not in item[1] and u"本节" not in item[1] and u"数罪" not in item[1] and u"有数" not in item[1] \
                                    and u"本条" not in item[1] and u"财产罪一样" not in item[1] and u"与走私罪犯通谋" not in item[1] and u"条规定之罪" not in item[1] and u"前款" not in item[1] \
                                    and u"的犯罪分子" not in item[1]:
                                reason_list.append(item[1])
                    if reason_data[num][0] != "和正在服刑的罪".decode("utf-8") and u"单位" not in reason_data[num][0] and u"已宣判" not in reason_data[num][0] and u"如实供述" not in reason_data[num][0] \
                            and u"行为" not in reason_data[num][0] and u"被告人" not in reason_data[num][0]:
                        list_reason.setdefault(reason_data[num][0], list(set(reason_list)))
                    # if reason_data[num][0] == u"张爱民":
                    #     print result
                else:
                    for item in reason_data[num + 1:]:
                        if item[1]:
                            if len(item[1]) < 25 and u"一款" not in item[1] and u"二款" not in item[1] and u"三款" not in item[1] \
                                    and u"的罪分别处罚" not in item[1] and u"。" not in item[1] and u"，" not in item[1] and u"的全部罪行处罚" not in item[1] and u"或者" not in item[1] \
                                    and u"上述任一类" not in item[1] and u"论处" not in item[1] and u"应当" not in item[1] and u"本节" not in item[1] and u"数罪" not in item[1] and u"有数" not in item[1] \
                                    and u"本条" not in item[1] and u"财产罪一样" not in item[1] and u"与走私罪犯通谋" not in item[1] and u"条规定之罪" not in item[1] and u"前款" not in item[1] \
                                    and u"的犯罪分子" not in item[1]:
                                reason_list.append(item[1])
                    if reason_data[num][0] != "和正在服刑的罪".decode("utf-8") and u"单位" not in reason_data[num][0] and u"已宣判" not in reason_data[num][0] and u"如实供述" not in reason_data[num][0] \
                            and u"行为" not in reason_data[num][0] and u"被告人" not in reason_data[num][0]:
                        list_reason.setdefault(reason_data[num][0], list(set(reason_list)))
                        # if reason_data[num][0] == u"张爱民":
                        #     print result
    if list_reason:
        list_reason = json.dumps(list_reason,ensure_ascii=False)
    else:
        list_reason = ""
    return list_reason




def get_law_and_courtid(divide_result):
    """获取法条名称 law_list  从倒数第二段获取""" # 这里返回的是一个数组
    """获取法院观点 court_idea 从倒数第二段获取""" # 这里返回的是一个字符串

    court_idea = ""
    law_list = []

    split_c = []

    a1 = re.compile(ur"([^\n。]{1,200}(?<=判[处决]如下.))")
    reg_lawlist = re.compile(r'《')
    reg_law = re.compile(r'《.+?》')
    reg_last_law = re.compile(r'第.{1,15}?条.{2,15}?项|第.{1,15}条第[^条]{1,15}(?=款)款|第?[零一二三四五六七八九十百千]{1,15}?条')

    if len(divide_result) == 5:
        law_and_cour = divide_result[-2]
        if law_and_cour:
            split_c = re.split(a1,law_and_cour)
        # if len(split_c) == 1:
        #     print law_and_cour
        if len(split_c) > 1:
            court_idea = split_c[0]

            lawlist = split_c[1]

            lawlist = lawlist.encode("utf-8")
            lawlist = re.sub(r'\n', '', lawlist)
            lawlist_data = re.split(reg_lawlist, lawlist)
            for item in lawlist_data:
                item = '《' + item
                law_data = re.search(reg_law, item)
                if law_data:
                    re.sub('[及和与的之]$', '', item)
                    law_name = law_data.group()
                    last_raw_list = re.findall(reg_last_law, item)
                    last_raw_list = [law_name + law_item for law_item in last_raw_list]
                    law_list.extend(last_raw_list)
    # ll = ""
    # for i in law_list:
    #     ll = i
    #     ll += ","
    law_list = json.dumps(law_list,ensure_ascii=False)
    return court_idea,law_list


def get_party_info(divide_result):
    """获取参与人信息 party_info，第一段"""
    """获取被告律师 defendant，从第一段获得"""
    """获取原告律师 plaintiff，从第一段获得"""
    """获取第三方律师 third， 从第一段获得"""

    party_info = ""
    defendant = ""
    plaintiff = ""
    third = ""

    defen_res = ""
    plain_res = ""


    defendant_search = re.compile(ur"(?<=辩护人)[\u4e00-\u9fa5].+?(?=，|。)")
    plain_search = re.compile(ur"[\u4e00-\u9fa5].*?(?=辩护人)")
    plaintiff_search = re.compile(ur"[。]{0,1}(?<=委托代理人|诉讼代理人)[\u4e00-\u9fa5].+?(?=，|。|$)")
    plaintiff_search2 = re.compile(ur"(?<=代理人)[\u4e00-\u9fa5].+?(?=$)")

    if len(divide_result) == 5:
        party_info = divide_result[0]
        # print party_info,"\n"
        if party_info:
            defen_res = re.search(defendant_search,party_info)
            plain_res = re.search(plain_search,party_info)

        if plain_res:
            p = plain_res.group(0)
            plainiff_res = re.search(plaintiff_search,p)
            if plainiff_res:
                plaintiff = plainiff_res.group(0)
                plaintiff = plaintiff.replace("、".decode("utf-8"),"||")
                plaintiff = plaintiff.replace("暨".decode("utf-8"), "")
                plaintiff = plaintiff.replace("及".decode("utf-8"), "")
                plaintiff = plaintiff.replace("附带民事诉讼原告人".decode("utf-8"),"")
                if "代理人".decode("utf-8") in plaintiff:
                    plaintiff_res2 = re.search(plaintiff_search2,plaintiff)
                    if plaintiff_res2:
                        plaintiff = plaintiff_res2.group(0)

        if defen_res:
            defendant = defen_res.group(0)
            defendant = defendant.replace("、".decode("utf-8"),"||")
            defendant = defendant.replace("暨".decode("utf-8"), "")
            defendant = defendant.replace("及".decode("utf-8"), "")
            defendant = defendant.replace("附带民事诉讼代理人".decode("utf-8"),"")
            defendant = defendant.replace("附带民事诉委托理人".decode("utf-8"),"")
            defendant = defendant.replace("诉讼代理人".decode("utf-8"),"")
            defendant = defendant.replace("委托代理人".decode("utf-8"),"")

    return party_info,defendant,plaintiff

aa = 0
def get_request_reply(divide_result):
    """获取诉求 trial_request ， 从第三段获取"""
    """获取庭审答辩 trial_reply ，从第三段获取"""
    """获取事实认定 court_find ，从第三段获取"""
    global aa
    trial_request = ""
    trial_reply = ""
    court_find = ""
    request_split = re.compile(ur"[^\n。]{0,20}(?:上述|以上)(指控的){0,1}(犯罪|案件){0,1}(?:事实)[，]{0,1}[\u4e00-\u9fa5].*?(?=$)")
    find_search = re.compile(ur"[^\n。]{0,20}(?:上述|以上)(指控的){0,1}(犯罪|案件){0,1}(?:事实|指控)[，]{0,1}[\u4e00-\u9fa5].*?(?=$)")
    find_search2 = re.compile(ur"[^\n。]{0,50}(?:上述事实|以上事实)[\u4e00-\u9fa5].*?(?=$)")
    reply_search = re.compile(ur"[^\n。]{0,100}(?:异议)[，]{0,1}.*?(?:。)((?:辩护).*?(?=经审理查明)){0,1}")
    if len(divide_result) == 5:
        info = divide_result[2]
        # print info,"\n"
        find_res = re.search(find_search,info)
        request_res = re.split(request_split,info)
        reply_res = re.search(reply_search,info)
        find_res2 = re.search(find_search2,info)
        if find_res:
            court_find = find_res.group(0)
            # print court_find,"\n"

        if len(request_res) > 1:
            nn = 0
            trial_request = request_res[0]
            # for i in request_res:
            #     nn += 1
            #     print nn
            #     print i,"\n"
            # print request_res[0],"\n"
        if reply_res:
            trial_reply = reply_res.group(0)

    return court_find,trial_request,trial_reply


def get_time(divide_result):
    fst = ""
    judg =""
    judg2 =""
    public =""
    rec = ""
    rec2 = ""
    time_str = ""
    list_tt = []
    if len(divide_result) == 5:
        trial_process = divide_result[1]
        reg_first = re.compile(ur'(\d{2,5}年\d{1,2}月\d{1,2}[日号]?)')
        reg_judge = re.compile(ur'(\d{0,5}年?\d{1,2}月\d{1,2}[日号]?).{0,16}(?:审理)')
        reg_public = re.compile(ur'(\d{0,5}年?\d{1,2}月\d{1,2}[日号]?)\S*(?:向本院)')
        reg_record = re.compile(ur'(\d{0,6}年?\d{1,2}月\d{1,2}[日号]?).{0,10}(?:立案|受理)')
        date_first = re.findall(reg_first, trial_process)
        date_judge = re.findall(reg_judge, trial_process)
        # date_public = re.findall(reg_public,trial_process)
        date_record = re.findall(reg_record,trial_process)
        # list_tt = []
        if date_first:
            qs = "起诉".decode("utf-8")
            fst = date_first[0]
            fst = fst.replace("年".decode("utf-8"), "-")
            fst = fst.replace("月".decode("utf-8"), "-")
            fst = fst.replace("日".decode("utf-8"), "")
            lst1 = [fst,qs]
            list_tt.append(lst1)
            # fst = "起诉：".decode("utf-8") + fst
        if date_record:
            la = "立案".decode("utf-8")
            rec = date_record[0]
            rec = rec.replace("年".decode("utf-8"), "-")
            rec = rec.replace("月".decode("utf-8"), "-")
            rec = rec.replace("日".decode("utf-8"), "")
            if rec[0] == "-":
                if date_first:
                    df = date_first[0]
                    rec = df[0:4] + rec
                else:
                    rec = rec[1:]
            lst3 = [rec, la]

            list_tt.append(lst3)
        if date_judge:
            sl = "审理".decode("utf-8")
            judg = date_judge[0]
            judg = judg.replace("年".decode("utf-8"), "-")
            judg = judg.replace("月".decode("utf-8"), "-")
            judg = judg.replace("日".decode("utf-8"), "")
            if judg[0] == "-":
                if date_first:
                    df = date_first[0]
                    judg = df[0:4] + judg
                else:
                    judg = judg[1:]
            lst2 = [judg,sl]

            list_tt.append(lst2)


    return rec,list_tt


# 读取未分段的文本内容
# database
conn = pymysql.connect(host="192.168.10.24",user="raolu",passwd="123456",db="laws_doc",charset="utf8")

cur = conn.cursor()
# aa = cur.execute("select id,uuid,doc_content,caseid,title,court,casedate from judgment where id > 1876056 and is_format != 1 and is_format != 0 "
#                  "and is_format != 3 and doc_from != 'wenshu-gov' limit 100")
# aa = cur.execute("select id,doc_content from judgment where id > 1876056 and is_format != 1 and is_format != 0 "
#                  "and is_format != 3")
aa = cur.execute("select id,doc_content from judgment where id = 1965278")
a = cur.fetchall()
ww = 0
cc = 0
for i in a:
    tt_n += 1
    cc += 1
    n = i[0]
    para = format_html(i[1])
    para2 = text_replace(para)
    p2 = as_text(para2)
    dd = divide_para(p2)
    # if len(dd) == 5:
    #     for i in dd:
    #         print i,"\n"
    reason_list = reason_format(dd)

    # 更新非标准案由
    sql = "update judg2 set doc_reason = '%s' where id ='%s'" % (reason_list, n)
    cur.execute(sql)
    conn.commit()
    if n % 500 == 0:
        print n
    # some_info = get_org_and_reason(dd)  # 获取检察院，检察员，案由，审理流程，判决结果，审判长，陪审团成员，结尾(8个字段，每个字段都是字符串)
    # law_court = get_law_and_courtid(dd)  # 获取法院观点，法条名称（2个字段，都是字符串）
    # date_list = get_time(dd) #获取立案时间，时间线（两个字段，都是字符串）
    # if i[6]:
    #     public_time = [i[6],"判决".decode("utf-8")]
    # timelist = date_list[1]
    # timelist.append(public_time)
    #
    # timelist = json.dumps(timelist,ensure_ascii=False)
    #
    #
    # party = get_party_info(dd) # 获取参与人信息，被告律师，原告律师（3个字段，都是字符串）
    # info_requst = get_request_reply(dd) # 获取诉求，庭审答辩，事实认定

    # if some_info[0] and some_info[2] and some_info[3] and some_info[4] and law_court[0] and law_court[1] and party[0]:
    #     try:
    #         value = [i[0],i[1],i[3],i[4],i[5],i[6],some_info[0],some_info[1],some_info[2],some_info[3],some_info[4],some_info[5],some_info[6],some_info[7],law_court[0],law_court[1],party[0],party[1],party[2],date_list[0],timelist,info_requst[0],info_requst[1],info_requst[2]]
    #         sql = "insert into judg2(id,uuid,caseid,title,court,casedate,doc_oriligigation,fact_finder,reason,trial_process,judge_result,judge_chief," \
    #               "judge_member,doc_footer,court_idea,lawlist,party_info,defendant,plaintiff,record_time,timeline,court_find,trial_request,trial_reply) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    #         cur.execute(sql,value)
    #         conn.commit()
    #     except Exception:
    #         print "wrong"



# 对源文本进行处理
# p1 = format_html(content_list[5])
# p2 = text_replace(p1)
# divide_res = divide_para(p2)
# for i in divide_res:
#     print i
# print get_org_and_reason(divide_res)



print "未处理：",wrong_n
print "总数：",tt_n
print "未分出的：",ww

