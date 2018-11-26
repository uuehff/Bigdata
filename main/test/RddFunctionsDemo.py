# -*- coding: utf-8 -*-
# spark使用总结：    http://www.tuicool.com/articles/JbuMN3u
# 6个聚合函数区别：
# combineByKey(createCombiner, mergeValue, mergeCombiners, numPartitions=None, partitionFunc）
#aggregateByKey(zeroValue, seqFunc, combFunc, numPartitions=None）
# reduceByKey(func, numPartitions=None, partitionFunc=）
# 1）上面三个是（K,V）算子，下面三个是（V）算子。
# 2）由参数可知，combineByKey -> aggregateByKey -> reduceByKey越来越简化，combineByKey为底层实现，
# combineByKey可接受三个参数，第一个是初始化函数，第二个分区内（即map端）聚合函数，第三个分区间（即reduce端）聚合函数；
# aggregateByKey相比combineByKey，第一个参数使用具体的值代替（初始化值只在map端使用），而不是函数，虽然简化了些，但没有方法灵活。其他两个参数都一样。
# reduceByKey相比上边两个：只有一个聚合函数，没有初始化值或函数，分区内与分区间使用同一个聚合函数，即第一个参数。

# aggregate(zeroValue, seqOp, combOp)
# fold(zeroValue, op)
# reduce(f)
# 1）以下三个是（V）算子，对比着上边的三个聚合函数来理解，aggregate类似于aggregateByKey，reduce类似于reduceByKey。
# 其中aggregate和fold的初始化值会在分区内和分区间（即map端reduce端）都会用。

from pyspark import SparkConf,SparkContext

conf = SparkConf()
sc = SparkContext(conf=conf)
sc.setLogLevel("ERROR")

# hd = sc.textFile("hdfs://cdh-master-slave1:8020/user/weiwc/data/t1.txt")
# lo = sc.parallelize(["123","好",u"好",1],3)
# loo = sc.parallelize(["123","好",u"好",2],2)

# 将多个RDD进行简单合并，不去重
# lor = sc.union([loo,lo])
# lor的分区数为lo和loo的分区之和。union是窄依赖，每个父子分区都是1:1，见：http://www.cnblogs.com/isenhome/p/5085872.html
# print lor.getNumPartitions()  #5
# print lor.collect()

# [u'a123 hadoop', u'a123 a123', u'a012 a123', u'b123 hive hadoop', u'Spark scala python',
# u'a123 hadoop', u'a123 a123', u'a012 a123', u'b123 hive hadoop', u'Spark scala python',
# '123', '\xe5\xa5\xbd', u'\u597d', 4]
# textFile从文件读取是字符串，无论是否包含汉字，前面都带u,这样读取的汉字才正确。parallelize中

# lo1 = sc.parallelize(["123","好",u"好",4])
# lo2 = sc.parallelize(["12345","好123",u"好",4])
# lo3 = sc.parallelize(["12345","12345",u"好",4])
# lo4 = sc.parallelize(["12345","12345",u"好",4])
# ['12345', u'\u597d', 4]

# lo5 = sc.parallelize(["12345","12345",u"好",4])
# lo6 = sc.parallelize(["12345","12345",u"好123",4,5,6])

# 求交集，去重
# print lo3.intersection(lo4).collect()
# print lo4.intersection(lo3).collect()

#求差集
# subtract(other, numPartitions=None)
# subtractByKey(other, numPartitions=None)
# 求在lo5却不在lo6的结果,Return each value in self that is not contained in other.
# print lo5.subtract(lo6).collect()

# rdd = sc.parallelize([1,2,3,4,5,11,12])
# rdd2 = sc.parallelize([1,2,3,4,5,6,7,8,9])
# print rdd.subtract(rdd2).collect()
# [11, 12]
# x = sc.parallelize([("a", 1), ("b", 4), ("b", 5), ("a", 2)])
# y = sc.parallelize([("a", 3), ("c", None)])
# sorted(x.subtractByKey(y).collect())
# [('b', 4), ('b', 5)]
# ============================================================

# combineByKey函数比较重要，我们熟悉地诸如aggregateByKey、foldByKey、reduceByKey
# 等函数都是基于该函数实现的。默认情况会在Map端进行组合操作。
# aggregateByKey执行流程，为何该方法会有两个方法作为参数？
# 因为该方法会先在map端进行聚合，即每个task对应的分区会先根据相同Key的聚合，聚合的结果类型和原来Value的类型不一定相同。
# 因此需要两个函数，seq在map端的一个分区内，comb针对多个分区中相同的Key进行聚合。
# 聚合函数，这里对应seq函数，过程是：
# 将初始值和每个分区相同key的第一个value传入seq函数，即x,y；返回一个值，该值得类型可能改变，即V=>U，不一定是传进的参数的类型。
# 接着将返回值和key的第二个value传入seq函数计算。结果返回（K,U），然后进行分区之间的聚合，相同Key的values进行聚合，相同Key的
# 前两个Value先作为x,y输入comb函数计算，返回结果，接着将返回值和第三个value，作为参数x,y输入comb函数，进行计算。如果相同的Key只有
# 一个Value，就不执行该方法，说明相同Key的记录在一个分区内，不存在分区间的聚合。
# a1 = sc.parallelize([1,1,2,2,3,3,1,1,2,2,4,5],3)
# print a1.glom().collect()
# def seq(x,y):
#     print x,y
#     return str(x) + str(y) + "a"
#
# def comb(x,y):
#     print type(x),type(y)
#     print x,y
#     return x+y
#
# print a1.map(lambda x:(x,1)).aggregateByKey(100,seq,comb).collect()
# ====================================================
# cartesian类似笛卡尔积，a.cartesian(b)返回结果是一个k,v类型的RDD，k是a中的每一个元素，v是b中的每一个元素
# b1 = sc.parallelize(["a","b",123])
# b2 = sc.parallelize(["c","d",123456])
# print b1.cartesian(b2).collect()
# =====================================================
# cache和checkpoint参考：
# https://github.com/JerryLead/SparkInternals/blob/master/markdown/6-CacheAndCheckpoint.md
# http://blog.csdn.net/ljp812184246/article/details/53897613
# checkpoint读写源码分析：
# http://blog.csdn.net/lw_ghy/article/details/51480701
# http://blog.csdn.net/lw_ghy/article/details/51480658
# 需要注意的几点：
# 1）setCheckpointDir必须指定HDSF目录。
# 2）cache是计算一条就持久化到内存一条，checkpoint并非如此，当应用程序中遇到且是第一个action结束时，
#   会再启动一个job执行这个action来进行checkpoint，即第一个action将被执行两次（有时也很耗时）。
# 3）可通过stage的DAG Visualization进行查看，是否读取了checkpoint的HDFS数据。ReliableCheckpointRDD [11]
# 4）setCheckpointDir目录中的数据，driver结束不会自动删除，需手动remove.
# 5)checkpoint将RDD序列化存到HDFS上，HDFS会自动备份，相比cache(),即使哪个node或task或partition挂了，也能保证快速的恢复，而不是重新计算。

# sc.setCheckpointDir("hdfs://cdh-master-slave1:8020/user/weiwc/data/07")
# c1= sc.parallelize(["q","w","e","r","t","a","w","e","r"],3)
# c1 = sc.textFile("hdfs://cdh-master-slave1:8020/user/weiwc/data/t1.txt")
# def t(x):
#     return (x,1)
# c2 = c1.map(t).groupByKey(3).map(lambda x:(x[0],1)).reduceByKey(lambda x,y:x+y)
#
# c2.checkpoint()
# print c2.count()
#
# print c2.collect()
#
# d1 = sc.parallelize([1,2])
# print c2.cartesian(d1).count()
# =======================================
# coalesce	英[ˌkəʊəˈles]
# 美[ˌkoʊəˈles]
# vi.	联合，合并;

# coalesce和repartition算子可以直接对RDD进行分区修改。coalesce减小分区不会产生Shuffle（例如1000=>100，父子分区比为n:1是窄依赖），
# 增大分区，必须设置为shuffle=true才生效，会产生Shuffle(父子分区比为1：n是宽依赖)。repartition内部其实调用了coalesce(num,true)，
# 因此增大减小分区都会产生Shuffle。

# sc.parallelize([1, 2, 3, 4, 5], 3).glom().collect()
# sc.parallelize([1, 2, 3, 4, 5], 3).coalesce(1).glom().collect()
# =======================================
# cogroup将两个RDD中同一个Key对应的Value组合到一起。python中不能传进多个RDD,scala中可以.
# groupWith(other, *others)功能和cogroup一样，但可以接收多个RDD。

# e1 = sc.parallelize([("a",1),("b",2),("c1",6),("a",3),("b",4)],4)
# e2 = sc.parallelize([("a",1),("b",2),("c",3),("d",4)],3)
# e3 = sc.parallelize([("a1",1),("b1",2),("c1",3)])
# def cog(x):
#     if x[0]:
#         print x[0] + "======="
#         d = 0               #计算每个相同的key中有多少个value
#         for v in x[1]:
#             for v1 in v:
#                 if v1:
#                     d +=1
#                     print v1
#         print d


# result = e1.cogroup(e2,3)   #这里不明确指定结果的分区数时，默认为e1和e2的分区数之和。
# print result.getNumPartitions()
# print result.glom().collect()
# result = e2.cogroup(e1)
# result.foreach(cog)
# [('a', (<pyspark.resultiterable.ResultIterable object at 0x0000000005BA2EF0>, <pyspark.resultiterable.ResultIterable object at 0x0000000005BA2DD8>)), ('d', (<pyspark.resultiterable.ResultIterable object at 0x0000000005BA2EB8>, <pyspark.resultiterable.ResultIterable object at 0x0000000005BA2BA8>)), ('c1', (<pyspark.resultiterable.ResultIterable object at 0x0000000005BA2D30>, <pyspark.resultiterable.ResultIterable object at 0x0000000005BA2C18>)), ('c', (<pyspark.resultiterable.ResultIterable object at 0x0000000005BA2C88>, <pyspark.resultiterable.ResultIterable object at 0x0000000005BA2B38>)), ('b', (<pyspark.resultiterable.ResultIterable object at 0x0000000005BA2BE0>, <pyspark.resultiterable.ResultIterable object at 0x0000000005BA2B00>))]

# print e1.groupWith(e2,e3).collect()
# ====================================================
# collectAsMap 返回dict给driver。有多个相同Key的话，只会保存一个。
# f1 = sc.parallelize([("a",1),("b",2),("c1",6),("a",3),("b",4)],4)
# print f1.collectAsMap()
# print f1.collectAsMap().get("a")
# {'a': 3, 'c1': 6, 'b': 4}
# ====================================
# http://blog.csdn.net/jiangpeng59/article/details/52538254
# g1 = sc.parallelize([("Fred", 88.0), ("Fred", 95.0), ("Fred", 91.0), ("Wilma", 93.0), ("Wilma", 95.0), ("Wilma", 98.0)],4)
# createCombiner, mergeValue, mergeCombiners, numPartitions=None,
# def createCombiner(x):
#     return (1,x)
#
# def mergeValue(x,y):
#     print x,y
#     return (x[0]+1,x[1] + y)
#
# def mergeCombiners(x,y):
#     print x,y
#     print type(x),type(y)
#     print (x[0] + y[0],x[1] + y[1])
#     return (x[0] + y[0],x[1] + y[1])
# print g1.glom().collect()
# print g1.combineByKey(createCombiner,mergeValue,mergeCombiners).mapValues(lambda x:x[1]/x[0]).countByKey().keys()

# countByValue(): Map[T, Long]，（V）型算子，返回的是Map,数据量大时使用rdd.map(x => (x, 1L)).reduceByKey(_ + _),
# countByKey(): Map[K, Long] ，（K,V）型算子，返回的是Map,数据量大时使用rdd.mapValues(_ => 1L).reduceByKey(_ + _)代替！

#sorted 对iter排序
# print sorted(sc.parallelize([1, 2, 1, 2, 2], 2).countByValue().items(),reverse=False) #默认升序
# print sorted(sc.parallelize([1, 1, 2, 3]).distinct().collect(),reverse=True)        #reverse=True降序

#flatMapValues(f)
# x = sc.parallelize([("a", ["x", "y", "z"]), ("b", ["p", "r"])])
# def f(x): return x
# print sorted(x.flatMapValues(f).collect())


# 在combineByKey()中在 map 端开启 combine()，因此，reduceyByKey() 默认也在 map 端开启 combine()，
# 这样在 shuffle 之前先通过 mapPartitions 操作进行 combine，得到 MapPartitionsRDD， 然后 shuffle
# 得到 ShuffledRDD，再进行 reduce（通过 aggregate + mapPartitions() 操作来实现）得到 MapPartitionsRDD。

#foldByKey： http://blog.csdn.net/a6210575/article/details/52260326
#reduce(f)、fold(zeroValue, op)、aggregate ：  http://lxw1234.com/archives/2015/07/394.htm

# reduce(f)，fold(zeroValue, op)，以及aggregate(zeroValue, seqOp, combOp)：
# reduce(f)，fold(zeroValue, op)不可改变数据的类型，aggregate接受两个函数，可改变数据的类型。aggregate的两个函数一样时就类似fold的功能了！
# 注意：fold和aggregate的初始值既在map端又在reduce端使用！

# foldByKey: 基于combineByKey实现，因此也先在map端的聚合，即每个分区中的相同的Key先使用初始值聚合，
# 之后将所有分区中的相同Key聚合。注意：这里的初始值只在map端使用，不再在reduce端使用！

from operator import add
# print sc.parallelize([1, 2, 3, 4, 5],2).reduce(add)       #结果15
# print sc.parallelize([1, 2, 3, 4, 5],3).reduce(add)       #结果15
# print sc.parallelize([1, 2, 3, 4, 5],3).fold(2, add)       #结果23,3个map端，1个reduce端，15+4*2
# print sc.parallelize([1, 2, 3, 4, 5],4).fold(2, add)       #结果25,4个map端，1个reduce端，15+5*2
# def seqOp(x,y):
#     return x+y
# def combOp(x,y):
#     return x+y
# print sc.parallelize([1, 2, 3, 4, 5],2).aggregate(2,seqOp,combOp)
# print sc.parallelize([1, 2, 3, 4, 5],3).aggregate(2,seqOp,combOp)
# print sc.parallelize([1, 2, 3, 4, 5],4).aggregate(2,seqOp,combOp)

# rdd = sc.parallelize([("a", 1), ("b", 1), ("a", 1),("a", 1)],3)
# print rdd.glom().collect()
# print sorted(rdd.foldByKey(1,add).collect())

# getStorageLevel
# rdd_storage_level = sc.parallelize([("a", 1), ("b", 1), ("a", 1),("a", 1)],3)
# rdd_storage_level.getStorageLevel()

# join、leftOuterJoin、rightOuterJoin和fullOuterJoin

# pairRDD1 = sc.parallelize([("cat",2), ("cat", 5), ("book", 4),("cat", 12)])
# pairRDD2 = sc.parallelize([("cat",2), ("cup", 5), ("mouse", 4),("cat", 12)])
# pairRDD1 = sc.parallelize([("cat",2), ("cat", 5), ("book", 4),("cat", 12)]).groupByKey().mapValues(lambda x:list(x))
# pairRDD2 = sc.parallelize([("cat",2), ("cup", 5), ("mouse", 4),("cat", 12)]).groupByKey().mapValues(lambda x:list(x))

# def p(t):
#     print type(t)
#     print type(t[0])
#     print type(t[1])
# print sc.parallelize([("cat",2), ("cup", 5), ("mouse", 4),("cat", 12)]).groupByKey().foreach(p)
# <type 'tuple'>
# <type 'str'>
# <class 'pyspark.resultiterable.ResultIterable'>

# print pairRDD1.leftOuterJoin(pairRDD2).collect()
# print pairRDD1.rightOuterJoin(pairRDD2).collect()
# print pairRDD1.fullOuterJoin(pairRDD2).collect()

# join的结果： 是一个(k, (v1, v2)) tuple, where (k, v1) is in self and (k, v2) is in other.
# print pairRDD1.join(pairRDD2).collect()
# 使用map+broadcast代替join，避免shuffle过程
#。。。

# groupBy
# rdd = sc.parallelize([1, 1, 2, 3, 5, 8])
# result = rdd.groupBy(lambda x: x % 2).collect()
# print sorted([(x, sorted(y)) for (x, y) in result])

#求交集：intersection,rdd1.intersection(rdd2)
# 是否为空：isEmpty()
# re1 = sc.parallelize([])
# print re1.getNumPartitions()
# print re1.isEmpty()
# re2 = sc.parallelize([1])
# print re2.getNumPartitions()
# print re2.isEmpty()


# keyBy(f), 为RDD(v)生成k,返回RDD(k,v)
# keys(),返回RDD(k,v)中的k,结果为RDD(v)
# lookup(key),  lookup用于(K,V)类型的RDD,指定K值，返回RDD中该K对应的所有V值。

# rdd = sc.parallelize([1, 1, 2, 3, 5, 8]).keyBy(lambda x: x*x)
# print rdd.collect()
# print rdd.keys().collect()

# rdd2 = sc.parallelize([("cat",2), ("cat", 5), ("book", 4),("cat", 12)])
# print rdd2.lookup('cat')        # [2, 5, 12]
# ===================================

# mapPartitions(f, preservesPartitioning=False)
# mapPartitionsWithIndex(f, preservesPartitioning=False)
# 总结：一般mapPartitions\mapPartitionsWithIndex算子中的函数返回一般的数据时(包括字符串、整型)，类似字符串等（像{}、[]、True的对象也可使用return）必须使用yield，
# 而需要结束程序时用return，否则return返回整型会报错 或 return返回的字符串会被拆分。

# len、sum等函数可以直接用于mapValues()中。但是用在mapPartitions和mapPartitionsWithIndex
# 中就必须使用def f(iterator): yield sum(iterator)这种方式，将结果通过yield返回！否则报错如下：
# TypeError: 'int' object is not iterable

# rdd = sc.parallelize([1, 2, 2, 3, 3, 4], 2)
# def f(iterator): yield sum(iterator)
# print rdd.mapPartitions(f).collect()          # [3, 7]
# print rdd.map(lambda x:(x,2)).groupByKey().mapValues(len).collect()
# print rdd.map(lambda x:(x,2)).groupByKey().mapValues(sum).collect()
# ================================

# rdd = sc.parallelize([1, 2, 3, 4], 3)
# rdd2 = sc.parallelize([1, 2, 3, 4, 5, 6], 2)
# def f(iterator):
#     yield sum(iterator)
#
# def f0(iterator):
#     return sum(iterator)
#
# def f1(index,iterator):
#     d = 0
#     for v in iterator:
#         d+= v
#     return d
#
# def f2(index,iterator):
#     d = 0
#     for v in iterator:
#         d+= v
#     yield d
#
# def f3(index,iterator):
#     d = 0
#     for v in iterator:
#         d+= v
#     return str(d)
# def f4(index,iterator):
#     d = 0
#     for v in iterator:
#         d+= v
#     yield str(d)
# def p(x):
#     print type(x)
#     print x

# print rdd.glom().collect()
# print rdd2.glom().collect()
# print rdd.mapPartitions(f).collect()
# print rdd.mapPartitions(f0).collect()             #TypeError: 'int' object is not iterable
# rdd2.mapPartitionsWithIndex(f1).foreach(p)          #TypeError: 'int' object is not iterable
# rdd2.mapPartitionsWithIndex(f2).foreach(p)
# rdd2.mapPartitionsWithIndex(f3).foreach(p)          #没有报错，但结果不对，return str(d)返回的6,15没有组装成对象，在foreach中被分开为6,1,5。
# <type 'str'>
# 1
# <type 'str'>
# 5
# <type 'str'>
# 6
# print rdd2.mapPartitionsWithIndex(lambda x,y:str(sum(y))).collect() #与上面一个使用f3一样的道理
# ['6', '1', '5']
# print rdd2.mapPartitionsWithIndex(f4).collect()
# ['6', '15']
# ==========================================
# max(key=None)
# min(key=None)
# sum()
# mean()
# rdd = sc.parallelize([2.0,5.0, 43.0, 10.0])
# print rdd.max()
# print rdd.max(key=str)
# print rdd.min()
# print rdd.min(key=str)
# print rdd.sum()
# 43.0
# 5.0
# 2.0
# 10.0
# 60.0
# ===========================
# 管道操作： pipe(command, env=None, checkCode=False)
# 作用：可以调用第三方的程序来处理数据，比如Linux脚本文件

# print sc.parallelize(['1', '2', '', '3']).pipe('cat').collect()
# ==============================
# reduceByKeyLocally(func):在reduceByKey计算之后，将所有结果返回到driver，组合为字典！
# from operator import add
# rdd = sc.parallelize([("a", 1), ("b", 1), ("a", 1)])
# print rdd.reduceByKeyLocally(add).items()
# ============================

# repartitionAndSortWithinPartitions(numPartitions=None, partitionFunc=<function portable_hash at 0x7fa664f3cb90>, ascending=True, keyfunc=<function <lambda> at 0x7fa665048b90>)
# 分区后的每个分区中的结果，按Key排序！
# rdd = sc.parallelize([(0, 5), (3, 8), (2, 6), (0, 8), (3, 8), (1, 3)])
# rdd2 = rdd.repartitionAndSortWithinPartitions(2, lambda x: x % 2)
# print rdd2.glom().collect()
# [[(0, 5), (0, 8), (2, 6)], [(1, 3), (3, 8), (3, 8)]]
# ==================================
# sample(withReplacement, fraction, seed=None)
# sampleByKey(withReplacement, fractions, seed=None)，返回约等于fractions大小的样本
# takeSample(withReplacement, num, seed=None),返回指定固定大小的样本，指定的大小大于RDD元素个数时，返回全部。

# rdd = sc.parallelize([1,2,3,4,5,6,7,8,9,10])
# print rdd.sample(True,0.7,8).collect()         #结果有重复
# print rdd.sample(False,0.3,8).collect()         #结果无重复
# print len(rdd.takeSample(False, 5, 1))        #5
# print len(rdd.takeSample(False, 20, 1))        #10

# =========================
# sortBy(keyfunc, ascending=True, numPartitions=None)
# sortByKey(ascending=True, numPartitions=None, keyfunc=<function <lambda> at 0x7fa665048c80>)

# tmp = [('a', 1), ('b', 2), ('1', 3), ('d', 4), ('2', 5)]
# sc.parallelize(tmp).sortBy(lambda x: x[0]).collect()
# sc.parallelize(tmp).sortBy(lambda x: x[1]).collect()
# sc.parallelize(tmp).sortByKey().first()
# sc.parallelize(tmp).sortByKey(True, 1).collect()

# takeOrdered(num, key=None):按元素升序，或按照作用于key的函数
# rdd2 = sc.parallelize([10, 1, 2, 9, 3, 4, 5, 6, 7])
# print rdd2
# .takeOrdered(6)   #[1, 2, 3, 4, 5, 6]
# print rdd2.takeOrdered(6,key=lambda x: -x)  #[10, 9, 7, 6, 5, 4]
# =================
# top(num, key=None):内部将元素先降序排序，再取前n个。
# print sc.parallelize([2, 3, 4, 5, 6], 2).top(2)
# [6, 5]
# print sc.parallelize([10, 4, 2, 12, 3]).top(3, key=str)
# [4, 3, 2]
# ================================================================
# values()
# zip(other),使用时两个RDD的分区和每个分区内的元素个数必须相等！
# zipWithIndex()
# partitionBy(numPartitions, partitionFunc),是一个RDD(K,V)类型的算子。key一样的话，肯定会被分到同一个分区。

# def p(x): print x
# x = sc.parallelize([1,2,3,4,5,6]).map(lambda x: (x,x)).partitionBy(2)
# y = sc.parallelize([1,2,3,4,5,6]).map(lambda x: (x,x)).partitionBy(2)
# z = sc.parallelize([1,2,3,4,5,6],4)
# print x.values().collect()
# print x.getNumPartitions()
# print x.glom().collect()
# print y.glom().collect()
# print x.zip(y).collect()
# print z.zipWithIndex().collect()
#
# [2, 4, 6, 1, 3, 5]
# 2
# [[(2, 2), (4, 4), (6, 6)], [(1, 1), (3, 3), (5, 5)]]
# [[(2, 2), (4, 4), (6, 6)], [(1, 1), (3, 3), (5, 5)]]
# [((2, 2), (2, 2)), ((4, 4), (4, 4)), ((6, 6), (6, 6)), ((1, 1), (1, 1)), ((3, 3), (3, 3)), ((5, 5), (5, 5))]
# [(1, 0), (2, 1), (3, 2), (4, 3), (5, 4), (6, 5)]
# ====================================================================