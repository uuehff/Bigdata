# -*- coding: utf-8 -*-
# join
# 传统的join操作会导致shuffle操作。
# 因为两个RDD中，相同的key都需要通过网络拉取到一个节点上，由一个task进行join操作。
from pyspark import SparkContext

sc = SparkContext("local","test")
sc.setLogLevel("ERROR")

#使用flatMap + broadcast实现join,避免shuffle!

# ================================================================================
# rdd1 = sc.parallelize([("cat",2), ("cat", 5), ("book", 4)])
# rdd2 = sc.parallelize([("cat",2), ("cup", 5), ("book", 4),("cat", 12),("cat",22), ("cup", 50), ("mouse", 40),("cat", 120)])
#
# b = sc.broadcast(rdd1.collect())
# def m(x):
#     l = []
#     for k,v in b.value:
#         if x[0] == k:
#             l.append((x[0],(v,x[1])))
#     return l
#
# # print rdd1.join(rdd2).collect()
# print rdd2.flatMap(m).collect()
#
# [('book', (4, 4)), ('cat', (2, 2)), ('cat', (2, 12)), ('cat', (2, 22)), ('cat', (2, 120)), ('cat', (5, 2)), ('cat', (5, 12)), ('cat', (5, 22)), ('cat', (5, 120))]
# [('cat', (2, 2)), ('cat', (5, 2)), ('book', (4, 4)), ('cat', (2, 12)), ('cat', (5, 12)), ('cat', (2, 22)), ('cat', (5, 22)), ('cat', (2, 120)), ('cat', (5, 120))]
# ================================================================================
# 使用mapPartitions替代普通map
# 注意：mapPartitions()中的算子返回时需要使用yield，不能使用return!
# 使用mapPartitions()代替map()

# rdd = sc.parallelize([1, 2, 2, 3, 3, 4], 2)
#
# def f(iterator): yield sum(iterator)
# def f2(x):
#     l = []
#     for v in x:
#         l.append(v+10)
#     yield l         #注意：这里使用return的话，下面使用mapPartitions()时结果不对，因为这里return没有真正返回list对象
# def p(x):  print type(x)
#
# print rdd.glom().collect()
# print rdd.map(lambda x: x+10).collect()
# print rdd.mapPartitions(f2).flatMap(lambda x: x).collect()
# print rdd.mapPartitions(f2).collect()
# rdd.mapPartitions(f2).foreach(p)
# [[1, 2, 2], [3, 3, 4]]
# [11, 12, 12, 13, 13, 14]
# [11, 12, 12, 13, 13, 14]
# [[11, 12, 12], [13, 13, 14]]
# <type 'list'>
# <type 'list'>
# ================================================================================
# 数据倾斜问题，key分布不均匀，countByKey + collect查看Key的分布情况！
# 数据倾斜的解决方案
# 解决方案一：使用Hive ETL预处理数据，将shuffle过程提前到Hive中
# 使用场景：导致数据倾斜的是Hive表。hive表中的数据本身key分布不均匀，可以现在hive中进行join、groupby等预处理，
# 然后spark处理预处理后的中间表，可在sparK中避免shuffle。

# 解决方案二：过滤少数导致倾斜的key
# 如果发现导致倾斜的key就少数几个，而且对计算本身的影响并不大的话，那么很适合使用这种方案。比如99%的key就对应10条数据，
# 但是只有一个key对应了100万数据，从而导致了数据倾斜。

# 使用参考：   http://tech.meituan.com/spark-tuning-pro.html
# 解决方案三：采样倾斜key并分拆join操作
# 方案适用场景：两个RDD/Hive表进行join的时候，如果数据量都比较大，无法采用 map + broadcast方式，那么如果出现数据倾斜，
# 是因为其中某一个RDD/Hive表中的少数几个key的数据量过大，而另一个RDD/Hive表中的所有key都分布比较均匀，那么采用这个解决方案是比较合适的。
# 方案实现思路：
# 1）对包含少数几个数据量过大的key的那个RDD，通过sample算子采样出一份样本来，然后统计一下每个key的数量，计算出来数据量最大的是哪几个key。
# 2）然后将这几个key对应的数据从原来的RDD中拆分出来，形成一个单独的RDD，并给每个key都打上n以内的随机数作为前缀，其余key的数据形成另外一个RDD。
# 3）接着将需要join的另一个RDD，也过滤出来那几个倾斜key对应的数据并形成一个单独的RDD，将每条数据膨胀成n条数据，这n条数据都按顺序附加一个0~n的前缀，其余key的数据形成另外一个RDD。
# 4）再将附加了随机前缀的独立RDD与另一个膨胀n倍的独立RDD进行join，此时就可以将原先两个RDD中相同的key最大分散到n个分区中，分散到多个task中去进行join了。
# 而另外两个普通的RDD就照常join即可。
# 5）最后将两次join的结果使用union算子合并起来即可，就是最终的join结果。

# 数据说明：假设data中key为cat和book的数据会引起数据倾斜！

data = [("a", 1), ("b", 1), ("a", 1),("cat",2), ("cat", 5),("cat",20), ("cat", 50),("cat",200), ("cat", 500),
        ("book", 6),("book", 60), ("book", 61), ("book", 62), ("book", 63),("book", 64)]

data2 = [("a", 10), ("b", 16), ("a", 11),("a", 12),("cat",2), ("cat", 5), ("book", 666)]

rdd1 = sc.parallelize(data)
rdd2 = sc.parallelize(data2)

# print rdd2.join(rdd1,2).glom().collect()

def filter_key(elem):
    if elem[0] in top_key:
        return True
    else:
        return False


sets1 = rdd1.countByKey().items()       #   [('a', 2), ('b', 1), ('book', 6), ('cat', 6)]
rdd3 = sc.parallelize(sets1).map(lambda t:(t[1],t[0])).sortByKey(False).cache()
# print rdd1.takeSample(False,8)
# print rdd3.collect()        #[(6, 'book'), (6, 'cat'), (2, 'a'), (1, 'b')]
# print rdd3.take(3)          #[(6, 'book'), (6, 'cat'), (2, 'a')]
# print rdd3.top(3)           #[(6, 'cat'), (6, 'book'), (2, 'a')]
# print rdd3.map(lambda x: x[1]).take(2)      #['book', 'cat']

top_key = rdd3.map(lambda x: x[1]).take(2)

#拆分rdd1
top_key_rdd1 = rdd1.filter(filter_key)      #含有导致数据倾斜的key的rdd
rest_rdd1 = rdd1.subtract(top_key_rdd1)

#拆分rdd2
top_key_rdd2 = rdd2.filter(filter_key)
rest_rdd2 = rdd2.subtract(top_key_rdd2)

#正常的key聚合
rest_result = rest_rdd1.join(rest_rdd2)

# =====================
# print rdd1.join(rdd2).collect()
# print rest_result.collect()
#
# print top_key_rdd1.collect()
# print rest_rdd1.collect()
#
# print top_key_rdd2.collect()
# print rest_rdd2.collect()

# [('a', (1, 10)), ('a', (1, 11)), ('a', (1, 12)), ('a', (1, 10)), ('a', (1, 11)), ('a', (1, 12)), ('b', (1, 16)), ('book', (6, 666)), ('book', (60, 666)), ('book', (61, 666)), ('book', (62, 666)), ('book', (63, 666)), ('book', (64, 666)), ('cat', (2, 2)), ('cat', (2, 5)), ('cat', (5, 2)), ('cat', (5, 5)), ('cat', (20, 2)), ('cat', (20, 5)), ('cat', (50, 2)), ('cat', (50, 5)), ('cat', (200, 2)), ('cat', (200, 5)), ('cat', (500, 2)), ('cat', (500, 5))]
# [('a', (1, 10)), ('a', (1, 12)), ('a', (1, 11)), ('a', (1, 10)), ('a', (1, 12)), ('a', (1, 11)), ('b', (1, 16))]
# [('cat', 2), ('cat', 5), ('cat', 20), ('cat', 50), ('cat', 200), ('cat', 500), ('book', 6), ('book', 60), ('book', 61), ('book', 62), ('book', 63), ('book', 64)]
# [('b', 1), ('a', 1), ('a', 1)]
# [('cat', 2), ('cat', 5), ('book', 666)]
# [('a', 10), ('a', 12), ('b', 16), ('a', 11)]

#top_key聚合，即导致shuffle的key聚合，这里可以使用两种方式：对key加前缀 或 map + broadcast ！
# 方式一：加前缀大散key进行join，使原来相同的key可以分布到多个分区！
# 变换数据

import random
def randomData():
    return random.randint(1,9)      #产生1-9,9个数字，包括1和9

def gen(x):
    l = []
    d = 1
    while (d < 10):
        l.append(( str(d)+x[0],x[1]))
        d += 1
    return l

dist_rdd1 = top_key_rdd1.map(lambda x:(str(randomData())+x[0],x[1])).cache()
dist_rdd2 = top_key_rdd2.flatMap(gen).cache()

# print dist_rdd1.collect()
# print dist_rdd2.collect()
# [('6cat', 2), ('3cat', 5), ('1cat', 20), ('4cat', 50), ('9cat', 200), ('8cat', 500), ('1book', 6), ('5book', 60), ('9book', 61), ('7book', 62), ('8book', 63), ('3book', 64)]
# [('1cat', 2), ('2cat', 2), ('3cat', 2), ('4cat', 2), ('5cat', 2), ('6cat', 2), ('7cat', 2), ('8cat', 2), ('9cat', 2), ('1cat', 5), ('2cat', 5), ('3cat', 5), ('4cat', 5), ('5cat', 5), ('6cat', 5), ('7cat', 5), ('8cat', 5), ('9cat', 5), ('1book', 666), ('2book', 666), ('3book', 666), ('4book', 666), ('5book', 666), ('6book', 666), ('7book', 666), ('8book', 666), ('9book', 666)]

# python字符串截取：
# str = ’0123456789′
# print str[0:3] #截取第一位到第三位的字符
# print str[:] #截取字符串的全部字符
# print str[6:] #截取第七个字符到结尾
# print str[:-3] #截取从头开始到倒数第三个字符之前
# print str[2] #截取第三个字符
# print str[-1] #截取倒数第一个字符
# print str[::-1] #创造一个与原字符串顺序相反的字符串
# print str[-3:-1] #截取倒数第三位与倒数第一位之前的字符
# print str[-3:] #截取倒数第三位到结尾

top_key_join_result = dist_rdd1.join(dist_rdd2,9).cache()
top_key_result = top_key_join_result.map(lambda x:(x[0][1:],x[1]))      # 去掉之前添加的数字前缀

# print top_key_join_result.getNumPartitions()
# print top_key_join_result.sortByKey().glom().collect()
# print top_key_result.sortByKey().collect()

# 9
# [[('1cat', (500, 2)), ('1cat', (500, 5)), ('2cat', (5, 2)), ('2cat', (5, 5))],
#  [('3book', (6, 666))],
#  [('3cat', (2, 2)), ('3cat', (2, 5))],
#  [('4book', (60, 666)), ('4cat', (20, 2)), ('4cat', (20, 5))],
#  [('5cat', (200, 2)), ('5cat', (200, 5))],
#  [('6book', (61, 666))],
#  [('8book', (63, 666)), ('8book', (64, 666))],
#  [('8cat', (50, 2)), ('8cat', (50, 5))],
#  [('9book', (62, 666))]]
#
# [('book', (6, 666)), ('book', (60, 666)), ('book', (62, 666)), ('book', (63, 666)), ('book', (64, 666)),  ('book', (61, 666)),
#  ('cat', (500, 2)), ('cat', (500, 5)), ('cat', (20, 2)), ('cat', (20, 5)), ('cat', (50, 2)), ('cat', (50, 5)),
#  ('cat', (200, 2)), ('cat', (200, 5)), ('cat', (2, 2)), ('cat', (2, 5)), ('cat', (5, 2)), ('cat', (5, 5))]

# 最总结果对比：
end_result = top_key_result.union(rest_result).cache()     #打散key，拆分join
print end_result.getNumPartitions()
print end_result.sortByKey().collect()

end_result2 = rdd1.join(rdd2).cache()                       #直接join的方式计算结果
print end_result2.getNumPartitions()
print end_result2.sortByKey().collect()

# 13
# [('a', (1, 10)), ('a', (1, 12)), ('a', (1, 11)), ('a', (1, 10)), ('a', (1, 12)), ('a', (1, 11)), ('b', (1, 16)),
#  ('book', (63, 666)), ('book', (6, 666)), ('book', (61, 666)), ('book', (64, 666)), ('book', (62, 666)), ('book', (60, 666)),
#  ('cat', (2, 2)), ('cat', (2, 5)), ('cat', (20, 2)), ('cat', (20, 5)), ('cat', (500, 2)), ('cat', (500, 5)), ('cat', (200, 2)), ('cat', (200, 5)), ('cat', (50, 2)), ('cat', (50, 5)), ('cat', (5, 2)), ('cat', (5, 5))]
# 2
# [('a', (1, 10)), ('a', (1, 11)), ('a', (1, 12)), ('a', (1, 10)), ('a', (1, 11)), ('a', (1, 12)), ('b', (1, 16)),
#  ('book', (6, 666)), ('book', (60, 666)), ('book', (61, 666)), ('book', (62, 666)), ('book', (63, 666)), ('book', (64, 666)),
#  ('cat', (2, 2)), ('cat', (2, 5)), ('cat', (5, 2)), ('cat', (5, 5)), ('cat', (20, 2)), ('cat', (20, 5)), ('cat', (50, 2)), ('cat', (50, 5)), ('cat', (200, 2)), ('cat', (200, 5)), ('cat', (500, 2)), ('cat', (500, 5))]


# 解决方案四：类似方案三，方案三中是少数的Key导致数据倾斜，这一种方案是针对有大量倾斜key的情况，没法将部分key拆分出来进行单独处理，
# 因此使用随机前缀和扩容RDD进行join，因此只能对整个RDD进行数据扩容，对内存资源要求很高。

# 方案实现思路：
# 1）该方案的实现思路基本和“解决方案三”类似，首先查看RDD/Hive表中的数据分布情况，找到那个造成数据倾斜的RDD/Hive表，比如有多个key都对应了超过1万条数据。
# 2）然后将该RDD的每条数据都打上一个n以内的随机前缀。
# 3）同时对另外一个正常的RDD进行扩容，将每条数据都扩容成n条数据，扩容出来的每条数据都依次打上一个0~n的前缀。
# 4）最后将两个处理后的RDD进行join即可。