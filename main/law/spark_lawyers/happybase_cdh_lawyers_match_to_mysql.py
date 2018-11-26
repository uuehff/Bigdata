# -*- coding: utf-8 -*-

import happybase
import logging
import time

import pymysql
logger = logging.getLogger(__name__)

conn = happybase.Connection(host='cdh5-slave2',port=9090,timeout=7200000)
t = conn.table('cdh:lawyers_match')
# t = conn.table('cdh:lawyers_add')

print time.asctime( time.localtime(time.time()) )
#读取judgment_all一万条，写入judgment_all_1w来测试
q = t.scan()

# id,uuid,party_info,trial_process,trial_request,court_find,court_idea,judge_result,doc_footer,\
# caseid,title,court,court_uid,lawlist,law_id,\
# casedate,reason_type,type,judge_type,reason,reason_uid,province,plt_claim,dft_rep,crs_exm

try:
    conn = pymysql.connect(host='cdh5-slave2', user='weiwc', passwd='HHly2017.', db='laws_doc_lawyers_new', charset='utf8')
    cursor = conn.cursor()
    for k, v in q:
        # print k,v
        # data = {}
        # for k1 in v.keys():
            # data.update({k1:v[k1]})
        sql2 = " insert into hht_lawyer_all_collect_match " \
               "(name,pra_number,org_name,age,area,birth_date,biyexueyuan,city,edu_origin,first_pra_time,gender,id_num," \
               "mail,nation,org_identity,phone,politics,practicestatus,pra_course,pra_type,province,qua_number,qua_time," \
               "xuewei,zhuanye) " \
               "values (%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s)"
        # id','d:uuid','d:party_info','d:trial_process','d:trial_request','d:court_find','d:court_idea','d:judge_result',
        # 'd:doc_footer','d:caseid','d:title','d:court','d:court_uid','d:lawlist','d:law_id','d:casedate',
        # 'd:reason_type','d:type','d:judge_type','d:reason','d:reason_uid','d:province','d:plt_claim','d:dft_rep','d:crs_exm
        cursor.execute(sql2,
                       (v.get('d:name',''),v.get('d:pra_number',''),v.get('d:org_name',''),v.get('d:age',''),v.get('d:area',''),v.get('d:birth_date',''),v.get('d:biyexueyuan',''),v.get('d:city',''),
                        v.get('d:edu_origin', ''), v.get('d:first_pra_time', ''),v.get('d:gender',''),v.get('d:id_num',''),v.get('d:mail',''),v.get('d:nation',''),
                        v.get('d:org_identity',''),v.get('d:phone',''),v.get('d:politics', ''), v.get('d:practicestatus', ''),v.get('d:pra_course',''),v.get('d:pra_type',''),
                        v.get('d:province',''),v.get('d:qua_number',''),v.get('d:qua_time',''),v.get('d:xuewei',''),
                        v.get('d:zhuanye', '')))
    conn.commit()
    cursor.close()
    conn.close()
    print time.asctime(time.localtime(time.time()))

    raise ValueError("Something went wrong!")  #此句写在with语句的代码块里，抛出异常，except截获，不要写在for循环里，否则循环直接结束。
except ValueError:
    pass
finally:
    print time.asctime( time.localtime(time.time()) )

