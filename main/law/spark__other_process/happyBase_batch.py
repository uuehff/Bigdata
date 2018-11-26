# -*- coding: utf-8 -*-

import happybase
import json
import logging

import time

print time.asctime( time.localtime(time.time()) )

conn = happybase.Connection(host='cdh-slave1',port=9090,timeout=7200000)
t = conn.table('laws_doc:judgment_all')
# t_batch = t.batch()

# batch理解：batch只能以table.batch()这种方式创建，其中有put,delete,send方法，使用table的put，delete操作时，每一个
# put 或delete都会立刻向thrift server发一个请求，比如在一个循环里执行put，delete，那请求次数太频繁，且效率不高。
# 可以使用table.batch()创建一个表的batch对象，使用它的put,delete操作，然后执行send()，将操作发送到hbase thrift server。

# 三种情况下才会真正执行put,delete操作：
# 1）使用with t.batch() as b:创建batch对象，在下面执行put,delete操作时，当with语句执行完，会自动调用send()。
# 比如：
# with t.batch() as b:
#     b.put(b'row-key-1', {b'cf:col1': b'value1', b'cf:col2': b'value2'})
#     b.put(b'row-key-2', {b'cf:col2': b'value2', b'cf:col3': b'value3'})
#     b.put(b'row-key-3', {b'cf:col3': b'value3', b'cf:col4': b'value4'})
#     b.delete(b'row-key-4')

# 2） 不使用with创建batch对象，手动调用batch.send()方法，例如：
# b = t.batch()
# for i in range(1200):
#     b.put(b'row-%04d' % i, {
#         b'cf1:col1': b'v1',
#         b'cf1:col2': b'v2',
#     })
# b.send()

# 如果with代码块中包含很多的put，delete请求，在with语句默认最后一次性提交（或不使用with方式创建的batch，t.batch()创建batch方式时，
# 但for循环最后手动send提交）的数据会很大，因此可以设置：batch_size=1000，当put或delete次数等于batch_size时，也会触发提交（send）,
# 通过batch_size的大小控制分批发送操作。就是下面第三种方法。
# 3）在使用t.batch(batch_size=1000)，其中指定batch_size大小时，当put或delete次数等于batch_size时，就会自动发送操作到hbase thrit server!

# with t.batch(batch_size=1000) as b:  #或 b =t.batch(batch_size=1000)
#     for i in range(1200):
#         # this put() will result in two mutations (two cells)
#         #batch_size=1000,batch_size的意思是指以一个单元格为单位，也即是一个字段的put，delete就相当于batch_size=1。
#         #下面的put操作，一次put就插入两个字段的值（cf1:col1，cf1:col2），涉及两个单元格,两个字段，因此对应的batch_size值为2。
#         #基于batch_size=1000，1200次循环，一次循环中的put操作,插入两个字段的值，因此，循环1200次会有2400个字段值的插入，而batch_size=1000，
#          因此会产生三个batch，发送三次，第一个batch有1000个插入，第二个batch有1000个插入，第三个batch有400个插入。
#         # 换句话说,i为499时发送一次，999时发送一次，1199时发送一次！
#         b.put(b'row-%04d' % i, {
#             b'cf1:col1': b'v1',
#             b'cf1:col2': b'v2',
#         })

#with语句中产生的batch对象，transaction=True是开启了事务的，在with语句执行结束前，with中有报错，
# 则该batch中的数据都不会提交到服务器在执行。
# try:
#     with t.batch(transaction=True) as b:
#         b.put(b'row-key-1', {b'cf:col1': b'value1', b'cf:col2': b'value2'})
#         b.put(b'row-key-2', {b'cf:col2': b'value2', b'cf:col3': b'value3'})
#         b.put(b'row-key-3', {b'cf:col3': b'value3', b'cf:col4': b'value4'})
#         b.delete(b'row-key-4')
#         raise ValueError("Something went wrong!")
# except ValueError:
#     # error handling goes here; nothing is sent to HBase
#     pass


q = t.scan(filter="QualifierFilter(=, 'binary:id') AND KeyOnlyFilter()")  #过滤id字段，且只保留key
# q = t.scan(limit=20)


#  hbaseFor example, this will result in three round-trips to the server (two batches with 1000 cells, and one with the remaining 400):
# with table.batch(batch_size=1000) as b:
#     for i in range(1200):
#         # this put() will result in two mutations (two cells)
#         b.put(b'row-%04d' % i, {
#             b'cf1:col1': b'v1',
#             b'cf1:col2': b'v2',
#         })

try:
    # t_batch添加的操作达到10000个时，会自动执行send，发送命令到服务器端，执行到with语句结束，不足10000个操作，
    # 也会自动调用send，因为是基于with语句创建的t_batch的上下文管理器。
    with t.batch(batch_size=10000) as t_batch: #这句是经典的语句，一般都这样使用，with加batch_size。
        for k,vs in q:
            # t_batch.delete(k,['d:org_plaintiff','d:org_defendant','d:plaintiff_judge_result','d:defendant_judge_result'])
            t_batch.delete(k,['d:org_plaintiff','d:org_defendant'])

        raise ValueError("Something went wrong!")   #此句写在with语句的代码块里，抛出异常，except截获，不要写在for循环里，否则循环直接结束。
except ValueError:
    pass
finally:
    # print d
    pass

print time.asctime( time.localtime(time.time()) )
