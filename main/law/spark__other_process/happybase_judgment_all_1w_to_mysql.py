# -*- coding: utf-8 -*-

import happybase
import logging
import time

import pymysql
logger = logging.getLogger(__name__)

conn = happybase.Connection(host='cdh5-master-slave1',port=9090,timeout=7200000)
t = conn.table('laws_doc:judgment_implement_all')
# laws_doc:judgment_administration_all
# laws_doc:judgment_all
# laws_doc:judgment_civil_all
# laws_doc:judgment_implement_all


print time.asctime( time.localtime(time.time()) )
#读取judgment_all一万条，写入judgment_all_1w来测试
q = t.scan(limit=2500)

try:
    conn = pymysql.connect(host='cdh5-slave2', user='weiwc', passwd='HHly2017.', db='laws_doc_administration', charset='utf8')
    cursor = conn.cursor()
    for k, v in q:
        # print k,v
        # data = {}
        # for k1 in v.keys():
            # data.update({k1:v[k1]})
        # id, uuid, party_info, trial_process, trial_request, court_find, court_idea, judge_result,\
        # doc_footer, court, caseid, uuid, title, lawlist, reason_type, type, judge_type,\
        # law_id, reason, reason_uid, casedate, province, court_uid,\
        # judge, court_cate, plaintiff_id, defendant_id, lawyer_id, law_office, lawyer,
        try:

            sql2 = " insert into administration_etl_1w (uuid,uuid_old,party_info,trial_process,trial_request,court_find,court_idea,judge_result,doc_footer,caseid,title,court,court_uid,lawlist,law_id,casedate,reason_type,type,judge_type,reason,reason_uid,province,judge,court_cate,plaintiff_id, defendant_id, lawyer_id, law_office, lawyer) values (%s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s,%s, %s, %s,%s,%s)"
        # id','d:uuid','d:party_info','d:trial_process','d:trial_request','d:court_find','d:court_idea','d:judge_result',
        # 'd:doc_footer','d:caseid','d:title','d:court','d:court_uid','d:lawlist','d:law_id','d:casedate',
        # 'd:reason_type','d:type','d:judge_type','d:reason','d:reason_uid','d:province','d:plt_claim','d:dft_rep','d:crs_exm
        # cursor.execute(sql2, (v.get('d:uuid',''),v.get('d:uuid_old',''),v.get('d:party_info',''),v.get('d:trial_process',''),v.get('d:trial_request',''),v.get('d:court_find',''),v.get('d:court_idea',''),v.get('d:judge_result',''),v.get('d:doc_footer', ''), v.get('d:caseid', ''),v.get('d:title',''),v.get('d:court',''),v.get('d:court_uid',''),v.get('d:lawlist123',''),v.get('d:law_id',''),v.get('d:casedate',''),v.get('d:reason_type', ''), v.get('d:type', ''),v.get('d:judge_type',''),v.get('d:reason',''),v.get('d:reason_uid',''),v.get('d:province',''),v.get('d:judge',''),v.get('d:court_cate',''),v.get('d:plaintiff_id', ''),v.get('d:defendant_id',''),v.get('d:lawyer_id',''),v.get('d:law_office',''),v.get('d:lawyer','')))
            cursor.execute(sql2, (k,v.get('d:uuid_old',''),v.get('d:party_info',''),v.get('d:trial_process',''),v.get('d:trial_request',''),v.get('d:court_find',''),v.get('d:court_idea',''),v.get('d:judge_result',''),v.get('d:doc_footer', ''), v.get('d:caseid', ''),v.get('d:title',''),v.get('d:court',''),v.get('d:court_uid',''),v.get('d:lawlist',''),v.get('d:law_id',''),v.get('d:casedate',''),v.get('d:reason_type', ''), v.get('d:type', ''),v.get('d:judge_type',''),v.get('d:reason',''),v.get('d:reason_uid',''),v.get('d:province',''),v.get('d:judge',''),v.get('d:court_cate',''),v.get('d:plaintiff_id', ''),v.get('d:defendant_id',''),v.get('d:lawyer_id',''),v.get('d:law_office',''),v.get('d:lawyer','')))
        #     print k
        except:
            print "error======uuid =======+++" + v.get('d:uuid', '') + "+++===============" + k

    conn.commit()
    cursor.close()
    conn.close()
    print time.asctime(time.localtime(time.time()))

    # raise ValueError("Something went wrong!")  #此句写在with语句的代码块里，抛出异常，except截获，不要写在for循环里，否则循环直接结束。
except ValueError:
    print "error+++++++++++++++++++++++++++++++++++++" + v.get('d:uuid','')
finally:
    print time.asctime( time.localtime(time.time()) )

