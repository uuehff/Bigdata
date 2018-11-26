# -*- coding:utf-8 -*-

import html
import re
import xlrd
import pymysql
import pickle
import json
import lawyer as ly


def as_text(v):
    if v is None:
        return None
    elif isinstance(v, unicode):
        return v
    elif isinstance(v, str):
        return v.decode('utf-8', errors='ignore')
    else:
        raise ValueError('Invalid type %r' % type(v))

lawyer_list2 = []

def get_defendant(text):
    # pattern_plain2 = re.compile(u"(?P<name>(?<=代理人)[：]{0,1}([\u4e00-\u9fa5]{1,10}.*?)(?=，){0,1})"
    #                             u"(?P<office>(?<=，).*?(?=$))")

    pattern_p = re.compile(u"(?:原告)(：|）){0,1}.*?(?=被告|$)")
    pattern_d = re.compile(u"(?:被告).*?(?:原告|$)")

    pattern_n = re.compile(u"(?<=代理人|辩护人)[：]{0,1}([\u4e00-\u9fa5]{1,10}.*?)(?=，|、)")
    pattern_o = re.compile(u"[^\n，]{2,22}(?:事务所|事务部|援助中心|分所|服务所)")

    pattern_of = re.compile(u"[^\n。]{2,32}(?:事务所|事务部|援助中心|分所|服务所)")

    pl_info = {}  # 原告律师律所
    de_info = {}  # 被告律师律所
    name_d = ""  # 被告律师
    name_p = ""  # 原告律所
    office_d = ""  # 被告律所
    office_p = ""  # 原告律所

    if text:
        text = as_text(text)
        text = text.replace("\n","")
        plain = re.search(pattern_p, text)
        defen = re.search(pattern_d, text)

        if plain:
            # print plain.group(0)
            plain_search = re.findall(pattern_of, plain.group(0))

            for i in plain_search:

                name_p = re.search(pattern_n, i)
                office_p = re.search(pattern_o, i)
                if name_p and office_p:
                    name_p = name_p.group(0)
                    office_p = office_p.group(0)
                    name_p = name_p.replace(u"，", u"")
                    name_p = name_p.replace(u"：", u"")
                    name_p = ly.clean_name(name_p)
                    # name_p = name_p.split(u"、")
                    office_p = office_p.replace(u"系",u"")
                    office_p = ly.clean_office(office_p)
                    # if u"、" in name_p:
                    #     name_p = name_p.split(u"、")
                    #     for nn in name_p:
                    #         pl_info[nn] = office_p
                    # elif u"和" in name_p and len(name_p) > 6:
                    #     name_p = name_p.split(u"和")
                    #     for nn in name_p:
                    #         pl_info[nn] = office_p
                    # else:
                    if name_p and office_p:
                        pl_info[name_p] = office_p
            # print json.dumps(pl_info,ensure_ascii=False)
                    # plain_info.append(pl_info)
            # plain_info = json.dumps(plain_info, ensure_ascii=False)

        if defen:
            # print defen.group(0)
            de2_search = re.findall(pattern_of, defen.group(0))

            for i in de2_search:

                name_d = re.search(pattern_n, i)
                office_d = re.search(pattern_o, i)
                if name_d and office_d:
                    name_d = name_d.group(0)
                    office_d = office_d.group(0)
                    name_d = name_d.replace(u"，", u"")
                    name_d = name_d.replace(u"：", u"")
                    name_d = ly.clean_name(name_d)
                    # name_d = name_d.split(u"、")
                    office_d = office_d.replace(u"系",u"")
                    office_d = ly.clean_office(office_d)
                    if name_d and office_d:
                        de_info[name_d] = office_d
                    # defen_info.append(de_info)
            # defen_info = json.dumps(defen_info, ensure_ascii=False)
    return pl_info,de_info


def get_infomation(text):
    global lawyer_list2
    pl_dic = get_defendant(text)[0]
    de_dic = get_defendant(text)[1]
    infom = ""
    for k,v in pl_dic.iteritems():
        infom = k + " " + v
        lawyer_list2.append(infom)
    for k,v in de_dic.iteritems():
        infom = k + " " + v
        lawyer_list2.append(infom)


f1 = file("total_list2.pkl","rb")
a1 = pickle.load(f1)

conn = pymysql.connect(host="192.168.12.34",user="raolu",passwd="123456",db="laws_doc2",charset="utf8")
cur = conn.cursor()
# aa = cur.execute("select id,lawyer,office from lawyer")
aa = cur.execute("select id,uuid,party_info from judgment2")
a = cur.fetchall()
total_list = []

# 把lawyer表的id，律师，律所存下来 step2
# total_list2 = []
# for i in a:
#     list_s = []
#     id_l = i[0]
#     lawyer_l = i[1]
#     office_l = i[2]
#     list_s = [id_l,lawyer_l,office_l]
#     total_list2.append(list_s)
#
# output = open("total_list2.pkl","wb")
# pickle.dump(total_list2,output)
# output.close()
# print len(total_list2)
for i in a:
    # get_infomation(i[2]) # 第一次从judgment里面把数据down下来，用于lawyer这个表的形成（使用lawyer.py）step 1

    try:
        info = get_defendant(i[2])  # step 3
        plainiff_info = info[0]  # 原告律师信息
        defendant_info = info[1]  # 被告律师信息
        id_list_plain = []
        id_list_defen = []

        for k,v in plainiff_info.iteritems():
            for j in a1:
                if k == j[1] and v == j[2]:
                    law_id_p = j[0]
                    # print law_id_p
                    id_list_plain.append(law_id_p)
                    break
        for k,v in defendant_info.iteritems():
            for j in a1:
                if k == j[1] and v == j[2]:
                    law_id_d = j[0]
                    id_list_defen.append(law_id_d)
                    break

        if len(plainiff_info) == len(id_list_plain) and plainiff_info:
            plainiff_info = json.dumps(plainiff_info, ensure_ascii=False)
            id_list_plain = json.dumps(id_list_plain, ensure_ascii=False)
            # print "原告信息：", plainiff_info, id_list_plain
        else:
            plainiff_info = u""
            id_list_plain = u""
            # print i[0]
        if len(defendant_info) == len(id_list_defen) and defendant_info:
            defendant_info = json.dumps(defendant_info, ensure_ascii=False)
            id_list_defen = json.dumps(id_list_defen, ensure_ascii=False)
            # print "被告信息：", defendant_info, id_list_defen
        else:
            defendant_info = u""
            id_list_defen = u""
            # print i[0]
        # if plainiff_info:
        #     plainiff_info = json.dumps(plainiff_info, ensure_ascii=False)
        # else:
        #     plainiff_info = u""
        # if defendant_info:
        #     defendant_info = json.dumps(defendant_info, ensure_ascii=False)
        # else:
        #     defendant_info = u""
        if plainiff_info or defendant_info:
            values = [i[0],i[1],plainiff_info,id_list_plain,defendant_info,id_list_defen]
            sql = "insert into tmp_lawyers(id,uuid,plaintiff_info,plaintiff_id,defendant_info,defendant_id) values(%s,%s,%s,%s,%s,%s)"
            cur.execute(sql,values)
            conn.commit()

    except Exception:
        # print i[2]
        pass

# lawyer_list2 = list(set(lawyer_list2))
# output = open("lawyer_list2.pkl","wb")
# pickle.dump(lawyer_list2,output)
# output.close()
# print len(lawyer_list2)





# output = open("lawyer_info.pkl","wb")
# pickle.dump(t_list,output)
# output.close()

