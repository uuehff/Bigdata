# -*- coding: utf-8 -*-
import pymysql
import re

date_range = ["2012-*","2002-2012","1992-2002","1982-1992","1978-1982","1949-1978"]

def mapRange(y_m_d):
    year = int(row[1].split("-")[0])
    # print year
    # print type(year)
    if year >= 2012:           #前闭后开区间
        return date_range[0]
    elif year >= 2002:
        return date_range[1]
    elif year >= 1992:
        return date_range[2]
    elif year >= 1982:
        return date_range[3]
    elif year >= 1978:
        return date_range[4]
    elif year >= 1949:
        return date_range[5]
    else:
        return str(year)
import time
if __name__ == '__main__':

    print time.time()
    conn=pymysql.connect(host='192.168.12.35',user='root',passwd='HHly2017.',db='law',charset='utf8')
    cursor = conn.cursor()
    sql = 'select id,effective_date from law_rule_result2'
    cursor.execute(sql)
    # row_1 = cursor.fetchone()
    # row_2 = cursor.fetchmany(5)
    row_2 = cursor.fetchall()

    for row in row_2 :
        # id为int类型，不用%d!
        sql2 = " insert into effective_range_field (id,effective_range) values (%s, %s)"
        effect_row = cursor.execute(sql2,(row[0],mapRange(row[1])))

    conn.commit()
    cursor.close()
    conn.close()
    print time.time()