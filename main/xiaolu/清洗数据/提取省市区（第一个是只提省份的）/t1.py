# -*- coding:utf-8 -*-

import pymysql
import re
import xlrd
import json
import pandas


# class AttrDict(dict):
#     """Dict that can get attribute by dot"""
#     def __init__(self, *args, **kwargs):
#         super(AttrDict, self).__init__(*args, **kwargs)
#         self.__dict__ = self


def as_text(v):
    if v is None:
        return None
    elif isinstance(v, unicode):
        return v
    elif isinstance(v, str):
        return v.decode('utf-8', errors='ignore')
    else:
        raise ValueError('Invalid type %r' % type(v))

aaa = 0
def text_replace(content_text):
    """ 文本规范化"""
    # global aaa
    # content_text = content_text
    # content_text = content_text.replace(' ','')
    # content_text = content_text.replace("　","")
    # content_text = content_text.replace("	","")
    # content_text = content_text.strip()
    # content_text = content_text.replace('<<', '《')
    # content_text = content_text.replace('>>', '》')
    # content_text = content_text.replace('〈〈', '《')
    # content_text = content_text.replace('〉〉', '》')
    # content_text = content_text.replace(':','：')

    content_text = content_text.replace(u',', u'，')
    content_text = content_text.replace(u'.', u'。')


    return content_text


def read_location_xcel(path):
    data = xlrd.open_workbook(path)
    table = data.sheet_by_name("sheet")
    result_list = []
    for i in range(0,table.nrows):
        row_content = table.row_values(i,0,table.ncols)
        result_list.append(row_content)
    return result_list

city_list, dis_list, prov_list = [],[],[]
location_list = read_location_xcel("location_1.xlsx")
for i in location_list:
    prov_list.append(i[0])
    city_list.append(i[1])
    dis_list.append(i[2])


def get_public_defendant_party(info):
    law_place = ""
    law_people = ""
    try:
        party = as_text(info)
        # party = text_replace(party1)
    except ValueError:
        party = ""
    if party:
        # print party
        party_pattern = re.compile(ur"(?:辩护人).+?(?:事务所)")
        party_search = re.compile(ur"[^\n，]{0,50}(?:事务所)")
        lawyer_search = re.compile(ur"(?<=辩护人)[\u4e00-\u9fa5].+?(?=，|。)")
        lawyer_search2 = re.compile(ur"(?<=刑事附带民事诉讼(委托|被告)代理人).+?(?:$)")
        lawyer_search3 = re.compile(ur"[\u4e00-\u9fa5].+?(?=、)")
        # party_result = re.search(party_pattern, party)
        party_result = re.search(party_pattern,party)
        if party_result:
            # print "律所信息：",i
            sen = party_result.group(0)
            # print sen,"\n"
            law_p = re.search(party_search,sen)
            lawyer = re.search(lawyer_search,sen)
            if law_p:
                # print "律所：",law_p.group(0)
                law_place = law_p.group(0)
                law_place = law_place.replace("系".decode("utf-8"),"")
            if lawyer:
                law_people = lawyer.group(0)
                law_people2 = re.search(lawyer_search2, law_people)
                if law_people2:
                    law_people = law_people2.group(0)
                law_people3 = re.search(lawyer_search3,law_people)
                if law_people3:
                    law_people = law_people3.group(0)
                # law_people = law_people.replace("、".decode("utf-8"), "||")
                law_people = law_people.replace("暨".decode("utf-8"), "")
                law_people = law_people.replace("及".decode("utf-8"), "")
                law_people = law_people.replace("兼".decode("utf-8"), "")
                law_people = law_people.replace("附带民事诉讼代理人".decode("utf-8"), "")
                law_people = law_people.replace("附带民事诉讼委托代理人".decode("utf-8"), "")
                law_people = law_people.replace("附带民事诉委托理人".decode("utf-8"), "")
                law_people = law_people.replace("诉讼代理人".decode("utf-8"), "")
                law_people = law_people.replace("委托代理人".decode("utf-8"), "")

    # if law_people:
    #     print "律师：",law_people
    # if law_place:
    #     print "律所：", law_place,"\n"
    # if law_people == u"付金彪":
    #     print law_people,law_place,sen

    return law_place,law_people


def get_defendant(list_):
    pattern = re.compile(ur"((?:被告).+?(?:事务所))")
    p_search = re.compile(ur"((?<=代理人).+?(?:事务所))")
    lawyer_search = re.compile(ur"(.+?(?=，|、))")
    lawyer_search2 = re.compile(ur"((?<=代理人)[\u4e00-\u9fa5]{1,7}?(?=，))")
    office_search = re.compile(ur"((?<=，).+?(?:事务所))")
    pattern_search = re.search(pattern,list_)
    if pattern_search:
        p_info = pattern_search.groups(0)[0]
        p2 = re.search(p_search,p_info)
        if p2:
            # print p2.groups(0)[0]
            lawyer = re.search(lawyer_search,p2.groups(0)[0])
            office = re.search(office_search,p2.groups(0)[0])
            lawyer_1 = lawyer.groups(0)[0]
            office_1 = office.groups(0)[0]
            if len(office_1)>15:
                print "p_info:",p_info
                print "office:",office_1
                print "list:",list_
                print "lawyer:",lawyer_1
                lawyer2 = re.search(lawyer_search2,office_1)
                lawyer_2 = lawyer2.groups(0)[0]
                office2 = re.search(office_search,office_1)
                office_2 = office2.groups(0)[0]
                print lawyer_2,office_2
                print "\n"
            dic1 = [u"：",u"特别授权",u"（",u"）"]
            for d in dic1:
                lawyer_1 = lawyer_1.replace(d, u"")
            if len(lawyer_1) > 10:
                lawyer_1 = u""
            # print lawyer_1

        # if office:
        #     print office.groups(0)[0]




area={u'威宁':u'贵州省',u'六盘水':u'贵州省',u'凤岗县':u'贵州省',
      u'大连':u'辽宁省',u'沈阳':u'辽宁省',u'锦州':u'辽宁省',u'丹东':u'辽宁省',
      u'烟台':u'山东省',u'临沂':u'山东省',u'威海':u'山东省',u'日照':u'山东省',u'菏泽':u'山东省',u'泰安':u'山东省',u'垦利区':u'山东省',
      u'红石林区':u'湖南省',u'大通湖':u'湖南省',
      u'福州':u'福建省',
      u'泰州':u'江苏省',u'扬州':u'江苏省',u'盐城':u'江苏省',u'南通':u'江苏省',u'徐州':u'江苏省',u'镇江':u'江苏省',u'苏州':u'江苏省',u'淮安':u'江苏省',u'南京':u'江苏省',
      u'积石山保安族东乡族撒拉族':u'甘肃省',u'兰州':u'甘肃省',u'庆阳林区':u'甘肃省',
      u'白石山林区':u'吉林省',u'图们':u'吉林省',u'长春':u'吉林省',u'和龙林区':u'吉林省',
      u'敦化林区':u'吉林省',u'汪清林区':u'吉林省',u'抚松林区':u'吉林省',u'珲春林区':u'吉林省',
      u'杭州':u'浙江省',u'洞头县':u'浙江省',
      u'南昌':u'江西省',u'新建县':u'江西省',
      u'珠海':u'广东省',u'梅州市':u'广东省' ,u'从化市':u'广东省',u'湛江':u'广东省',u'增城市':u'广东省',
      u'九三农垦':u'黑龙江省',u'建三江农垦':u'黑龙江省',u'哈尔滨':u'黑龙江省',u'牡丹江':u'黑龙江省',u'铁力林区':u'黑龙江省',
      u'迎春林区':u'黑龙江省',u'通北林区':u'黑龙江省',u'绥化农垦':u'黑龙江省',u'方正林区':u'黑龙江省',u'双丰林区':u'黑龙江省',
      u'苇河林区':u'黑龙江省',u'齐齐哈尔':u'黑龙江省',u'红兴隆农垦':u'黑龙江省',u'兴隆林区':u'黑龙江省',u'东方红林区':u'黑龙江省',
      u'绥棱林区':u'黑龙江省',u'大庆':u'黑龙江省',u'东京城林区':u'黑龙江省',u'北安农垦':u'黑龙江省',u'大兴安岭':u'黑龙江省',
      u'穆棱林区':u'黑龙江省',u'佳木斯':u'黑龙江省',u'林口林区':u'黑龙江省',
      u'金平苗族瑶族傣族':u'云南省',u'玉溪':u'云南省',u'元江哈尼族':u'云南省',u'曲靖':u'云南省',
      u'潼南县':u'重庆市',
      u'荆州市':u'湖北省',u'武汉':u'湖北省',
      u'郑州':u'河南省',u'洛阳':u'河南省',u'三门峡':u'河南省',
      u'安康':u'陕西省',u'西安':u'陕西省',u'歧山县':u'陕西省',
      u'石家庄':u'河北省',u'秦皇岛':u'河北省',u'邢台':u'河北省',u'保定':u'河北省',u'黄骅':u'河北省',u'河间':u'河北省',u'任丘':u'河北省',u'泊头':u'河北省',u'沙河':u'河北省',u'迁安':u'河北省',u'遵化':u'河北省',
      u'乃东区':u'西藏自治区',
      u'乌鲁木齐':u'新疆维吾尔自治区',u'新疆':u'新疆维吾尔自治区',
      u'武鸣县':u'广西壮族自治区',u'临桂县':u'广西壮族自治区',
      u'通辽':u'内蒙古自治区',u'阿拉善左旗':u'内蒙古自治区',u'察哈尔右翼前旗':u'内蒙古自治区',u'奈曼旗':u'内蒙古自治区',
      u'准格尔旗':u'内蒙古自治区',u'科尔沁右翼中旗':u'内蒙古自治区',u'乌拉特中旗':u'内蒙古自治区',
      u'扎赉特旗':u'内蒙古自治区',u'阿荣旗':u'内蒙古自治区',u'额济纳旗':u'内蒙古自治区',u'杭锦旗':u'内蒙古自治区',
      u'克什克腾旗':u'内蒙古自治区',u'四子王旗':u'内蒙古自治区',u'达拉特旗':u'内蒙古自治区',u'桃山林区':u'黑龙江省',u'宝泉岭':u'黑龙江省',u'双鸭山林区':u'黑龙江省',u'桦南林区':u'黑龙江省',u'图强林区':u'黑龙江省',
      u'亚布力林区':u'黑龙江省',u'阿木尔林区':u'黑龙江省',u'十八站林区':u'黑龙江省',u'沾河林区':u'黑龙江省',u'清河林区':u'黑龙江省',
      u'绥阳林区':u'黑龙江省',u'大海林林区':u'黑龙江省',u'柴河林区':u'黑龙江省',u'鹤北林区':u'黑龙江省',u'海林林区':u'黑龙江省',
      u'常州市':u'江苏省',u'高陵县':u'陕西省',u'渭南市华州区':u'陕西省',u'赣州':u'江西省',
      u'庐山':u'江西省',u'武威':u'甘肃省',u'卓尼林区':u'甘肃省',u'迭部林区':u'甘肃省',u'舟曲林区':u'甘肃省',
      u'济南':u'山东省',u'德州':u'山东省',u'滨州':u'山东省',u'青岛':u'山东省',u'济宁':u'山东省',
      u'陕州区':u'河南省',u'冷湖矿区':u'青海省',u'茫崖矿区':u'青海省',u'西宁':u'青海省',u'大柴旦矿区':u'青海省',
      u'宜昌':u'湖北省',u'葛洲坝':u'湖北省',u'襄阳':u'湖北省',u'沙洋':u'湖北省',
      u'屈原管理区':u'湖南省',u'长沙':u'湖南省',u'洪江':u'湖南省',u'ＸＸ瑶族自治县':u'湖南省',u'衡阳':u'湖南省',u'怀化':u'湖南省',
      u'高要市':u'广东省',u'广州':u'广东省',u'通化':u'吉林省',
      u'靖西县':u'广西壮族自治区',u'柳州':u'广西壮族自治区',u'南宁':u'广西壮族自治区',
      u'荣昌县':u'重庆市',u'彭山县':u'四川省',u'马尔康市':u'四川省',u'西昌':u'四川省',u'平坝县':u'贵州省',u'贵阳':u'贵州省',
      u'腾冲县':u'云南省',u'镇沅彝族哈尼族拉祜族':u'云南省',u'孟连傣族拉祜族佤族':u'云南省',u'双江拉祜族佤族布朗族傣族':u'云南省',u'昆明':u'云南省',u'开远':u'云南省',
      u'香格里拉':u'云南省',u'土默特':u'内蒙古自治区',u'阿拉善':u'内蒙古自治区',u'旗':u'内蒙古自治区',u'包头':u'内蒙古自治区',u'呼和浩特':u'内蒙古自治区',
      u'库尔勒':u'新疆维吾尔自治区',u'哈密':u'新疆维吾尔自治区',u'北屯市':u'新疆维吾尔自治区',u'塔什库尔干塔吉克自治县':u'新疆维吾尔自治区',
      u'银川':u'宁夏回族自治区',u'吴忠市红寺堡开发区':u'宁夏回族自治区',
      u'宁河县':u'河北省',u'抚宁县':u'河北省',u'清苑县':u'河北省',u'张家口':u'河北省',u'廊坊市':u'河北省',
      u'太原':u'山西省',
      u'吉林':u'吉林省',
      u'大同':u'山西省',
      u'鹤立林区':u'黑龙江省', u'山河屯林区':u'黑龙江省', u'八面通林区': u'黑龙江省',u'朗乡林区':u'黑龙江省',
      u'海拉尔':u'内蒙古自治区',
      u'营口市':u'辽宁省', u'辽河人民法院': u'辽宁省',
      u'喀喇沁':u'内蒙古自治区',u'前郭尔罗斯':u'内蒙古自治区',
      u'白城铁路运输法院':u'吉林省',u'白河林区':u'吉林省',u'临江林区':u'吉林省',u'江源林区':u'吉林省',
      u'无锡':u'江苏省',u'常州':u'江苏省',
      u'甘肃':u'甘肃省',
      u'潍坊':u'山东省',
      u'临汾':u'山西省',
      u'堆龙德庆区':u'西藏自治区',
      u'徐水县':u'河北省',u'唐山':u'河北省',
      u'上海':u'上海市',u'北京':u'北京市',u'天津':u'天津市',u'重庆':u'重庆市',
      u'合肥':u'安徽省',u'九华山':u'安徽省',u'铜陵市':u'安徽省',u'六安':u'安徽省',u'芜湖':u'安徽省',
      u'成都':u'四川省',u'绵阳':u'四川省',
      }


def get_public_court_location(list):
    global area
    court = as_text(list)
    city = ""
    province = ""
    district = ""
    extra_t = [u"红旗区", u"社旗县"]
    if court:
        location_pattern = re.compile(u'(?P<province>[\u4e00-\u9fa5]{1,12}?(?:省|自治区)){0,1}'
                                      u'(?P<city>[\u4e00-\u9fa5]{2,12}?(?:市|州)){0,1}'
                                      u'(?P<district>[\u4e00-\u9fa5]{1,12}?(?:市|区|县|自治县)){0,1}')
        location_result = re.search(location_pattern, court)
        province = location_result.group("province")

        city = location_result.group("city")
        district = location_result.group("district")
        cate = [u"最高", u"高级", u"中级"]
        court_m = [u"天津海事法院", u"宁波海事法院", u"厦门海事法院", u"新疆维吾尔自治区高级人民法院伊犁哈萨克自治州分院"]
        high_city = ["北京市".decode("utf-8"), "上海市".decode("utf-8"), "天津市".decode("utf-8"), "重庆市".decode("utf-8")]
        a = ''

        if city == None and district != None:
            # 若市为空,但区并不为空,需要判断市是否为县级市
            if district in city_list:
                # 如果district是在市的列表中,且city为空,便将dis转为city
                city = district
                district = ''
            else:
                # 否则,判断一下市和区是否反了,若反了,则纠正
                if district in city_list and city in dis_list:
                    temp = district
                    district = city
                    city = temp
                # 如果以上两种情况都不是，就根据district补全city
                for item in location_list:
                    if item[2] == district:
                        city = item[1]

        if province == None and (district != None or city != None):
            # 若省为空,且市和区都非空,则根据市或区来查找省
            # if city != None and district != None:
            #     for item in location_list:
            #         if item[1] == city and item[2] == district:
            #             province = item[0]

            if city != None:
                for item in location_list:
                    if item[1] == city:
                        province = item[0]
                    elif item[2] == city:
                        province = item[0]

            elif district != None:
                for item in location_list:
                    if item[2] == district:
                        province = item[0]
                    elif item[1] == district:
                        province = item[0]

        if city != None and district == None and city[-1] == u"市":
            # 若市级为非空,但是区为空,且市级的最后一位为"市",需判断市级是否为县级市
            for item in dis_list:
                # 若为县级市,需要将城市降级
                if city == item:
                    district = city
                    city = ''

        if (province == None and city == None) and district != None:
            # 若省为空,且市也为空,则根据区县来查找省 市
            for item in location_list:
                if item[2] == district:
                    province, city = item[0], item[1]
        for i in extra_t:
            if i in court:
                district = i

    for c in cate:
        if c in court:
            a = c
            break
        else:
            a = u"基层"
    if court in court_m:
        a = u"中级"

    if city in high_city:
        province = city

    if not province:
        for k,v in area.iteritems():
            if k in court:
                province = v
    # if not province or not city or not district:
        # print "wrong:", court
    # else:
    # print a,province, city, district,court

    return a, province, city, district

def update_info(doc):
    # doc = doc.replace(u"均是",u"")
    # doc = doc.replace(u"均为",u"")
    # doc = doc.replace(u"（特别授权）",u"")
    dic3 = [
        u"（特别授权）",u"附带民事诉讼被告人代理人",u"附带民事诉讼的",u"附带",u"民事代理人",u"诉讼代表理人",u"代理人",u"委托",u"民事",\
        u"：",u"（杭州市余杭区法律援助中心指派）",u"刑事",u"许燕辩护人",u"张声宏辩护人"
    ]


    dic1 = [u"辩护人及附带民事诉讼委托诉讼代理人王禹祈",u"辩护人暨附带民事诉讼代理人闻静会",u"辩护人暨附带民事诉讼代理人高红莲袁义",u"辩护人、诉讼代理人",u"辩护人及附带民事诉讼委托代理人张哲峰",\
           u"辩护人兼附带民事诉讼代理人张百顺",u"辩护人暨附带民事诉讼代理人",u"辩护人暨诉讼代理人",\
           u"辩护人及诉讼代理人",u"辩护人王俊友暨附带民事诉讼代理人",u"中华人民共和国",\
           u"辩护人及民事诉讼代理人杨某某、",u"辩护人暨附带民事诉讼委托代理人杨丽娟、姚杰敏",u"浙江省义乌市法律援助中心指派的",u"义乌市法律援助中心指派的",u"浙江省义乌市法律援助中心指定的"]
    # dic2 = [u"榆林市榆阳区法律援助中心指派的",u"陈某某、上海陈某某律师事务所",u"榆林市榆阳区法律援助中心指派",u"榆林市法律援助中心指派的",u"辩护人王加庆",u"辩护人彭茂红",u"辩护人金某、程某",\
    #         u"辩护人生东洋",u"辩护人陈建方、吕梦维",u"辩护人李剑锋、男、",u"辩护人",u"杨德永、杨德伟",u"高晓萍。",u"雷某某、高某某",u"白某、男、",u"浙ＸＸ浙律师事务所",u"杨建恒。",\
    #         u"：高扬善、",u"陈忠圆",u"周某某共和某某律师事务所",u"张某某",u"张永峰。",u"杨尘、张朋",u"赖卫东、吴文清（实习律师）",u"吉布哈、",u"：",u"张志芳",u"李术荣",\
    #         u"许平、王显军",u"黄华超",u"虞某某",u"景某某"u"颜福民",u"杨文胜",u"白伟、",u"冯铁柱",u"杨成宝",u"姜来金",u"杨明峰",u"杨光明。",u"龚丽萍",u"杨",u"黄俊君、",u"上海市某某法律援助中心指派的",\
    #         u"律师（",u"律师的",u"",u"（",u"分别是"]  #还有以均开头的，二人均为，□，＊，等等
    dic4 = [u"□",u"＊",u"x",u"X",u"×"]
    pro_search = re.compile(ur"(?<=指派).+?(?:事务所)")
    pro_res = re.search(pro_search,doc)
    if pro_res:
        doc = pro_res.group(0)
    province = [u"湖北",u"湖南",u"广东",u"广西",u"河南",u"河北",u"山东",u"山西",u"江苏",u"浙江",u"江西",u"黑龙江",u"新疆",u"云南",u"贵州", \
                u"福建",u"吉林",u"安徽",u"四川",u"西藏",u"宁夏",u"辽宁",u"青海",u"甘肃",u"陕西",u"内蒙古",u"台湾",u"北京",u"上海",u"天津",u"重庆",u"香港"]
    for p in province:
        pro_search = re.compile(ur"(?:"+p+ur").+?(?:事务所)")
        pro_res = re.search(pro_search,doc)
        if pro_res:
            doc = pro_res.group(0)
        # else:
        #     print doc
    for i in dic3:
        doc = doc.replace(i,u"")
    for p in dic4:
        if p in doc:
            doc = u""
    return doc

data1 = xlrd.open_workbook("tb_doc.xlsx")
table = data1.sheet_by_name("tb_doc")

result_list = []
court_list = [table.cell(i,ord('H')-ord('A')).value for i in range(1,1001)]  #获取法院信息
law_list = [table.cell(i,ord('M')-ord('A')).value for i in range(1,1001)] #获取律所信息
c_idea_list = [table.cell(i,ord('U')-ord('A')).value for i in range(1,1001)]
# inform_list = [table.cell(i,ord('M')-ord('A')).value for i in range(1,1001)]  #获取罪犯个人信息
# print "\n".join(inform_list) □

# 从数据库提取
conn = pymysql.connect(host="192.168.12.35",user="raolu",passwd="123456",db="civil",charset="utf8")
cur = conn.cursor()
# aa = cur.execute("select id,party_info from judgment2 where id > 26825")
aa = cur.execute("select id,uuid,court from judgment where  id > 11295127 limit 100000")
a = cur.fetchall()
# for i in a:
#     pro = i[1]
#     pro_new = u"重庆市"
#     sql = "update tmp_raolu set province = '%s' where province = '%s' and id ='%s'" % (pro_new, pro,i[0])
#     cur.execute(sql)
#     conn.commit()
ri = 0
count = 0
for i in a:
    count += 1
    try:
        uuid = i[1]
        cate = get_public_court_location(i[2])[0]
        pro = get_public_court_location(i[2])[1]
        city = get_public_court_location(i[2])[2]
        dis = get_public_court_location(i[2])[3]
        # if pro != i[2]:
        #     print i[1],pro,dis,city,i[2]

        # info = as_text(i[2])
        # get_defendant(info)
        # print i[2]

        # lawyer = update_info(lawyer)
        # office = update_info(office)

    except Exception:
        pass
        # print count

    values = [i[0],uuid,pro,city,dis,cate,i[2]]
    sql = "insert into tmp_raolu(id,uuid,province,city,district,court_cate,court) values(%s,%s,%s,%s,%s,%s,%s)"
    # sql = "update tmp_raolu set new_lawyer = '%s' where id ='%s'" % (new_lawyer,uuid)
    cur.execute(sql,values)
    conn.commit()
    # if id % 5000 == 0:
    #     print id
# area_list = []
# for i in law_list:
#     n = get_public_defendant_party(i)
#     if n:
#         print n

    # area_list.append(n)
    # j = get_public_defendant_party(i)

