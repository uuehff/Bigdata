# -*- coding: utf-8 -*-

import time
import pymysql

if __name__ == "__main__":
    print time.time()
    conn = pymysql.connect(host='192.168.12.34', user='root', passwd='root', db='laws_doc', charset='utf8')
    cursor = conn.cursor()
    # sql = 'select id,art_num from law_rule_result2 '
    sql = 'update judgment_etl j, uuid_and_lawlist_ids_1shen_result t set j.lawlist_ids = t.lawlist_ids where j.uuid = t.uuid;'

    cursor.execute(sql)

    row_2 = cursor.fetchall()

    for row in row_2:
        # id为int类型，不用%d!

        # lawlist_id = getLawlistID(row[1])
        # print row[1],int(lawlist_id)


        # art_num.strip()
        sql2 = "update law_rule_result2 set art_num='%s' where id='%s'" % (row[1].strip(), row[0])
        # sql2 = " insert into effective_range_field (id,effective_range) values (%s, %s)"
        effect_row = cursor.execute(sql2)

    conn.commit()
    cursor.close()
    conn.close()
    print time.time()