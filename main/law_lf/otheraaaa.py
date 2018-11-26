# encoding:utf-8
import MySQLdb
import re
import util_n
import json
con = MySQLdb.connect(host='192.168.12.34', user='liuf', passwd='123456', db='laws_doc', charset='utf8')
cursor = con.cursor()
# sql = 'select uuid, casedate, type, reason, fact_finder, judge_member, judge_result, doc_oriligigation, is_format, id from judgment where uuid=a78dd0af-987b-4dd3-868b-f76356a97abd'
sql = 'select uuid, casedate, type, reason, fact_finder, judge_member, judge_result, doc_oriligigation, is_format, id from judg2 ' \
      'where is_format=1'

cursor.execute(sql)
row = cursor.fetchall()

def to_list(line):
    list_new = []
    if line!='' and line!='None':
        if '||' in line:
            list = line.split('||')
            for i in list:
                if i!='':
                    list_new.append(i)
        else:
            list_new.append(line)
    return list_new

def punishcate(judge_result):
    control_result = re.search(u'(拘役)', judge_result)
    lock_result = re.search(u'(管制)', judge_result)
    punish_date_result = re.search(u'(有期徒刑|徒刑)', judge_result)
    unlimited_date_result = re.search(u'(无期徒刑)', judge_result)
    death_result = re.search(u'(死刑)', judge_result)
    if death_result:
        punish_cate = u'死刑'
    elif unlimited_date_result:
        punish_cate = u'无期徒刑'
    elif punish_date_result:
        punish_cate = u'有期徒刑'
    elif control_result:
        punish_cate = u'拘役'
    elif lock_result:
        punish_cate = u'管制'
    else:
        punish_cate = ''
    return punish_cate

def punishdate(judge_result):
    punish_date = ''
    punish_date_search = re.search(u'(?<=有期徒刑)\d+(?:年|个月)|((?<=有期徒刑)[\u4e00-\u9fa5]{1,6}(?:年|个月))', judge_result.replace('\n',''))
    if punish_date_search:
        punish_date = str(util_n.as_date_date(punish_date_search.group(0)))
        if re.search(r'\d', punish_date_search.group(0)) and u'年' in punish_date_search.group(0):
            num = filter(str.isdigit, punish_date_search.group(0).encode('gbk'))
            punish_date = str(int(num) * 12)
        elif re.search(r'\d', punish_date_search.group(0)) and u'个月' in punish_date_search.group(0):
            num = filter(str.isdigit, punish_date_search.group(0).encode('gbk'))
            punish_date = str(int(num))
        elif u'半年' in punish_date_search.group(0):
            punish_date = str(6)
        elif u'年十个月' in punish_date_search.group(0):
            punish_date = str(10)
        elif u'年十年' in punish_date_search.group(0):
            punish_date = str(120)
    return punish_date

def delaydate(judge_result):
    delay_date = ''
    delay_date_search = re.search(u'((?<=缓刑)\d+(?:年|个月))|((?<=缓刑)[\u4e00-\u9fa5]{1,7}?(?:年|个月))',
                                  judge_result.replace('\n', ''))
    if delay_date_search:
        delay_date = str(util_n.as_date_delay(delay_date_search.group(0)))
        if re.search(r'\d', delay_date_search.group(0)) and u'年' in delay_date_search.group(0):
            num = filter(str.isdigit, delay_date_search.group(0).encode('gbk'))
            delay_date = str(int(num) * 12)
        elif re.search(r'\d', delay_date_search.group(0)) and u'个月' in delay_date_search.group(0):
            num = filter(str.isdigit, delay_date_search.group(0).encode('gbk'))
            delay_date = str(int(num))
        elif u'半年' in delay_date_search.group(0):
            delay_date = str(6)
    return delay_date
# 拘役
def controldate(judge_result):
    control_date = ''
    control_date_search = re.search(u'((?<=拘役)\d+(?:月|年))|((?<=拘役)[\u4e00-\u9fa5]{1,3}?(?:月|年))',judge_result.replace('\n', ''))
    if control_date_search:
        control_date=util_n.as_date_delay(control_date_search.group(0))
        if re.search(r'\d', control_date_search.group(0)) and u'个月' in control_date_search.group(0):
            num = filter(str.isdigit, control_date_search.group(0).encode('gbk'))
            control_date = str(int(num))
        elif u'一个半月' in control_date_search.group(0):
            control_date = str(1.5)
        elif u'二个半月' in control_date_search.group(0):
            control_date = str(2.5)
        elif u'三个半月' in control_date_search.group(0):
            control_date = str(3.5)
        elif u'四个半月' in control_date_search.group(0):
            control_date = str(4.5)
        elif u'五个半月' in control_date_search.group(0):
            control_date = str(5.5)
    return control_date
# 管制
def lockdate(judge_result):
    lock_date = ''
    lock_date_search = re.search(u'((?<=管制)\d+(?:年|个月))|((?<=管制)[\u4e00-\u9fa5]{1,5}?(?:年|个月))',judge_result.replace('\n', ''))
    if lock_date_search:
        lock_date = util_n.as_date_delay(lock_date_search.group(0))
        if re.search(r'\d', lock_date_search.group(0)) and u'个月' in lock_date_search.group(0):
            num = filter(str.isdigit, lock_date_search.group(0).encode('gbk'))
            lock_date = str(int(num))
        elif re.search(r'\d', lock_date_search.group(0)) and u'年' in lock_date_search.group(0):
            num = filter(str.isdigit, lock_date_search.group(0).encode('gbk'))
            lock_date = str(int(num))
        elif u'半年' in lock_date_search.group(0):
            lock_date = str(6)
    return lock_date
# 剥夺政治权利时长
def rightdate(judge_reesult):
    right_date = ''
    right_date_search = re.search(u'((?<=剥夺政治权利)\d+(?:年|个月))|((?<=剥夺政治权利)[\u4e00-\u9fa5]{1,5}?(?:年|个月))', judge_result)
    if right_date_search:
        right_date = str(util_n.as_date_date(right_date_search.group(0)))
        # print judge_result.encode('GB18030')
        # print right_date_search.group(0),right_date
    if u'剥夺政治权利' in judge_result and u'终身' in judge_result:
        right_date = u'终身'
    return right_date

for i in row:
    punish_cate = ''       # 刑事判决类型（拘役或管制、有期徒刑、无期徒刑、死刑）
    punish_date = ''       # 有期徒刑期（月）
    delay_date = ''        # 缓刑期（月）
    punish_money = ''      # 罚金
    crime_reason = ''      # 案由 list
    control_date=''        # 拘役时间
    lock_date=''           # 管制时间
    right_date=''          #
    if_right = 0
    # 案由
    crime_reason = to_list(i[3])
    # print crime_reason
    try:
        judge_result = util_n.as_text(i[6])
    except ValueError:
        judge_result = ''
    # punish = re.split(u'\n', i[5])
    if len(judge_result):
        # 有期徒刑类型
        punish_cate = punishcate(judge_result)
        # 有期徒刑期
        punish_date = punishdate(judge_result)
        # 缓刑期
        delay_date = delaydate(judge_result)
        # 拘役时长
        control_date = controldate(judge_result)
        # 管制时长
        lock_date = lockdate(judge_result)
        # 剥夺政治权利时长
        right_date = rightdate(judge_result)
        # 是否剥夺政治权利
        if right_date:
            if_right=1

    print i[0],punish_cate,punish_date,delay_date,control_date,lock_date
    # value = [i[0],punish_cate,punish_date,delay_date,control_date,lock_date]
#     sql = "update tmp_liufang set punish_cate='%s',punish_date='%s',delay_date='%s', control_date='%s',lock_date='%s' where uuid='%s'" % (punish_cate,punish_date,delay_date,control_date,lock_date, i[0])
#     cursor.execute(sql)
# con.commit()
# cursor.close()
# con.close()