# -*- coding:utf-8 -*-

import pymysql
import re
import pickle

list_law = []


def get_lawyer(text):
    global list_law
    text_split = text.split("||")
    if len(text_split) > 1 and len(text_split) % 2 == 0:
        for i in range(len(text_split)):
            if i % 2 == 0:
                tt = text_split[i] + " " + text_split[i + 1]
                list_law.append(tt)
                # if len(text_split)%2 == 1 and len(text_split) > 1:
                #     print text


def modify_info(text):
    dic = [u"×", u"x", u"X", u"□"]



# f1 = file("lawyer_info2.pkl","rb")
# f2 = file("lawyer_info2_2.pkl","rb")
# f3 = file("lawyer_info2_3.pkl","rb")
# f4 = file("lawyer_info2_4.pkl","rb")
#
#
# a1 = pickle.load(f1)
# a2 = pickle.load(f2)
# a3 = pickle.load(f3)
# a4 = pickle.load(f4)
#
#
# list_totall = a1 + a2 + a3 + a4
#
# list_new = list(set(list_totall))
# print len(list_new)


# 预处理
def as_text(text):
    text = text.replace(u"(",u"（")
    text = text.replace(u")",u"）")
    text = text.replace(u"〉",u"）")
    text = text.replace(u",",u"，")
    # text = text.replace(u".",u"。")

    return text

# 清洗律师
def clean_name(name):
    name = as_text(name)
    dic = [u"×", u"x", u"ｘ", u"Ｘ", u"Ⅹ", u"*", u"＊", u"X", u"a", u"□", u"中华人民共和国民法", u"执业经验", u"规定", u"å", u",", u"，",
           u"0", u"z",
           u"某"]
    for i in dic:
        if i in name:
            name = u""
            break
    name = name.replace(u"中华人民共和国", u"")
    pattern_re = re.compile(u"(?:（|[(]).*?(?=$)")
    name_search = re.search(pattern_re, name)
    if name_search:
        name = name.replace(name_search.group(0), "")
    if u"委托" in name:
        name = name.replace(u"诉讼", u"")
        pattern_na = re.compile(u"(?<=委托代理人).*?(?=$)")
        name_search = re.search(pattern_na, name)
        if name_search:
            name = name_search.group(0)
        else:
            name = u""
    if u"实习" in name or u"律师" in name:
        name = name.replace(u"﹤实习﹥", u"")
        name = name.replace(u"﹙实习﹚", u"")
        name = name.replace(u"实习", u"")
        name = name.replace(u"律师", u"")
        # print name
    if u"事务所" in name:
        name = u""
    if u"代理" in name:
        pattern_na3 = re.compile(u"(?<=代理人)(.*?)(?=$)")
        name_search3 = re.search(pattern_na3, name)
        if name_search3:
            name = name_search3.group(0)
        else:

            pattern_na4 = re.compile(u"(?<=权限).*?(?=$)")
            name_search4 = re.search(pattern_na4, name)
            if name_search4:
                name = name_search4.group(0)
            else:
                name = u""
    if len(name) > 1 and name[0] == u"均":
        name = name.replace(u"均为", u"")
    if len(name) > 1 and name[0] == u"是":
        name = name.replace(u"是", u"")
    if u"授权" in name:
        name = u""
    if u"身份" in name:
        name = name.replace(u"身份", u"")
        name = name.replace(u"的", u"")
    if u"和" in name and len(name) > 4:
        pattern_na5 = re.compile(u"(.*?)(?=和)")

        if u"额日" in name or u"孟和" in name or u"布和" in name or u"恩和" in name or u"木和" in name:
            pass
        else:
            name_search5 = re.search(pattern_na5, name)
            if name_search5:
                name = name_search5.group(0)

    if u"包括" in name:
        name = name.replace(u"包括", u"")
    if u"（" in name or u"）" in name:
        name = name.replace(u"（", u"")
        name = name.replace(u"）", u"")
    if u"；" in name:
        name = name.replace(u"；", u"")
    if len(name) < 2:
        name = u""
    return name

# 清洗律所
def clean_office(office):
    office = as_text(office)
    dic = [u"×", u"x", u"ｘ", u"Ｘ", u"Ⅹ", u"*", u"＊", u"X", u"a", u"□", u"中华人民共和国民法", u"执业经验", u"规定", u"å", u",", u"，",
           u"0", u"z",
           u"某"]
    province = [u"湖北", u"湖南", u"广东", u"广西", u"河南", u"河北", u"山东", u"山西", u"江苏", u"浙江", u"江西", u"黑龙江", u"新疆", u"云南",
                u"贵州", u"福建", u"吉林", u"安徽", u"四川", u"西藏", u"宁夏", u"辽宁", u"青海", u"甘肃", u"陕西", u"内蒙古", u"台湾", u"北京",
                u"上海",
                u"天津", u"重庆", u"香港", u"高碑店市", u"徐州市", u"临安市", u"抚顺市", u"咸阳市", u"邳州市"]
    for i in dic:
        if i in office:
            office = u""
            break
    office = office.replace(u"中华人民共和国", u"")

    # office_search = re.compile(ur"((?:湖南|贵州)[\u4e00-\u9fa5]{1,20}.*?(?:|事务所|事务部))")
    # pattern_re = re.compile(u"(?:（|[(]).*?(?=$)")
    pattern_of = re.compile(u"(.*?)(?:事务所|援助中心|服务所)")
    pattern_of2 = re.compile(u"(?<=指派).*?(?=$)")
    pattern_of3 = re.compile(u"(.*?)(?:实习）|实习律师）)")
    office = office.replace(u"均", u"")
    if u">" in office or u"事务所律师" in office or u"中心律师" in office:
        office_s = re.search(pattern_of, office)
        if office_s:
            office = office_s.group(0)
            # print "modify:",office
    if u"实习" in office:
        # print office
        office_s3 = re.search(pattern_of3, office)
        if office_s3:
            office = office.replace(office_s3.group(0), u"")
            # print "modify: ",office
        else:
            # print office
            pattern_of4 = re.compile(u"(.*?)(?=实习人员|实习律师（)")
            office_s4 = re.search(pattern_of4, office)
            if office_s4:
                office = office_s4.group(0)
    if u"服务所（" in office or u"服务所法律工作者" in office:
        office_s5 = re.search(pattern_of, office)
        if office_s5:
            office = office_s5.group(0)

    if len(office) > 18:

        office_s2 = re.search(pattern_of2, office)
        if office_s2:
            office = office_s2.group(0)
            office = office.replace(u"的", u"")
            office = office.replace(u"律师（", u"")

    if (u"该" in office and len(office) < 10) or len(office) < 7:
        office = u""

    office = office.replace(u"分别是", u"")
    office = office.replace(u"分别为", u"")
    office = office.replace(u"分别", u"")
    office = office.replace(u"依次为", u"")
    office = office.replace(u"工作单位：", u"")
    office = office.replace(u"工作单位", u"")
    # print office
    if len(office) > 1 and office[0] == u"是":
        office = office.replace(u"是是", u"")
        office = office.replace(u"是", u"")

    if u"代理" in office:
        # print office
        pattern_of6 = re.compile(u"(?<=代理）).*?(?=$)")
        pattern_of8 = re.compile(u"(?<=（).*?(?=$)")
        pattern_of9 = re.compile(u"(?<=代理人为).*?(?=$)")
        pattern_of13 = re.compile(u"[^\n、；]{2,22}(?:事务所|事务部|援助中心|分所|服务所)")

        office_s7 = re.search(pattern_of6, office)
        if office_s7:
            office = office_s7.group(0)
        else:
            office_s8 = re.search(pattern_of8, office)
            if office_s8:
                office = office_s8.group(0)
            else:
                office_s9 = re.search(pattern_of9, office)
                if office_s9:
                    office = office_s9.group(0)
                else:
                    office_s13 = re.search(pattern_of13, office)
                    if office_s13:
                        office = office_s13.group(0)
                        for p in province:
                            pro_search = re.compile(ur"(?:" + p + ur").*?(?:事务所|事务部|援助中心|分所|服务所)")
                            pro_res = re.search(pro_search, office)
                            if pro_res:
                                office = pro_res.group(0)

    if u"：" in office or u"、" in office or u"：" in office:
        pattern_of5 = re.compile(u"[^\n、；：]{2,25}(?:事务所|事务部|援助中心|分所|服务所)")
        office_s6 = re.search(pattern_of5, office)
        if office_s6:
            office = office_s6.group(0)
            for p in province:
                pro_search = re.compile(ur"(?:" + p + ur").*?(?:事务所|事务部|援助中心|分所|服务所)")
                pro_res = re.search(pro_search, office)
                if pro_res:
                    office = pro_res.group(0)
        else:
            office = office.replace(u"、", u"")

    if len(office) > 1 and office[0] == u"为":
        office = office.replace(u"为", u"")
    if len(office) > 1 and office[0] == u"该":
        if u"事务部" in office:
            office = u""
        else:
            office = office.replace(u"（", u"")
            office = office.replace(u"该公司法律顾问", u"")
            office = office.replace(u"该中心法律顾问", u"")
            office = office.replace(u"该单位工作人员", u"")
            office = office.replace(u"该公司管理人", u"")
            office = office.replace(u"该公司员工、", u"")
            office = office.replace(u"该公司员工", u"")
            office = office.replace(u"该公司", u"")
            office = office.replace(u"该校", u"")
            office = office.replace(u"该", u"")

    if u"（" in office and u"）" not in office:
        if office[0] == u"（" and len(office) > 1 or u"分所" in office:
            office = office.replace(u"（", u"")

        else:
            pattern_of11 = re.compile(u"(?:（)(.*?)(?=$)")
            office_s11 = re.search(pattern_of11, office)
            pattern_of12 = re.compile(u"(.*?)(?=（原)")
            office_s12 = re.search(pattern_of12, office)
            if office_s12:
                office = office_s12.group(0)

            elif office_s11:
                if len(office_s11.group(1)) > 7:
                    office = office_s11.group(1)
                    office = office.replace(u"现更名为", u"")
                else:
                    office = u""

    if u"（" not in office and u"）" in office:
        pattern_of10 = re.compile(u"(?:）)[、]{0,1}(.*?)(?=$)")
        office_s10 = re.search(pattern_of10, office)
        if office_s10:
            if len(office_s10.group(1)) > 5:
                office = office_s10.group(1)
        else:
            office = u""
            # print office
    if len(office) == 7 and u"律师" in office:
        for p in province:
            if p in office:
                office = u""
                break

    if len(office) < 7 and len(office) > 0:
        office = u""

    return office

# 律所和律师名一起清洗
def clean_data(text):
    name = u""
    office = u""
    text = as_text(text)
    dic = [u"×", u"x", u"ｘ",u"Ｘ",u"Ⅹ", u"*", u"＊", u"X", u"a", u"□", u"中华人民共和国民法", u"执业经验", u"规定", u"å", u",", u"，", u"0", u"z",
           u"某"]
    province = [u"湖北", u"湖南", u"广东", u"广西", u"河南", u"河北", u"山东", u"山西", u"江苏", u"浙江", u"江西", u"黑龙江", u"新疆", u"云南",
                u"贵州", u"福建", u"吉林", u"安徽", u"四川", u"西藏", u"宁夏", u"辽宁", u"青海", u"甘肃", u"陕西", u"内蒙古", u"台湾", u"北京", u"上海",
                u"天津", u"重庆", u"香港",u"高碑店市",u"徐州市",u"临安市",u"抚顺市",u"咸阳市",u"邳州市"]
    for i in dic:
        if i in text:
            text = u""

    text = text.replace(u"谢文波（特别授权）",u"")
    text = text.replace(u"中华人民共和国",u"")

    if text:
        new_l = text.split(" ")
        # office_search = re.compile(ur"((?:湖南|贵州)[\u4e00-\u9fa5]{1,20}.*?(?:|事务所|事务部))")
        pattern_re = re.compile(u"(?:（|[(]).*?(?=$)")
        pattern_of = re.compile(u"(.*?)(?:事务所|援助中心|服务所)")
        pattern_of2 = re.compile(u"(?<=指派).*?(?=$)")
        pattern_of3 = re.compile(u"(.*?)(?:实习）|实习律师）)")
        name = new_l[0]
        office = new_l[1]
        office = office.replace(u"均",u"")

        name_search = re.search(pattern_re, name)
        if name_search:
            name = name.replace(name_search.group(0), "")
        if u"委托" in name:
            name = name.replace(u"诉讼",u"")
            pattern_na = re.compile(u"(?<=委托代理人).*?(?=$)")
            name_search = re.search(pattern_na,name)
            if name_search:
                name = name_search.group(0)
            else:
                name = u""
        if u"实习" in name or u"律师" in name:
            name = name.replace(u"﹤实习﹥",u"")
            name = name.replace(u"﹙实习﹚",u"")
            name = name.replace(u"实习",u"")
            name = name.replace(u"律师",u"")
            # print name
        if u"事务所" in name:
            name = u""
        if u"代理" in name:
            pattern_na3 = re.compile(u"(?<=代理人)(.*?)(?=$)")
            name_search3 = re.search(pattern_na3,name)
            if name_search3:
                name = name_search3.group(0)
            else:

                pattern_na4 = re.compile(u"(?<=权限).*?(?=$)")
                name_search4 = re.search(pattern_na4, name)
                if name_search4:
                    name = name_search4.group(0)
                else:
                    name = u""
        if len(name)>1 and name[0] == u"均":
            name = name.replace(u"均为",u"")
        if len(name)>1 and name[0] == u"是":
            name = name.replace(u"是",u"")
        if u"授权" in name:
            name = u""
        if u"身份" in name:
            name = name.replace(u"身份",u"")
            name = name.replace(u"的", u"")
        if u"和" in name and len(name) > 4:
            pattern_na5 = re.compile(u"(.*?)(?=和)")

            if u"额日" in name or u"孟和" in name or u"布和" in name or u"恩和" in name or u"木和" in name:
                pass
            else:
                name_search5 = re.search(pattern_na5,name)
                if name_search5:
                    name = name_search5.group(0)

        if u"包括" in name:
            name = name.replace(u"包括",u"")
        if u"（" in name or u"）" in name:
            name = name.replace(u"（",u"")
            name = name.replace(u"）",u"")
        if u"；"in name:
            name = name.replace(u"；",u"")
        if len(name) < 2:
            name = u""


                # pattern_na2 = re.compile(u"(.*?)[的]{0,1}(?=共同|特别)")
                # name_search2 = re.search(pattern_na2,name)
                # if name_search2:
                #     name = name_search2.group(1)
                # else:
                #     print name

        if u">" in office or u"事务所律师" in office or u"中心律师" in office:
            office_s = re.search(pattern_of,office)
            if office_s:
                office = office_s.group(0)
                # print "modify:",office
        if u"实习" in office:
            # print office
            office_s3 = re.search(pattern_of3, office)
            if office_s3:
                office = office.replace(office_s3.group(0),u"")
                # print "modify: ",office
            else:
                # print office
                pattern_of4 = re.compile(u"(.*?)(?=实习人员|实习律师（)")
                office_s4 = re.search(pattern_of4,office)
                if office_s4:
                    office = office_s4.group(0)
        if u"服务所（" in office or u"服务所法律工作者" in office:
            office_s5 = re.search(pattern_of,office)
            if office_s5:
                office = office_s5.group(0)

        if len(office) > 18:

            office_s2 = re.search(pattern_of2, office)
            if office_s2:
                office = office_s2.group(0)
                office = office.replace(u"的",u"")
                office = office.replace(u"律师（",u"")

        if (u"该" in office  and len(office) < 10) or len(office) < 7:
            office = u""

        office = office.replace(u"分别是",u"")
        office = office.replace(u"分别为",u"")
        office = office.replace(u"分别",u"")
        office = office.replace(u"依次为", u"")
        office = office.replace(u"工作单位：", u"")
        office = office.replace(u"工作单位", u"")
        # print office
        if len(office) > 1 and office[0] == u"是":
            office = office.replace(u"是是", u"")
            office = office.replace(u"是", u"")

        if u"代理" in office:
            # print office
            pattern_of6 = re.compile(u"(?<=代理）).*?(?=$)")
            pattern_of8 = re.compile(u"(?<=（).*?(?=$)")
            pattern_of9 = re.compile(u"(?<=代理人为).*?(?=$)")
            pattern_of13 = re.compile(u"[^\n、；]{2,22}(?:事务所|事务部|援助中心|分所|服务所)")

            office_s7 = re.search(pattern_of6,office)
            if office_s7:
                office = office_s7.group(0)
            else:
                office_s8 = re.search(pattern_of8,office)
                if office_s8:
                    office = office_s8.group(0)
                else:
                    office_s9 = re.search(pattern_of9,office)
                    if office_s9:
                        office = office_s9.group(0)
                    else:
                        office_s13 = re.search(pattern_of13,office)
                        if office_s13:
                            office = office_s13.group(0)
                            for p in province:
                                pro_search = re.compile(ur"(?:" + p + ur").*?(?:事务所|事务部|援助中心|分所|服务所)")
                                pro_res = re.search(pro_search, office)
                                if pro_res:
                                    office = pro_res.group(0)

        if u"：" in office or u"、" in office or u"：" in office:
            pattern_of5 = re.compile(u"[^\n、；：]{2,25}(?:事务所|事务部|援助中心|分所|服务所)")
            office_s6 = re.search(pattern_of5,office)
            if office_s6:
                office = office_s6.group(0)
                for p in province:
                    pro_search = re.compile(ur"(?:" + p + ur").*?(?:事务所|事务部|援助中心|分所|服务所)")
                    pro_res = re.search(pro_search, office)
                    if pro_res:
                        office = pro_res.group(0)
            else:
                office = office.replace(u"、",u"")

        if len(office) > 1 and office[0] == u"为":
            office = office.replace(u"为",u"")
        if len(office) > 1 and office[0] == u"该":
            if u"事务部" in office:
                office = u""
            else:
                office = office.replace(u"（",u"")
                office = office.replace(u"该公司法律顾问",u"")
                office = office.replace(u"该中心法律顾问",u"")
                office = office.replace(u"该单位工作人员",u"")
                office = office.replace(u"该公司管理人",u"")
                office = office.replace(u"该公司员工、",u"")
                office = office.replace(u"该公司员工",u"")
                office = office.replace(u"该公司",u"")
                office = office.replace(u"该校",u"")
                office = office.replace(u"该",u"")

        if u"（" in office and u"）" not in office:
            if office[0] == u"（" and len(office) > 1 or u"分所" in office:
                office = office.replace(u"（",u"")

            else:
                pattern_of11 = re.compile(u"(?:（)(.*?)(?=$)")
                office_s11 = re.search(pattern_of11, office)
                pattern_of12 = re.compile(u"(.*?)(?=（原)")
                office_s12 = re.search(pattern_of12, office)
                if office_s12:
                    office = office_s12.group(0)

                elif office_s11:
                    if len(office_s11.group(1)) > 7:
                        office = office_s11.group(1)
                        office = office.replace(u"现更名为",u"")
                    else:
                        office = u""

        if u"（" not in office and u"）" in office:
            pattern_of10 = re.compile(u"(?:）)[、]{0,1}(.*?)(?=$)")
            office_s10 = re.search(pattern_of10,office)
            if office_s10:
                if len(office_s10.group(1)) > 5:
                    office = office_s10.group(1)
            else:
                office = u""
                # print office
        if len(office) == 7 and u"律师" in office:
            for p in province:
                if p in office:
                    office = u""
                    break

        if len(office) < 7 and len(office) > 0:
            office = u""
        #
        # if len(office) > 20:
        #     print office
    return name,office



# f1 = file("lawyer_list2.pkl", "rb")
# a1 = pickle.load(f1)
#
#
# conn = pymysql.connect(host="192.168.12.34", user="raolu", passwd="123456", db="laws_doc2", charset="utf8")
# cur = conn.cursor()
#
#
# for i in a1:
#     try:
#         name = clean_data(i)[0]
#         office = clean_data(i)[1]
#         if name and office:
#             values = [name,office]
#             sql = "insert into lawyer(lawyer,office) values(%s,%s)"
#             cur.execute(sql,values)
#             conn.commit()
#     except Exception:
#         print "wrong"
