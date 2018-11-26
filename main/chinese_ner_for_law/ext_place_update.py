# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 11:18:53 2017

@author: Administrator
"""

# mysql法律数据更新
import MySQLdb
import re
import xlrd



def read_location_xcel(path):
    data = xlrd.open_workbook(path)
    table = data.sheet_by_name("sheet")
    result_list = []
    for i in range(0,table.nrows):
        row_content = table.row_values(i,0,table.ncols)
        result_list.append(row_content)
    return result_list

city_list, dis_list, prov_list,place_list = [],[],[],[]
location_list = read_location_xcel("location_law.xlsx")#E:/record/law_data_2/
for i in location_list:
    prov_list.append(i[0])
    city_list.append(i[1])
    dis_list.append(i[2])
    place_list.append(i[3])
    
#法院中提取地区 太慢了 方法2
def clean_place(name,org):
    place=name
    str=[u'中华人民共和国',u'暨附带民事诉讼原告人',u'暨提起附带民事诉讼机关',u'暨附带民事诉讼原告']
    for s in str:
        place=place.replace(s,u'')

    if u'某' in place or u'×' in place or u'X' in place or u'□' in place:
        place=u''
    place=re.sub(ur'[^\u4e00-\u9fa5]',u'',place)
    if len(place) > 0:
        location_pattern = re.compile(u'(?P<province>[\u4e00-\u9fa5]{2,10}?(?:省|自治区)){0,1}'
                                u'(?P<city>[\u4e00-\u9fa5]{2,10}?(?:市|州|盟 |地区)){0,1}'
                                u'(?P<district>[\u4e00-\u9fa5]{1,10}(?:市|区|开发区|县|自治县|旗)){0,1}')
        location_result = re.search(location_pattern, place)
        province = location_result.group("province")
        city = location_result.group("city")
        district = location_result.group("district")           
                        
        for item in location_list:
            if city!=None:
                if city==item[1] and district==None:
                    place = item[0]+item[1]+org
                elif city==item[1] and district==item[2]:
                    place = item[3]+org
                    
                elif city==item[0] and district==None:
                    place =item[0]+org
                elif city==item[0] and district==item[2]:
                    place=item[3]+org
                    
                elif city==item[2]:
                    place = item[3]+org
            elif city==None:
                if province==item[0] and district==None:
                    place = item[0]+org
                if province==None and district==item[2]:
                    place=item[3]+org          
                if province==item[0] and district==item[2]:
                    place=item[3]+org                                        
    if place=='':
        place=u''
    if len(name)==0:
        place=u''
    return place

# 连接数据库
conn=MySQLdb.connect(host='192.168.10.24',user='wxy',passwd='123456', db='laws_doc',charset='utf8')
cursor=conn.cursor()
a=940000
b=949999
while b<2830000:
    cursor.execute("select id,uuid,court,doc_oriligigation from judgment where id between '%s' and '%s'" % (a,b))
    results=cursor.fetchall()  
    for r in results:
        court_=clean_place(r[2],u'人民法院')
        oriligigation_=clean_place(r[3],u'人民检察院')         
        sql="update tmp_wxy set court_new='%s' where uuid='%s'" % (court_,r[1])
        cursor.execute(sql)
        sql1="update tmp_wxy set doc_oriligigation_new='%s' where uuid='%s'" % (oriligigation_,r[1])
        cursor.execute(sql1)
    conn.commit()
    print b
    a +=10000
    b +=10000
