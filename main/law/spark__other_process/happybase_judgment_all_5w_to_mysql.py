# -*- coding: utf-8 -*-

import happybase
import logging
import time

import pymysql
logger = logging.getLogger(__name__)

conn = happybase.Connection(host='cdh-slave1',port=9090,timeout=7200000)
t = conn.table('laws_doc:judgment_administration_all')
# t2 = conn.table('laws_doc:judgment_all_1w')

print time.asctime( time.localtime(time.time()) )
#读取judgment_all一万条，写入judgment_all_1w来测试
q = t.scan(limit=50000)

# id,uuid,party_info,trial_process,trial_request,court_find,court_idea,judge_result,doc_footer,\
# caseid,title,court,court_uid,lawlist,law_id,\
# casedate,reason_type,type,judge_type,reason,reason_uid,province,plt_claim,dft_rep,crs_exm

try:
    conn = pymysql.connect(host='cdh-slave1', user='weiwc', passwd='HHly2017.', db='laws_doc_administration', charset='utf8')
    cursor = conn.cursor()
    for k, v in q:
        # print k,v
        # data = {}
        # for k1 in v.keys():
            # data.update({k1:v[k1]})
        sql2 = " insert into administration_etl_5w (id,uuid,party_info,trial_process,trial_request,court_find,court_idea,judge_result,doc_footer,caseid,title,court,court_uid,lawlist,law_id,casedate,reason_type,type,judge_type,reason,reason_uid,province,plt_claim,dft_rep,crs_exm) " \
               "values (%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s)"
        # id','d:uuid','d:party_info','d:trial_process','d:trial_request','d:court_find','d:court_idea','d:judge_result',
        # 'd:doc_footer','d:caseid','d:title','d:court','d:court_uid','d:lawlist','d:law_id','d:casedate',
        # 'd:reason_type','d:type','d:judge_type','d:reason','d:reason_uid','d:province','d:plt_claim','d:dft_rep','d:crs_exm
        cursor.execute(sql2, (v.get('d:id',''),v.get('d:uuid',''),v.get('d:party_info',''),v.get('d:trial_process',''),v.get('d:trial_request',''),v.get('d:court_find',''),v.get('d:court_idea',''),v.get('d:judge_result',''),
                              v.get('d:doc_footer', ''), v.get('d:caseid', ''),v.get('d:title',''),v.get('d:court',''),v.get('d:court_uid',''),v.get('d:lawlist',''),v.get('d:law_id',''),v.get('d:casedate',''),
                              v.get('d:reason_type', ''), v.get('d:type', ''),v.get('d:judge_type',''),v.get('d:reason',''),v.get('d:reason_uid',''),v.get('d:province',''),v.get('d:plt_claim',''),v.get('d:dft_rep',''),
                              v.get('d:crs_exm', '')))
    conn.commit()
    cursor.close()
    conn.close()
    print time.asctime(time.localtime(time.time()))

    raise ValueError("Something went wrong!")  #此句写在with语句的代码块里，抛出异常，except截获，不要写在for循环里，否则循环直接结束。
except ValueError:
    pass
finally:
    print time.asctime( time.localtime(time.time()) )

