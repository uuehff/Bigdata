# -*- coding: utf-8 -*-

import time
import pymysql
import uuid as UUID

if __name__ == "__main__":
    print time.asctime(time.localtime(time.time()))

    conn2 = pymysql.connect(host='slave2', user='weiwc', passwd='HHly2017.', db='civil_v2', charset='utf8')
    cursor2 = conn2.cursor()

    sql2 = "select uuid from adjudication_civil_other_fields_v2 limit 10"
    cursor2.execute(sql2)
    row_2 = cursor2.fetchall()
    for row in row_2:
            uuid_ = unicode(UUID.uuid3(UUID.NAMESPACE_DNS2, row[0].encode("utf8"))).replace("-", "")
            sql3 = "update adjudication_civil_other_fields_v2 set uuid ='%s' "  % (uuid_)
            # effect_row = cursor2.execute(sql3)
            print row[0],uuid_,sql3
    conn2.commit()
    cursor2.close()
    conn2.close()
    print time.asctime(time.localtime(time.time()))