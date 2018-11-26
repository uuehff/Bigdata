# -*- coding: utf-8 -*-

import time
import pymysql
def flat_uid(uid):
    reason_uid = []
    if len(uid) == 7:
        reason_uid.append(uid[:4])
    elif len(uid) == 10:
        reason_uid.append(uid[:4])
        reason_uid.append(uid[:7])
    elif len(uid) == 13:
        reason_uid.append(uid[:4])
        reason_uid.append(uid[:7])
        reason_uid.append(uid[:10])
    elif len(uid) == 16:
        reason_uid.append(uid[:4])
        reason_uid.append(uid[:7])
        reason_uid.append(uid[:10])
        reason_uid.append(uid[:13])
    else:
        pass
    reason_uid.append(uid)
    return reason_uid


# 将筛选history中uuid个数为多个的，并将该uuid对应的四个字段与当前记录的四个字段对应一样，则保留该uuid在history中！
if __name__ == "__main__":
    print time.time()

    conn = pymysql.connect(host='192.168.12.34', user='root', passwd='root', db='laws_doc', charset='utf8')
    cursor = conn.cursor()

    conn2 = pymysql.connect(host='192.168.12.34', user='root', passwd='root', db='laws_doc2', charset='utf8')
    cursor2 = conn2.cursor()

    sql2 = "select uuid,history from judgment2_etl where history is not null and history != '' "
    cursor2.execute(sql2)
    row_2 = cursor2.fetchall()
    for row in row_2:
        # 获取pid_num，新增的数据编号从：pid_num+1开始
        history = row[1].strip().split("||")
        ht = []
        for uuid in history:
            # print len(history)
            # print uuid
            sql = "select title from judgment where uuid = '" + uuid + "'"
            cursor.execute(sql)
            uuid_row = cursor.fetchone()
            ht.append(uuid_row[0])
        sql3 = "update judgment2_etl set history_title ='%s' where uuid='%s'" % ("||".join(ht), row[0])
        effect_row = cursor2.execute(sql3)

        # if history_new:
        #     history2 = "||".join(history_new)
        #     sql3 = "update judgment2_etl set history ='%s' where id='%s'"  % (history2, row[0])
        #     effect_row = cursor2.execute(sql3)
        # else:
        #     sql3 = "update judgment2_etl set history ='%s' where id='%s'" % ('', row[0])
        #     effect_row = cursor2.execute(sql3)

    conn2.commit()
    cursor2.close()
    conn2.close()
    print time.time()