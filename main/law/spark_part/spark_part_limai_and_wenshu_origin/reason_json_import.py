# -*- coding: utf-8 -*-

import time
import pymysql
import json
print time.time()
if __name__ == "__main__":
    file_object = open(r"E:\PycharmProjects\data_etl\main\law\uuid2lawlist\reason2.json")
    json_data = file_object.read()

    conn2 = pymysql.connect(host='192.168.12.34', user='root', passwd='root', db='laws_doc', charset='utf8')
    cursor = conn2.cursor()

    try:
        for i in json.loads(json_data):
            n2 = i['n'].strip().rstrip(u'罪')              #去除前后空格，在去除右边匹配到的罪字。
            sql2 = " insert into reason_bashou (p,i,n) values (%s, %s, %s)"
            effect_row = cursor.execute(sql2,(i['p'],i['i'],n2))
    finally:
        file_object.close()