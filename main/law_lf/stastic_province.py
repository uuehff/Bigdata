# encoding:utf-8
import MySQLdb
import datetime

con = MySQLdb.connect(host='192.168.12.34', user='liuf', passwd='123456', db='laws_doc', charset='utf8')
cursor = con.cursor()
import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import multiprocessing

# 插入省份
# def update(int_num):
#     con = MySQLdb.connect(host='192.168.12.34', user='liuf', passwd='123456', db='laws_doc', charset='utf8')
#     cursor = con.cursor()
#     sql = "select uuid, province from tmp_raolu"
#     cursor.execute(sql)
#     row = cursor.fetchall()
#     for n in int_num:
#         # print row[n][0],row[n][1]
#         sql = "update tmp_liufang set province='%s' where uuid='%s'"%(row[n][1],row[n][0])
#         cursor.execute(sql)
#     con.commit()
#     cursor.close()
#     con.close()
# if __name__ == '__main__':
#     pool = multiprocessing.Pool(processes=8)
#     pool.apply_async(update, (xrange(40 * 10000),))
#     pool.apply_async(update, (xrange(40 * 10000, 80 * 10000),))
#     pool.apply_async(update, (xrange(80*10000, 120*10000), ))
#     pool.apply_async(update, (xrange(120*10000, 160*10000), ))
#     pool.apply_async(update, (xrange(160*10000, 200*10000), ))
#     pool.apply_async(update, (xrange(200 * 10000, 240 * 10000),))
#     pool.apply_async(update, (xrange(240 * 10000, 270 * 10000),))
#     pool.apply_async(update, (xrange(270 * 10000, 290 * 10000),))
#     pool.close()
#     pool.join()


sql = "select uuid,crime_reason,punish_cate,punish_date,delay_date,punish_money,casedate,province from tmp_liufang"
cursor.execute(sql)
row = cursor.fetchall()

def provincelist(row):
    province_list =[]
    for i in row:
        if i[7]!='' and i[7]!='None':
            province_list.append(i[7])
    return list(set(province_list))
province_list=provincelist(row)

for p in province_list:
    # 近10年案件数
    new10_dict = {}
    t_year_num1=0;t_year_num2=0;t_year_num3=0;t_year_num4=0;t_year_num5=0;t_year_num6=0;t_year_num7=0;t_year_num8=0;t_year_num9=0;t_year_num10=0
    # 罚金
    punish_money_dict = {}
    punish_money_num1 = 0;punish_money_num2 = 0;punish_money_num3 = 0;punish_money_num4 = 0;punish_money_num5 = 0;
    punish_money_num6 = 0;punish_money_num7 = 0;punish_money_num8 = 0;punish_money_num9 = 0
    # 有期徒刑期
    punish_date_dict = {}
    punish_date_num1 = 0;punish_date_num2 = 0;punish_date_num3 = 0;punish_date_num4 = 0;punish_date_num5 = 0;punish_date_num6 = 0;punish_date_num7=0
    # 缓刑期
    delay_date_num1 = 0;delay_date_num2 = 0;delay_date_num3 = 0;delay_date_num4 = 0;delay_date_num5 = 0;delay_date_num6 = 0
    delay_date_dict = {}
    # 是否缓刑
    delay_num1 = 0;delay_num2 = 0
    delay_cate_dict = {}
    # 刑法判决类型
    num1 = 0;num2 = 0;num3 = 0;num4 = 0
    punish_cate_dict = {}
    province_num=0
    for i in row:
        if p == i[7]:
            province_num+=1
            # 判决类型
            if i[2] == u'拘役或管制':
                num1 += 1
            elif i[2] == u'有期徒刑':
                num2 += 1
            elif i[2] == u'无期徒刑':
                num3 += 1
            elif i[2] == u'死刑':
                num4 = 1
            # 是否缓刑
            if i[4] == '' or i[4] =='None':
                delay_num1+=1
            else:
                delay_num2+=1
            # 缓刑期
            if i[4] != '' and i[4] != 'None':
                delay = int(i[4])
                if delay <= 6:
                    delay_date_num1 += 1
                elif delay > 6 and delay <= 12:
                    delay_date_num2 += 1
                elif delay > 12 and delay <= 24:
                    delay_date_num3 += 1
                elif delay > 24 and delay <= 36:
                    delay_date_num4 += 1
                elif delay > 36 and delay <= 60:
                    delay_date_num5 += 1
                elif delay > 60:
                    delay_date_num6 += 1
            # 有期徒刑期
            if i[3] != '' and i[3] != 'None':
                punish_date = int(i[3])
                if punish_date<=6:
                    punish_date_num1+=1
                elif punish_date>6 and punish_date<=12:
                    punish_date_num2+=1
                elif punish_date>12 and punish_date<=24:
                    punish_date_num3+=1
                elif punish_date>24 and punish_date<=36:
                    punish_date_num4+=1
                elif punish_date>36 and punish_date<=60:
                    punish_date_num5+=1
                elif punish_date>60 and punish_date<=84:
                    punish_date_num6+=1
                elif punish_date>84:
                    punish_date_num7+=1
            # 罚金
            if i[5] != '' and i[5] != 'None':
                aa = int(i[5])
                if aa <= 3000:
                    punish_money_num1 += 1
                elif aa > 3000 and aa <= 6000:
                    punish_money_num2 += 1
                elif aa > 6000 and aa <= 10000:
                    punish_money_num3 += 1
                elif aa > 10000 and aa <= 20000:
                    punish_money_num4 += 1
                elif aa > 20000 and aa <= 30000:
                    punish_money_num5 += 1
                elif aa > 30000 and aa <= 50000:
                    punish_money_num6 += 1
                elif aa > 50000 and aa <= 100000:
                    punish_money_num7 += 1
                elif aa > 100000 and aa <= 500000:
                    punish_money_num8 += 1
                elif aa > 500000:
                    punish_money_num9 += 1
            # 近10年的案件数
            if i[6] !='' and i[6] !='None':
                t = datetime.datetime.strptime(i[6], "%Y-%m-%d")
                t_year = int(t.year)
                if t_year == 2017:
                    t_year_num1+=1
                elif t_year == 2016:
                    t_year_num2+=1
                elif t_year == 2015:
                    t_year_num3+=1
                elif t_year == 2014:
                    t_year_num4+=1
                elif t_year == 2013:
                    t_year_num5+=1
                elif t_year == 2012:
                    t_year_num6+=1
                elif t_year == 2011:
                    t_year_num7+=1
                elif t_year == 2010:
                    t_year_num8+=1
                elif t_year == 2009:
                    t_year_num9+=1
                elif t_year == 2008:
                    t_year_num10+=1
    delay_cate_dict[u'没有缓刑'] = delay_num1
    delay_cate_dict[u'缓刑'] = delay_num2

    punish_cate_dict[u'拘役或管制'] = num1
    punish_cate_dict[u'有期徒刑'] = num2
    punish_cate_dict[u'无期徒刑'] = num3
    punish_cate_dict[u'死刑'] = num4
    # print k,punish_cate_dict.keys(),punish_cate_dict.values()

    # print k, delay_date_num1, delay_date_num2, delay_date_num3, delay_date_num4, delay_date_num5, delay_date_num6
    delay_date_dict[u'6个月以下'] = delay_date_num1
    delay_date_dict[u'6个月-1年'] = delay_date_num2
    delay_date_dict[u'1年-2年'] = delay_date_num3
    delay_date_dict[u'2年-3年'] = delay_date_num4
    delay_date_dict[u'3年-5年'] = delay_date_num5
    delay_date_dict[u'5年以上'] = delay_date_num6

    # print k, punish_date_num1, punish_date_num2, punish_date_num3, punish_date_num4, punish_date_num5, punish_date_num6, punish_date_num7
    punish_date_dict[u'6个月以下'] = punish_date_num1
    punish_date_dict[u'6个月-1年'] = punish_date_num2
    punish_date_dict[u'1年-2年'] = punish_date_num3
    punish_date_dict[u'2年-3年'] = punish_date_num4
    punish_date_dict[u'3年-5年'] = punish_date_num5
    punish_date_dict[u'5年-7年'] = punish_date_num6
    punish_date_dict[u'7年以上'] = punish_date_num7

    # print k, punish_money_num1, punish_money_num2, punish_money_num3, punish_money_num4, punish_money_num5, punish_money_num6, punish_money_num7, punish_money_num8, punish_money_num9
    punish_money_dict[u'3千以下'] = punish_money_num1
    punish_money_dict[u'3千-6千'] = punish_money_num2
    punish_money_dict[u'6千-1万'] = punish_money_num3
    punish_money_dict[u'1万-2万'] = punish_money_num4
    punish_money_dict[u'2万-3万'] = punish_money_num5
    punish_money_dict[u'3万-5万'] = punish_money_num6
    punish_money_dict[u'5万-10万'] = punish_money_num7
    punish_money_dict[u'10万-50万'] = punish_money_num8
    punish_money_dict[u'50万以上'] = punish_money_num9

    # print k,t_year_num1,t_year_num2,t_year_num3,t_year_num4,t_year_num5,t_year_num6,t_year_num7,t_year_num8,t_year_num9,t_year_num10
    new10_dict[u'2017年'] = t_year_num1
    new10_dict[u'2016年'] = t_year_num2
    new10_dict[u'2015年'] = t_year_num3
    new10_dict[u'2014年'] = t_year_num4
    new10_dict[u'2013年'] = t_year_num5
    new10_dict[u'2012年'] = t_year_num6
    new10_dict[u'2011年'] = t_year_num7
    new10_dict[u'2010年'] = t_year_num8
    new10_dict[u'2009年'] = t_year_num9
    new10_dict[u'2008年'] = t_year_num10

    delay_cate_dict = json.dumps(delay_cate_dict, ensure_ascii=False)
    punish_cate_dict = json.dumps(punish_cate_dict, ensure_ascii=False)
    delay_date_dict = json.dumps(delay_date_dict, ensure_ascii=False)
    punish_date_dict = json.dumps(punish_date_dict, ensure_ascii=False)
    punish_money_dict = json.dumps(punish_money_dict, ensure_ascii=False)
    new10_dict = json.dumps(new10_dict, ensure_ascii=False)
    value = [p,province_num,new10_dict, punish_cate_dict, punish_date_dict, delay_cate_dict,delay_date_dict, punish_money_dict]
    print p,province_num,new10_dict, punish_cate_dict, punish_date_dict, delay_cate_dict, delay_date_dict, punish_money_dict
#   插入数据
    insert_sql = "insert into scene_province(province,province_num,new10_dict,punish_cate_dict,punish_date_dict,delay_cate_dict,delay_date_dict,punish_money_dict) values (%s,%s,%s,%s,%s,%s,%s,%s)"
    cursor.execute(insert_sql, value)
con.commit()


