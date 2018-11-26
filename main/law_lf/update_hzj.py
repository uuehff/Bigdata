# -*- coding: utf-8 -*-
import MySQLdb
import multiprocessing
import json
import re

con = MySQLdb.connect(host='192.168.12.34', user='liuf', passwd='123456', db='laws_doc', charset='utf8')
cursor = con.cursor()
# sql = "select id,edu from tmp_hzj"
# sql = "select uuid,casedate,crime_reason,province from tmp_liufang"
# sql = 'select a.id,a.gender,a.edu,b.party_info from tmp_hzj a,judgment b where a.id=b.id'
# sql = "select a.id,a.gender,a.edu,b.party_info from tmp_hzj a,judgment b where a.gender!='' and a.edu='' and a.id=b.id"
# sql = "select a.id,a.gender,a.nation,b.party_info from tmp_hzj a,judgment b where a.id=b.id "
sql = "select uuid,province from tmp_raolu"
cursor.execute(sql)
row = cursor.fetchall()

nation56 = [u'阿昌族',u'鄂温克族',u'傈僳族',u'水族',u'白族',u'高山族',u'珞巴族',u'塔吉克族',u'保安族',u'仡佬族',u'满族',u'塔塔尔族',u'布朗族',u'哈尼族'
    ,u'毛南族',u'土家族',u'布依族',u'哈萨克族',u'门巴族',u'土族',u'朝鲜族',u'汉族',u'蒙古族',u'佤族',u'达斡尔族',u'赫哲族',u'苗族',u'维吾尔族',u'傣族'
    ,u'回族',u'仫佬族',u'乌孜别克族',u'德昂族',u'基诺族',u'纳西族',u'锡伯族',u'东乡族',u'京族',u'怒族',u'瑶族',u'侗族',u'景颇族',u'普米族'	,u'彝族'
    ,u'独龙族',u'柯尔克孜族',u'羌族',u'裕固族',u'俄罗斯族',u'拉祜族',u'撒拉族',u'藏族',u'鄂伦春族',u'黎族',u'畲族',u'壮族',u'东乡族',u'穿青族']

other = [u'男',u'女',u'身',u'伊通',u'居',u'人',u'贵州',u'宁夏',u'家住',u'住',u'公民',u'公',u'身份',u'城步',u'新晃',u'通道',u'芷江',u'靖州',
         u'乐从贵族',u'云南省族',u'连山',u'连南',u'三江',u'恭城',u'富川',u'越南',u'巴马',u'都安',u'北川',u'峨边',u'石林',u'玉屏',
         u'漾濞',u'凤城',u'广西']

edu_list1 = [u'研究生', u'博士', u'博士后', u'硕士']
edu_list2 = [u'大学', u'本科']
edu_list3 = [u'专科', u'中专', u'大专', u'高职', u'高专']
edu_list4 = [u'高中', u'中学', u'初中']
edu_list5 = [u'小学', u'文盲']
def edustr(edu):
    edunew = ''
    if edu in edu_list1:
        edunew = u'研究生及以上文化'
    elif edu in edu_list2:
        edunew = u'本科文化'
    elif edu in edu_list3:
        edunew = u'专科文化'
    elif edu in edu_list4:
        edunew = u'中学文化'
    elif edu in edu_list5:
        edunew = u'小学及以下文化'
    return edunew

def update(int_num):
    for n in int_num:
        # edu_new = ''
        # if row[n][1] != '' and row[n][1] != None:
        #     if '||' in row[n][1]:
        #         edu_new = []
        #         edu_list = row[n][1].split('||')
        #         for e in edu_list:
        #             edunew = edustr(e)
        #             edu_new.append(edunew)
        #         edu_new = '||'.join(edu_new)
        #     else:
        #         edu_new = edustr(row[n][1])
        # print edu_new,row[n][0]
        # sql = "update tmp_hzj set edu_new='%s' where id='%s' " % (edu_new,row[n][0])
        sql = "update tmp_hzj set province='%s' where uuid='%s'" % (row[n][1],row[n][0])
        cursor.execute(sql)
    con.commit()
    cursor.close()
    con.close()
        # print row[n][0],row[n][1]
#         sql = "update tmp_hzj set province='%s' where id='%s' " % (row[n][1], row[n][0])
#         cursor.execute(sql)
#         for a in other:
#             if a in row[n][2]:
#                 nation = row[n][2].replace(a,'')
#             sql = "update tmp_hzj set nation='%s' where id='%s'" %(nation,row[n][0])
#             cursor.execute(sql)


if __name__ == '__main__':
    pool = multiprocessing.Pool(processes=7)
    pool.apply_async(update, (xrange(40 * 10000),))
    pool.apply_async(update, (xrange(40 * 10000, 80 * 10000),))
    pool.apply_async(update, (xrange(80 * 10000, 120 * 10000),))
    pool.apply_async(update, (xrange(120 * 10000, 160 * 10000),))
    pool.apply_async(update, (xrange(160 * 10000, 200 * 10000),))
    pool.apply_async(update, (xrange(200 * 10000, 240 * 10000),))
    pool.apply_async(update, (xrange(240 * 10000, 280 * 10000),))
    pool.close()
    pool.join()

# def update(int_num):
#     for n in int_num:
#         if row[n][3]:
#             aa = row[n][3].split()
#         str_info = ''
#         for a in aa:
#             if u'被告' in a:
#                 str_info+=a
#         gender_list = re.findall(u'男|女', str_info)
#         nation_model = re.compile(u'((?<=，|,)[\u4e00-\u9fa5]{1,3}?(?:族))')
#         nation_list = re.findall(nation_model, str_info)
#         nation = '||'.join(nation_list)
#         gender = '||'.join(gender_list)
#         if len(row[n][1]) != len(gender) or len(row[n][2]) < len(nation):
#             print gender,nation,row[n][0]
#             sql = "update tmp_hzj set gender='%s',nation='%s' where id='%s' " % (gender,nation, row[n][0])
#             cursor.execute(sql)
#     con.commit()
#     cursor.close()
#     con.close()
# if __name__ == '__main__':
#     pool = multiprocessing.Pool(processes=7)
#     pool.apply_async(update, (xrange(40 * 10000),))
#     pool.apply_async(update, (xrange(40 * 10000, 80 * 10000),))
#     pool.apply_async(update, (xrange(80*10000, 120*10000), ))
#     pool.apply_async(update, (xrange(120*10000, 160*10000), ))
#     pool.apply_async(update, (xrange(160*10000, 200*10000), ))
#     pool.apply_async(update, (xrange(200 * 10000, 240 * 10000),))
#     pool.apply_async(update, (xrange(240 * 10000, 280 * 10000),))
#     pool.close()
#     pool.join()

# def update(int_num):
#     for n in int_num:
#         aa = row[n][3].split()
#         str_info = ''
#         for a in aa:
#             if u'被告' in a:
#                 str_info+=a
#         if u'专' not in row[n][2]:
#             if u'中专' in str_info or u'大专' in str_info or u'专科' in str_info:
#                 edu = []
#                 if row[n][2]:
#                     edu.append(row[n][2])
#                 edu_list = re.findall(u'中专|大专|专科',str_info)
#                 edustr = '||'.join(edu_list)
#                 print edustr,row[n][0]
#                 sql = "update tmp_hzj set edu='%s' where id='%s' " % (edustr, row[n][0])
#                 cursor.execute(sql)
#     con.commit()
#     cursor.close()
#     con.close()
# if __name__ == '__main__':
#     pool = multiprocessing.Pool(processes=7)
#     pool.apply_async(update, (xrange(40 * 10000),))
#     pool.apply_async(update, (xrange(40 * 10000, 80 * 10000),))
#     pool.apply_async(update, (xrange(80*10000, 120*10000), ))
#     pool.apply_async(update, (xrange(120*10000, 160*10000), ))
#     pool.apply_async(update, (xrange(160*10000, 200*10000), ))
#     pool.apply_async(update, (xrange(200 * 10000, 240 * 10000),))
#     pool.apply_async(update, (xrange(240 * 10000, 280 * 10000),))
#     pool.close()
#     pool.join()




