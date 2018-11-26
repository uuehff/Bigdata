# -*- coding: utf-8 -*-
import happybase
import time


if __name__ == '__main__':

    print time.time()
    conn = happybase.Connection(host='cdh-slave1', port=9090, timeout=7200000)
    t = conn.table('laws_doc:law_rule_result2')
    # q = t.scan(filter="QualifierFilter(=, 'binary:uuid') AND KeyOnlyFilter()")
    # try:
    #     for k, v in q:
    # t.delete(k,['d:if_adult','d:law_office','d:crime_reason','d:doc_oriligigation_new','d:defendant_new','d:plaintiff_new','d:judge_member_new'])
    # t.delete(b'581e8e1454d07a046868bfe6')
    # finally:
    #     print time.time()
    print t.row('5707',['d:uuids','d:art_num'])