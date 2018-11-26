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

    sql2 = "select id,province,age_year,if_surrender,if_nosuccess,if_accumulate,history from judgment2_etl where history is not null and history != '' and CHAR_LENGTH(history) < 36"
    cursor2.execute(sql2)
    row_2 = cursor2.fetchall()
    for row in row_2:
        # 获取pid_num，新增的数据编号从：pid_num+1开始
        history = row[6].strip().split("||")
        history_new = []
        for uuid in history:
            sql = "select id,province,age_year,if_surrender,if_nosuccess,if_accumulate from judgment_etl where uuid = '" + uuid + "'"
            cursor.execute(sql)
            uuid_row = cursor.fetchone()
            # if uuid_row and row[1]==uuid_row[1] and row[2]==uuid_row[2] and row[3]==uuid_row[3] and row[4]==uuid_row[4] and row[5]==uuid_row[5]:
            if uuid_row:
                history_new.append(uuid)
        if history_new:
            history2 = "||".join(history_new)
            sql3 = "update judgment2_etl set history ='%s' where id='%s'"  % (history2, row[0])
            effect_row = cursor2.execute(sql3)
        else:
            print row[0],history
            sql3 = "update judgment2_etl set history ='%s' where id='%s'" % ('', row[0])
            effect_row = cursor2.execute(sql3)

    conn2.commit()
    cursor2.close()
    conn2.close()
    print time.time()