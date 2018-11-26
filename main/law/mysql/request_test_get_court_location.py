# encoding:utf-8
import requests
import json
import pymysql
import time
# http://api.map.baidu.com/place/v2/search?query=新疆生产建设兵团塔斯海垦区人民法院&tag=政府机构&region=全国&scope=2&output=json&ak=xy9qkhGkNEfHygHwU1UBC5NjG8HFi25K

# 已认证ak:    xy9qkhGkNEfHygHwU1UBC5NjG8HFi25K

conn=pymysql.connect(host='192.168.12.34',user='root',passwd='root',db='laws_doc2',charset='utf8')
cursor = conn.cursor()
# sql = "select id,court_new from court_city_null where court_new like '%市%市%' "
sql = "select id,court_new,province from court_add_distinct where court_new is not null and court_cate != '高级' "
# sql = "select id,court_new,province from court where city =  '呼和浩特市' and province in ('上海市','天津市','北京市','重庆市') "
# sql = "select id,court_new,province from court where id = 3395 "

# SELECT * from court where city = '呼和浩特市' and province in ("上海市","天津市","北京市","重庆市")

cursor.execute(sql)
row_2 = cursor.fetchall()
# for i2 in range(1,len(row_2)+1):
import re
for row in row_2:
    try :
        r1 = requests.get(
            'http://api.map.baidu.com/place/v2/search?query=' + row[1].encode("utf-8") + '&tag=政府机构&region=' + row[2].encode("utf-8") + '&scope=2&output=json&ak=xy9qkhGkNEfHygHwU1UBC5NjG8HFi25K')
        time.sleep(0.5)
        # print r1.content
        s1 = json.loads(r1.content)['results'][0]['location']
        lat_lng = str(s1['lat']) + "," + str(s1['lng'])     #获取经，纬度
        # print lat_lng
        r2 = requests.get(
            'http://api.map.baidu.com/geocoder/v2/?location=' + lat_lng + '&output=json&pois=1&ak=xy9qkhGkNEfHygHwU1UBC5NjG8HFi25K')

        result = json.loads(r2.content)["result"]['addressComponent']
        # result['province']
        city = result['city']
        district = result['district']
        # print city,district
        sql2 = " update court_add_distinct set city = '" + city + "', district = '" + district + "' where id = '" + str(row[0]) + "'"
        cursor.execute(sql2)
    except Exception, e:
        print e
        # print r1.text
        print row[0],row[1] + "error : "
# print i
conn.commit()
cursor.close()
conn.close()



# http://api.map.baidu.com/place/v2/search?query=%E9%80%9A%E5%8C%96%E9%93%81%E8%B7%AF%E8%BF%90%E8%BE%93%E6%B3%95%E9%99%A2&tag=%E6%94%BF%E5%BA%9C%E6%9C%BA%E6%9E%84&region=%E5%85%A8%E5%9B%BD&scope=2&output=json&ak=t5cHoyEwPHRt2bu7y4epmDPOCQ9lIK1t