# -*- coding: utf-8 -*-
import pymysql
import redis


pool = redis.ConnectionPool(host='master-slave1', port=6379, decode_responses=True,db=0,password="hhly_new_pass") #连接redis，加上decode_responses=True，写入的键值对中的value为str类型，不加这个参数写入的则为字节类型
r = redis.Redis(connection_pool=pool)


conn=pymysql.connect(host='slave2',user='weiwc',passwd='HHly2017.',db='implement_v2',charset='utf8')
cursor = conn.cursor()
sql = 'select uuid from uuids '   #LOCATE函数，包含||,返回大于0的数值。
cursor.execute(sql)
row_2 = cursor.fetchall()


pipe = r.pipeline() # 创建一个管道


for row in row_2 :
    pipe.sadd("laws_doc:judgment_implement_all",row[0])  # 往集合中添加元素
    pipe.incr("num")

pipe.execute()

print (pipe.get("num"))
print (pipe.smembers("laws_doc:judgment_implement_all"))

cursor.close()
conn.close()