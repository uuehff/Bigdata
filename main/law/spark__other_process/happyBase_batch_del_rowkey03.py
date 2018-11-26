# -*- coding: utf-8 -*-

import happybase
import time
print time.asctime( time.localtime(time.time()) )

import pymysql

conn = happybase.Connection(host='cdh5-slave2')
t = conn.table('laws_doc:judgment_civil_all')


conn=pymysql.connect(host='cdh5-slave3',user='weiwc',passwd='HHly2017.',db='laws_doc_civil',charset='utf8')
cursor = conn.cursor()

#分批次读取mysql进行删除
for i in range(0,391):
    sql = 'select uuid from uuid_old where id > ' + str(i*40000) + ' and id <= ' + str((i+1)*40000)   #LOCATE函数，包含||,返回大于0的数值。
    cursor.execute(sql)
    row_2 = cursor.fetchall()


    # q = t.scan(filter="QualifierFilter(=, 'binary:uuid') AND KeyOnlyFilter()")  #过滤id字段，且只保留key
    try:
        # t_batch添加的操作达到10000个时，会自动执行send，发送命令到服务器端，执行到with语句结束，不足10000个操作，
        # 也会自动调用send，因为是基于with语句创建的t_batch的上下文管理器。
        with t.batch(batch_size=10000) as t_batch: #这句是经典的语句，一般都这样使用，with加batch_size。
            for row in row_2:
                t_batch.delete(row[0])
                # print row[0]
                # sql2 = " insert into casedate_validate (id,uuid,casedate) values (%s, %s, %s)"
                # cursor.execute(sql2, (row[0], row[1], row[2]))
                # for k,vs in q:
                # t_batch.delete(k,['d:org_plaintiff','d:org_defendant','d:plaintiff_judge_result','d:defendant_judge_result'])

            # raise ValueError("Something went wrong!")   #此句写在with语句的代码块里，抛出异常，except截获，不要写在for循环里，否则循环直接结束。
    except ValueError:
        pass
    finally:
        pass
    print sql
    print time.asctime( time.localtime(time.time()) )
conn.commit()
cursor.close()
conn.close()
print time.asctime( time.localtime(time.time()) )
