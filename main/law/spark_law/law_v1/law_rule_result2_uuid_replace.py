# -*- coding: utf-8 -*-

import time
import pymysql


if __name__ == "__main__":
    print time.asctime(time.localtime(time.time()))

    conn2 = pymysql.connect(host='192.168.74.103', user='weiwc', passwd='HHly2017.', db='law', charset='utf8')
    cursor2 = conn2.cursor()

    sql2 = "select id,law_id,art_digit from law_rule_result2  where law_id = "
    cursor2.execute(sql2)
    row_2 = cursor2.fetchall()
    c = 1
    for row in row_2:
            law_id = str(c)
            lawlist_id = law_id + row[2].strip().zfill(4)
        #     uid = row2[1].encode("utf-8") + str(pid_num).zfill(3)
            sql3 = "update law_rule_result2 set law_id ='%s', lawlist_id ='%s' where id='%s'"  % (law_id,lawlist_id, row[0])
            effect_row = cursor2.execute(sql3)
            c += 1
            # print row[0],law_id,lawlist_id
            # print sql3
    conn2.commit()
    cursor2.close()
    conn2.close()
    print time.asctime(time.localtime(time.time()))