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


if __name__ == "__main__":
    print time.time()

    conn2 = pymysql.connect(host='192.168.12.34', user='root', passwd='root', db='laws_doc', charset='utf8')
    cursor2 = conn2.cursor()

    sql2 = "select id,reason_uid from judgment_etl where id <= 200000 "
    cursor2.execute(sql2)
    row_2 = cursor2.fetchall()
    for row in row_2:
        # 获取pid_num，新增的数据编号从：pid_num+1开始
        if row[1] and row[1] != '':
            reason_l = row[1].strip().split("||")
            reason_uids = ""
            t = []
            for uid in reason_l:
                t.extend(flat_uid(uid))
            reason_uids = "||".join(list(set(t)))
                # print reason_uids + "--------------"
        #     uid = row2[1].encode("utf-8") + str(pid_num).zfill(3)
            sql3 = "update judgment_etl set reason_uid ='%s' where id='%s'"  % (reason_uids, row[0])
            effect_row = cursor2.execute(sql3)
    conn2.commit()
    cursor2.close()
    conn2.close()
    print time.time()