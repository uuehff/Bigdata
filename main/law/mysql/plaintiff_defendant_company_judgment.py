# -*- coding: utf-8 -*-
import pymysql
import re

import time

print time.asctime( time.localtime(time.time()) )
# for i in range(1,28):
#     num = i * 100000
conn=pymysql.connect(host='192.168.12.34',user='root',passwd='root',db='laws_doc',charset='utf8')
cursor = conn.cursor()
# sql = 'select uuid,party_info from lawyer_picture where id < 2'   #LOCATE函数，包含||,返回大于0的数值。
sql = 'select uuid,party_info from lawyer_picture where party_info like "%被告%公司%"  or party_info like "%原告%公司%" '   #LOCATE函数，包含||,返回大于0的数值。
cursor.execute(sql)
# row_1 = cursor.fetchone()
# row_2 = cursor.fetchmany(5)
row_2 = cursor.fetchall()

import re
for row in row_2 :

    if row[1] and row[1] != "":
        result= re.split("[" + u"，，：。\n\r " + "]+",row[1])    #将当事人信息字段，按，。：换行等等分割
        plaintiff = []
        defendant = []

        # 附带民事诉讼被告人：赵西松。肇事冀B×××××号重型自卸车所有人。
        # 自诉人暨附带民事诉讼原告：昆明某某某有限公司。
        # 附带民事诉讼原告人××有限责任公司，住所××。
        for i in range(len(result)):
            if (result[i].endswith(u"原告") or result[i].endswith(u"原告人")) and i< len(result)-1 :  #限制i的大小，防止result[i+1]会数组越界
                if not result[i+1].startswith(u"××") and u"公司" in result[i+1]:
                    if result[i+1].endswith(u"公司"):
                        plaintiff.append(result[i+1])
                    else:
                        # 刑事附带民事被告：广西来宾中兴汽车运输有限责任公司来宾汽车总站。
                        plaintiff.append(result[i+1].split(u"公司")[0] + u"公司")
            elif result[i].endswith(u"被告") or result[i].endswith(u"被告人")  and i< len(result)-1:
                # 附带民事诉讼被告：中国大地财产保险股份有限公司阜新中心支公司，地址阜新市细河区迎宾大街中段宝典大厦。
                if not result[i+1].startswith(u"××") and u"公司" in result[i+1]:
                    if result[i+1].endswith(u"公司"):
                        defendant.append(result[i+1])
                    else:
                        defendant.append(result[i+1].split(u"公司")[0] + u"公司")
            elif result[i].endswith(u"公司"):
                if u"原告人" in result[i]:
                    # 附带民事诉讼被告人天安财产保险股份有限公司江西省分公司。
                    if not result[i].split(u"原告人")[1].startswith(u"××"):
                        # 附带民事诉讼被告：中国大地财产保险股份有限公司通城营销部（以下简称大地保险公司）
                        plaintiff.append(result[i].split(u"原告人")[1].split(u"公司")[0] + u"公司")
                elif u"原告" in result[i]:
                    if not result[i].split(u"原告")[1].startswith(u"××"):
                        plaintiff.append(result[i].split(u"原告")[1].split(u"公司")[0] + u"公司")
                elif u"被告人" in result[i]:
                    if not result[i].split(u"被告人")[1].startswith(u"××"):
                        defendant.append(result[i].split(u"被告人")[1].split(u"公司")[0] + u"公司")
                elif u"被告" in result[i]:
                    if not result[i].split(u"被告")[1].startswith(u"××"):
                        defendant.append(result[i].split(u"被告")[1].split(u"公司")[0] + u"公司")
        if plaintiff :
             plaintiff = "||".join(plaintiff)
        else: plaintiff = ""

        if defendant :
             defendant = "||".join(defendant)
        else:defendant = ""
        sql2 = " update lawyer_picture set plaintiff_company ='" + plaintiff + "', defendant_company = '" + defendant + "' where uuid = '" + str(row[0]) + "'"
        cursor.execute(sql2)
conn.commit()
cursor.close()
conn.close()
print time.asctime( time.localtime(time.time()) )