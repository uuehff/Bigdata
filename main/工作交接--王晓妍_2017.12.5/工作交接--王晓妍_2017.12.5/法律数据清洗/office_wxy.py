# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 15:35:27 2017

@author: Administrator
"""

#根据律师事务所统计结果 mysql
import MySQLdb
import pandas as pd
import json
from datetime import datetime
import numpy as np

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
        court_top[court_list.keys()[i].encode('utf8')]=int(court_list[i])
    return court_top    

def dur_r(duration):
    dur=np.zeros(11,dtype=np.int)
    if duration!=None:
        for i in duration:
            if i!=u'' and i!=None:
                if int(i)>=0 and int(i)<10:
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
    
conn=MySQLdb.connect(host='192.168.12.34',user='wxy',passwd='123456',db='laws_doc',charset='utf8')
cursor=conn.cursor()

cursor.execute("select new_office from tmp_raolu")
result=cursor.fetchall()
office=[]
for r in result:
    if r[0]!=u'' and r[0]!=None:
        office.append(r[0])
office=list(set(office))
print len(office)#32927条

cursor.execute("select court_new,duration,casedate_new,new_office,court_cate,reason,tmp_wxy.fact_finder_new from tmp_wxy,tmp_raolu,tmp_liufang where new_office !='%s' and tmp_wxy.uuid=tmp_raolu.uuid and tmp_wxy.uuid=tmp_liufang.uuid" % (u''))
results=cursor.fetchall() 
from operator import itemgetter
text=sorted(results,key=itemgetter(3,0)) #按律所排序 

a=0
for f in office: 
    year={}
    year['2017年']=0
    year['2016年']=0
    year['2015年']=0
    year['2014年']=0
    year['2013年']=0
    year['2012年']=0
    year['2011年']=0
    year['2010年']=0
    year['2009年']=0
    year['2008年']=0
    count=0
    reason,court,finder,duration,court_c=[],[],[],[],[]
    for r in text:
        if r[3]!=None and r[3]!=u'' and f == r[3]:#NoneType
            count +=1
            if r[5]!=None and r[5]!=u'':
                reason.append(r[5])
            if r[0]!=None and r[0]!=u'': 
                court.append(r[0])
            if r[6]!=None and r[6]!=u'':    
                finder.append(r[6])
            if r[1]!=None and r[1]!=u'':
                duration.append(r[1])
            if r[4]!=None and r[4]!=u'':
                court_c.append(r[4])             
            if r[2]!=None and r[2]!=u'':
                t = datetime.strptime(r[2], '%Y-%m-%d')
                t_year = t.year  
                if t_year == 2017:
                    year['2017年'] +=1
                elif t_year == 2016:
                    year['2016年'] +=1
                elif t_year == 2015:
                    year['2015年'] +=1
                elif t_year == 2014:
                    year['2014年'] +=1
                elif t_year == 2013:
                    year['2013年'] +=1
                elif t_year == 2012:
                    year['2012年'] +=1
                elif t_year == 2011:
                    year['2011年'] +=1
                elif t_year == 2010:
                    year['2010年'] +=1
                elif t_year == 2009:
                    year['2009年'] +=1
                elif t_year == 2008:
                    year['2008年'] +=1
    duration_r={}
    duration_r['10天以下']=0
    duration_r['10-20天']=0
    duration_r['20-30天']=0
    duration_r['30-40天']=0
    duration_r['40-50天']=0
    duration_r['50-60天']=0
    duration_r['60-70天']=0
    duration_r['70-80天']=0
    duration_r['80-90天']=0
    duration_r['90-120天']=0
    duration_r['120天以上']=0
    duration_r['10天以下'] +=dur_r(duration)[0]
    duration_r['10-20天'] +=dur_r(duration)[1]
    duration_r['20-30天'] +=dur_r(duration)[2]
    duration_r['30-40天'] +=dur_r(duration)[3]
    duration_r['40-50天'] +=dur_r(duration)[4]
    duration_r['50-60天'] +=dur_r(duration)[5]
    duration_r['60-70天'] +=dur_r(duration)[6]
    duration_r['70-80天'] +=dur_r(duration)[7]
    duration_r['80-90天'] +=dur_r(duration)[8]
    duration_r['90-120天'] +=dur_r(duration)[9]
    duration_r['120天以上'] +=dur_r(duration)[10]   
    
    court_cate={}
    court_cate['最高级法院']=0
    court_cate['高级法院']=0
    court_cate['中级法院']=0
    court_cate['基层法院']=0
    court_cate['最高级法院'] +=court_cat(court_c)[0]
    court_cate['高级法院'] +=court_cat(court_c)[1]
    court_cate['中级法院'] +=court_cat(court_c)[2]
    court_cate['基层法院'] +=court_cat(court_c)[3]  
   
    court_t=top_list(court)
    reason_t=top_list(reason)
    finder_t=top_list(finder)
    court_t=json.dumps(court_t,ensure_ascii=False)
    reason_t=json.dumps(reason_t,ensure_ascii=False)
    finder_t=json.dumps(finder_t,ensure_ascii=False)
    year=json.dumps(year,ensure_ascii=False)
    court_cate=json.dumps(court_cate,ensure_ascii=False)
    duration_r=json.dumps(duration_r,ensure_ascii=False)
    
    tmp=[f.encode('utf-8'),count,year,duration_r,court_cate,court_t,reason_t,finder_t]
    print a
    a +=1
    sql="insert into scene_office(office,office_num,new10_dict,duration_dict,court_cate_dict,court_top,reason_top,finder_top) values (%s,%s,%s,%s,%s,%s,%s,%s)"
    cursor.execute(sql,tmp)    
    conn.commit()
#    writer.writerow(tmp)
#csvf.close()
cursor.close()
conn.close()
#＊ □ ⅹ A B
