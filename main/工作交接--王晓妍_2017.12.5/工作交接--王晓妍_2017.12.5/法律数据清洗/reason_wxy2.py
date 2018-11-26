# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 10:24:12 2017

@author: Administrator
"""


#根据案由统计结果 mysql
import numpy as np
import MySQLdb
import pandas as pd
import json

def dur_r(duration):
    dur=np.zeros(11,dtype=np.int)
    if duration!=None:
        for i in duration:
            if i!=u'' and i!=None:
                if int(i)>0 and int(i)<10:
                    dur[0] +=1
                if int(i)>=10 and int(i)<20:
                    dur[1] +=1
                if int(i)>=20 and int(i)<30:
                    dur[2] +=1
                if int(i)>=30 and int(i)<40:
                    dur[3] +=1
                if int(i)>=40 and int(i)<50:
                    dur[4] +=1
                if int(i)>=50 and int(i)<60:
                    dur[5] +=1
                if int(i)>=60 and int(i)<70:
                    dur[6] +=1
                if int(i)>=70 and int(i)<80:
                    dur[7] +=1     
                if int(i)>=80 and int(i)<90:
                    dur[8] +=1
                if int(i)>=90 and int(i)<120:
                    dur[9] +=1
                if int(i)>=120:
                    dur[10] +=1 
    return dur
    
    

def court_cat(court_cate):
    cate=np.zeros(4,dtype=np.int)
    if court_cate!=None:
        for i in court_cate:
            if i!=u'' and i !=None:
                if i == u'基层':
                    cate[3] +=1
                if i ==u'中级':
                    cate[2] +=1
                if i==u'高级':
                    cate[1] +=1
                if i==u'最高':
                    cate[0] +=1
    return cate

def top_list(court):
    court_l=[]
    if court!=None:
        for i in court:
            if i !=None:
                i="".join(i)
                for j in i.split(u'||'):
                    if j!=u'':
                        court_l.append(j)  

    court_list=pd.Series(court_l).value_counts()[:10]    
    court_top={}
    for i in range(len(court_list)):
        court_top[court_list.keys()[i]]=int(court_list[i])
    return court_top
    
    
conn=MySQLdb.connect(host='192.168.12.34',user='wxy',passwd='123456',db='laws_doc',charset='utf8')
cursor=conn.cursor()

cursor.execute("select new_name from tb_reason")
result=cursor.fetchall()
reason=[]
for r in result:
    reason.append(r[0])
reason=list(set(reason))
#reason=[u'伪造、变造股票、公司、企业债券',u'伪造、变造金融票证']

cursor.execute("select duration,new_office,court_cate,new_reason,new_lawyer,casedate_new,court_new,if_accumulate,if_surrender,if_nosuccess from tmp_liufang,tmp_raolu,tmp_wxy where tmp_liufang.uuid=tmp_wxy.uuid and tmp_wxy.uuid=tmp_raolu.uuid")
results=cursor.fetchall() 

for i in reason:
    count=0
    duration,court_c,court,office,defendant_f=[],[],[],[],[]
    accum={}
    accum[u'累犯']=0
    accum[u'非累犯']=0
    
    surr={}
    surr[u'自首']=0
    surr[u'未自首']=0
    
    nosu={}
    nosu[u'未遂']=0
    nosu[u'成功']=0
    for r in results:
        if i in r[3].split('||'):
            count +=1
            if r[0]!=u'' and r[0]!=None:
                duration.append(r[0])
            if r[2]!=u'' and r[2]!=None:
                court_c.append(r[2])
            if r[6]!=u'' and r[6]!=None:
                court.append(r[6])
            if r[1]!=u'' and r[1]!=None:
                office.append(r[1]) 
            if r[4]!=u'' and r[4]!=None:
                defendant_f.append(r[4])
#           if r[5]>='2008-01-01':
#                defendant_10.append(r[4])
            #if r[5]>='2015-01-01':
                #defendant_3.append(r[4])

            if r[7]==u'1':
                accum[u'累犯'] +=1
            if r[7]==u'0':
                accum[u'非累犯'] +=1
            if r[8]==u'1':
                surr[u'自首'] +=1
            if r[8]==u'0':
                surr[u'未自首'] +=1
            if r[9]==u'1':
                nosu[u'未遂'] +=1
            if r[9]==u'0':
                nosu[u'成功'] +=1
        #诉讼时长
        #duration=[u'8', u'18', u'', u'20', u'21', u'16', u'', u'7', u'6', u'38']            
    duration_r={}
    duration_r[u'10天以下']=0
    duration_r[u'10-20天']=0
    duration_r[u'20-30天']=0
    duration_r[u'30-40天']=0
    duration_r[u'40-50天']=0
    duration_r[u'50-60天']=0
    duration_r[u'60-70天']=0
    duration_r[u'70-80天']=0
    duration_r[u'80-90天']=0
    duration_r[u'90-120天']=0
    duration_r[u'120天以上']=0
    duration_r[u'10天以下'] +=dur_r(duration)[0]
    duration_r[u'10-20天'] +=dur_r(duration)[1]
    duration_r[u'20-30天'] +=dur_r(duration)[2]
    duration_r[u'30-40天'] +=dur_r(duration)[3]
    duration_r[u'40-50天'] +=dur_r(duration)[4]
    duration_r[u'50-60天'] +=dur_r(duration)[5]
    duration_r[u'60-70天'] +=dur_r(duration)[6]
    duration_r[u'70-80天'] +=dur_r(duration)[7]
    duration_r[u'80-90天'] +=dur_r(duration)[8]
    duration_r[u'90-120天'] +=dur_r(duration)[9]
    duration_r[u'120天以上'] +=dur_r(duration)[10]
               
        #法院级别
    court_cate={}
    court_cate[u'最高级法院']=0
    court_cate[u'高级法院']=0
    court_cate[u'中级法院']=0
    court_cate[u'基层法院']=0
    court_cate[u'最高级法院'] +=court_cat(court_c)[0]
    court_cate[u'高级法院'] +=court_cat(court_c)[1]
    court_cate[u'中级法院'] +=court_cat(court_c)[2]
    court_cate[u'基层法院'] +=court_cat(court_c)[3]
        
    court_t=top_list(court)
    court_t=json.dumps(court_t,ensure_ascii=False)
    duration_r=json.dumps(duration_r,ensure_ascii=False)
    court_cate=json.dumps(court_cate,ensure_ascii=False)
    office_t=top_list(office)
    office_t=json.dumps(office_t,ensure_ascii=False)
                                         
    #defendant_t=top_list(defendant_10)
    #defendant_t=json.dumps(defendant_t,ensure_ascii=False)                        
    #defendant_r=top_list(defendant_3)   
    #defendant_r=json.dumps(defendant_r,ensure_ascii=False)
    defendant_full=top_list(defendant_f)   
    defendant_full=json.dumps(defendant_full,ensure_ascii=False)
    accum=json.dumps(accum,ensure_ascii=False)
    surr=json.dumps(surr,ensure_ascii=False)
    nosu=json.dumps(nosu,ensure_ascii=False)
    tmp=[i,count,duration_r,court_cate,office_t,defendant_full,court_t,accum,surr,nosu]
    #print tmp
    sql='insert into tmp_reason_wxy(reason,count,duration,court_cat,office_top,defendant_full,court_top,accumulate,surrender,nosuccess) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    cursor.execute(sql,tmp)    
    conn.commit()
cursor.close()
conn.close()   