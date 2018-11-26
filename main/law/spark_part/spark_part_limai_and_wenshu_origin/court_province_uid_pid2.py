# -*- coding: utf-8 -*-

import time
import pymysql

if __name__ == "__main__":
    print time.time()
    conn = pymysql.connect(host='192.168.12.34', user='root', passwd='root', db='laws_doc', charset='utf8')
    cursor = conn.cursor()
    cursor2 = conn.cursor()
    sql = 'select province,city from court_province_city'
    cursor.execute(sql)
    row_2 = cursor.fetchall()

    for row in row_2:
        # print type(row[0])
        sql2 = "select id from court where court_cate != '高级' and court_new is not null and province = '" + row[0].encode("utf8") + "' and city = '" + row[1].encode("utf8") + "'"
        # print sql2
        cursor2.execute(sql2)
        row_3 = cursor2.fetchall()
        # print len(row_3)
        i = 1
        for row2 in row_3:
            # print row2[0],row2[1],row2[2]
            sql3 = "update court set uid ='%s' where id='%s'" % (str(i).zfill(3), row2[0])
            effect_row = cursor.execute(sql3)
            i += 1
    conn.commit()
    cursor.close()
    conn.close()
    print time.time()