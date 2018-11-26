# coding:utf-8
import pymysql

import math


#判断是否为质数，质数返回1
def isPrime(n):
    if n <= 1:
        return 0
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return 0
    return 1

def isOdd(n):
    if n%2 == 1:
        return True
    else: 
        return False
def red_range(row):
    row2 = row[1:7]
    yi, er, san, si = 0, 0, 0, 0
    for i in row2:
        if i >= 1 and i <= 9:
            yi += 1
        elif i >= 10 and i <= 19:
            er += 1
        elif i >= 20 and i <= 29:
            san += 1
        else:
            si += 1
    return yi, er, san, si

# -- ==============================
# -- ssq规则：(更新数据：2\4\7)
# -- r1~r6: 1 ~ 33
# -- b1:	1 ~ 16
# 四区：
# 一：1~9
# 二：10~19
# 三：20~29
# 四：30~33
# -- ==============================
# -- dlt规则：(更新数据：1\3\6)
# -- r1~r5: 1 ~ 35
# -- b1~b2: 1 ~ 12
if __name__ == '__main__':

    conn = pymysql.connect(host='192.168.12.35', user='root', passwd='HHly2017.', db='algorithm', charset='utf8')
    cursor = conn.cursor()
    sql = 'select * from ssq '
    cursor.execute(sql)
    # row_1 = cursor.fetchone()
    # row_2 = cursor.fetchmany(5)
    rows = cursor.fetchall()
    for row in rows:

        odd = row[1]%2 + row[2]%2 + row[3]%2 + row[4]%2 + row[5]%2 + row[6]%2
        prime = isPrime(row[1]) + isPrime(row[2]) + isPrime(row[3]) + isPrime(row[4]) + isPrime(row[5]) + isPrime(row[6])
        sum = row[1]+row[2]+row[3]+row[4]+row[5]+row[6]
        area = red_range(row)

        # area 比例
        # print red_range(row)
        #
        # # red_min、red_max、blue
        # print  row[1], row[6], row[7]
        #
        # # odd、evev
        # print odd, 6 - odd
        #
        # # prime number、number
        # print prime, 6 - prime
        #
        # # red_sum，red_sum+bule，blue
        # print sum,sum+row[7],row[7]

        # id为int类型，不用%d!
        sql2 = " insert into factor values (%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s)"
        effect_row = cursor.execute(sql2, (row[0],area[0],area[1],area[2],area[3],row[1],row[6],row[7],odd,6-odd,prime,6-prime,sum,sum+row[7],row[7]))

        # print red_range(row),('%02d' % row[1], '%02d' % row[6], '%02d' % row[7]),(odd, 6 - odd),(prime, 6 - prime),('%03d' % sum,'%03d' % (sum+row[7]),'%03d' % row[7])
        # print "-------------------------------"
    conn.commit()
    cursor.close()
    conn.close()


