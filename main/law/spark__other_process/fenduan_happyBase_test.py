# -*- coding: utf-8 -*-

import happybase

conn = happybase.Connection(host='cdh-slave1',port=9090)
t = conn.table('laws_doc:zhangye_xingshi_join')
# q = t.scan(row_prefix="18983fe0-f5dd-4990-9aa9-a8b300d00360")  #满月酒截断
q = t.scan(row_prefix="4611bcbb-f5c2-4970-9ceb-a8a1009cda29")  #满月酒截断
for k,vs in q:
    print k,vs['d:id']
    for k1 in vs.keys():
        print k1 , vs[k1]
