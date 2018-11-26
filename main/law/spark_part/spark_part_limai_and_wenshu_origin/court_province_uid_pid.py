# -*- coding: utf-8 -*-

import time
import pymysql

if __name__ == "__main__":
    print time.time()
    conn = pymysql.connect(host='192.168.12.34', user='root', passwd='root', db='laws_doc', charset='utf8')
    cursor = conn.cursor()
    sql = 'select id,province from court_province_city where pid = ' + str(i).zfill(2)

    for i in range(1,32):
        sql = 'select id from court_province_city where pid = ' + str(i).zfill(2)
        cursor.execute(sql)
        row_2 = cursor.fetchall()
        i = 1
        for row in row_2:
            sql2 = "update court_province_city set uid ='%s' where id='%s'" % (str(i).zfill(3), row[0])
            effect_row = cursor.execute(sql2)
            i += 1
    conn.commit()
    cursor.close()
    conn.close()
    print time.time()