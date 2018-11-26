# -*- coding: utf-8 -*-

import time
import pymysql

if __name__ == "__main__":
    print time.time()

    conn2 = pymysql.connect(host='192.168.12.34', user='root', passwd='root', db='laws_doc2', charset='utf8')
    cursor2 = conn2.cursor()

    sql2 = "select pid from court_add_distinct where uid is null group by pid"
    cursor2.execute(sql2)
    row_2 = cursor2.fetchall()

    conn = pymysql.connect(host='192.168.12.34', user='root', passwd='root', db='laws_doc', charset='utf8')
    cursor = conn.cursor()
    for row in row_2:
        # print type(row[0])
        # 获取pid_num，新增的数据编号从：pid_num+1开始
        sql = "select count(*) from court where pid = '" + row[0].encode("utf8") + "'"
        cursor.execute(sql)
        tmp_num = cursor.fetchall()
        pid_num = 0
        for i in tmp_num:
            pid_num = i[0]

        sql_pids = "select id,pid from court_add_distinct where pid = '" + row[0].encode("utf8") + "'"
        cursor2.execute(sql_pids)
        row_3 = cursor2.fetchall()

        for row2 in row_3:
            pid_num += 1
            # print row2[0],row2[1],row2[2]
            uid = row2[1].encode("utf-8") + str(pid_num).zfill(3)
            sql3 = "update court_add_distinct set uid ='%s' where id='%s'" % (uid, row2[0])
            # print row2[0],uid,
            # print "======================"
            effect_row = cursor2.execute(sql3)
    conn.commit()
    cursor.close()
    conn.close()
    print time.time()