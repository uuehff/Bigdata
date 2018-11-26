# -*- coding: utf-8 -*-

import time
import pymysql
if __name__ == "__main__":
    print time.time()

    conn2 = pymysql.connect(host='192.168.12.34', user='root', passwd='root', db='laws_doc2', charset='utf8')
    cursor2 = conn2.cursor()

    sql2 = "select id,reason_uid from judgment2_etl where reason_uid != '' and reason_uid is not null "
    cursor2.execute(sql2)
    row_2 = cursor2.fetchall()
    for row in row_2:
        reason_l = row[1].strip().split("||")
        reason_uids = "||".join(list(set(reason_l)))
        sql3 = "update judgment2_etl set reason_uid ='%s' where id='%s'"  % (reason_uids, row[0])
        effect_row = cursor2.execute(sql3)
    conn2.commit()
    cursor2.close()
    conn2.close()
    print time.time()