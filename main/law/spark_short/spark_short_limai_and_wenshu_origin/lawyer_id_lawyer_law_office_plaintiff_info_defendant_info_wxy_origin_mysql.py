# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 15:56:15 2018

@author: hhly-pc
"""

# 提取律师
import re
import json
import MySQLdb

# 取出律师、律所
def get_lawyer(text):
    office={}
    person=u''
    off=u''
    patt=re.compile(ur'(诉讼代理人|辩护人|委托代理人|委托代理|诉讼代理|委托代表人|诉讼代表人|代理人（特别授权）|代理人（特别授权代理）)[：]{0,1}([\u4e00-\u9fa5]{2,10})(，|（|,|、)(.*?)(事务所律师|律师事务所">|事物所律师|中心律师|中心律师（特别授权）|事务部律师|法律援助中心，律师|律师事务所，律师|援助处律师|援助律师|工作站律师|工作总站律师|分所律师|服务所律师|律师事务所主任|事务律师|顾问室律师|顾问处军队律师|办公室律师|局律师|指派律师|律师部律师|律师所律师|公司律师|分行律师|政府律师|队律师|。)')
    for s in text:        
        o=re.findall(patt,s[1]) #s[1]
        if o:
            for i in range(len(o)):
                if u'律师' in o[i][4] and u'该' not in o[i][3] and u'＊' not in o[i][1] and u'X' not in o[i][1] and u'×' not in o[i][1] \
                and u'Ｘ' not in o[i][1] and u'某' not in o[i][1] and u'x' not in o[i][1] and u'×' not in o[i][3] and u'Ｘ'not in o[i][3] \
                and u'X' not in o[i][3] and u'x' not in o[i][3] and u'某' not in o[i][3] and u'＊' not in o[i][3] \
                 and u'A' not in o[i][3] and u'B' not in o[i][3] and u'C' not in o[i][3]:
                    lawy= o[i][1]
                    lawy=lawy.split(u'代理')[-1]
                    lawy=lawy.strip(u'均为').lstrip(u'人').rstrip(u'上诉人')
                    
                    a=o[i][3]+o[i][4]
                    a=a.replace(u'事物',u'事务')
                    a=a.replace(u'事务律师',u'事务所律师')
                    a=a.replace(u'律师事务所，律师',u'律师事务所律师')
                    a=a.replace(u'法律援助中心，律师',u'法律援助中心律师')
                    b=a.split(u'，')[-1]
                    b=b.split(u'、')[-1]
                    b=b.split(u'代理）')[-1]
                    b=b.split(u'授权）')[-1]
                    b=b.split(u',')[-1]   
                    b=b.split(u'：')[-1]
                    b=b.split(u'委托）')[-1]
                    c=b.strip(u'律师').strip(u'均系').strip(u'均为').strip(u'分别为').strip(u'系').strip(u'分别').strip(u'是').strip(u'主任').strip(u'军队').strip(u'指派').strip(u'\">')
                    if len(lawy)>1 and c !=u'律师事务所' and c !=u'事务所' and c != u'法律援助中心' and len(c)>3:
                        if c not in off:
                            off += c+u'||'                    
                        office[lawy]=c 
                        if lawy not in person:
                            person += lawy + u'||'                    
    office_=json.dumps(office,ensure_ascii=False)         
    return office_,person[:-2], off[:-2]

patt1=re.compile(ur'(原告)(.*?)(?=被告|原告|$)')
patt2=re.compile(ur'(被告)(.*?)(?=原告|被告|$)')
# 取出原告、被告内容
def get_text(f):
    f=f.replace(u'\n',u'')
    plain=re.findall(patt1,f)    
    defen=re.findall(patt2,f) 
    return plain,defen

#for i in get_text(r)[1]:
#    print i[1]
def get_result(uuid,text,judge,reason,id_):
    party=get_text(text)
    if party[0]:
        plaintiff = get_lawyer(party[0])[0]
        if plaintiff==u'{}':
            plaintiff=u''
    else:
        plaintiff = u''
        
    if party[1]:
        defendant = get_lawyer(party[1])[0]
        if defendant==u'{}':
            defendant=u''
    else:
        defendant = u''
    lawyer_ = get_lawyer(party[0])[1]+u'||'+get_lawyer(party[1])[1]
    lawyer_ = lawyer_.strip(u'||')
    office_ = get_lawyer(party[0])[2]+u'||'+get_lawyer(party[1])[2]
    office_ = office_.strip(u'||')
    return id_,uuid,plaintiff,defendant,office_,lawyer_,judge,reason
    

a=0
b=100000
while a<1000000: 
    conn=MySQLdb.connect(host='192.168.74.102',user='wxy',passwd='123456',db='laws_doc_adjudication',charset='utf8')
    cursor=conn.cursor()
    cursor.execute("select uuid,party_info,court_idea,judge_type,reason_type,id from adjudication_xingshi_etl_v2 where party_info like '%s' or court_idea like '%s' limit %s,%s" % (u'%律师%',u'%律师%',a,b))
    do_result=cursor.fetchall()
     
    for r in do_result:
        if r[1]!=u'':
            tmp=get_result(r[0],r[1],r[3],r[4],r[5])
        if r[1]==u'' or tmp[4]==u'':            
            if r[2]!=u'':
                tmp=get_result(r[0],r[2],r[3],r[4],r[5])
                    
        if tmp[4] !=u'':
            sql="insert into adjudication_xingshi_etl_v2_lawyer(id,uuid,plaintiff_info,defendant_info,law_office,lawyer,judge_type,reason_type) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql,tmp)
            conn.commit()    
    a +=100000
    print a #处理完