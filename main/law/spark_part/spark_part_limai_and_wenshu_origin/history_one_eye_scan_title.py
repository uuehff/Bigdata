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

    sql2 = "select uuid,province,age_year,if_surrender,if_nosuccess,if_accumulate,history from judgment2_etl where id <1000 and history is not null and history != '' and CHAR_LENGTH(history) = 36"
    cursor2.execute(sql2)
    row_2 = cursor2.fetchall()
    a = 0
    b = 0
    for row in row_2:
        b +=1
        history = row[6].strip().split("||")
        sql = "select id,province,age_year,if_surrender,if_nosuccess,if_accumulate from judgment_etl where uuid = '" + history[0] + "'"
        cursor.execute(sql)
        uuid_row = cursor.fetchone()
        # if uuid_row and row[1]==uuid_row[1] and row[2]==uuid_row[2] and row[3]==uuid_row[3] and row[4]==uuid_row[4] and row[5]==uuid_row[5]:
        if uuid_row and row[1]==uuid_row[1]:
            a +=1
            continue
        else:
            print row[1],row[2],row[3],row[4],row[5]
            print uuid_row[1],uuid_row[2],uuid_row[3],uuid_row[4],uuid_row[5]
            # 获取pid_num，新增的数据编号从：pid_num+1开始
            sql_ = "select uuid,title from judgment2 where uuid = '" + row[0] + "'"
            cursor2.execute(sql_)
            data = cursor2.fetchone()
            print data[0],data[1],"-------------------"

            history_new = []
            sql = "select uuid,title from judgment where uuid = '" + history[0] + "'"
            cursor.execute(sql)
            uuid_row = cursor.fetchone()
            if uuid_row:
                print uuid_row[0],uuid_row[1],"===================="
            else :
                print "||||||||||||||||||||||||||||||"
        print "++++++++++++++++++++++++++++++++++++++"
    print a
    print b
    conn2.commit()
    cursor2.close()
    conn2.close()
    print time.time()