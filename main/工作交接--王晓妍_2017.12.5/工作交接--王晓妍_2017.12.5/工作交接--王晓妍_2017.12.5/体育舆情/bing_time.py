# -*- coding: utf-8 -*-
# 体育mysql数据 全网分析
import MySQLdb
import pandas as pd
import numpy as np
import json
conn=MySQLdb.connect(host='192.168.12.34',user='wxy',passwd='123456',db='spider',charset='utf8')
cursor=conn.cursor()

cursor.execute("select id,tie_date from tmp_tieba where sub_id=8") 
ba_result=cursor.fetchall()

cursor.execute("select id,date from tmp_weibo where sub_id=8")
bo_result=cursor.fetchall()

cursor.execute('select id,web_time from tmp_news where sub_id=8')
new_result=cursor.fetchall()

cursor.execute("select id,date from tmp_wechat where sub_id=8")
chat_result=cursor.fetchall()

cursor.execute("select id,date from tmp_bbs where sub_id=8")
bbs_result=cursor.fetchall()

# 体育全网分析 来源饼图 mysql
ba_num=len(ba_result)
bo_num=len(bo_result)
new_num=len(new_result)
chat_num=len(chat_result)
bbs_num=len(bbs_result)
print "贴吧、微博、新闻、微信、论坛文章个数分别为：" 
print (ba_num,bo_num,new_num,chat_num,bbs_num)

from datetime import datetime
from datetime import timedelta

# 体育全网分析 时序图
date_list=[]
begin_date = datetime.strptime('2017-04-30', "%Y-%m-%d")
end_date = datetime.strptime('2017-10-10', "%Y-%m-%d")
while begin_date <= end_date:
    date_str = begin_date.strftime("%Y-%m-%d")
    date_list.append(date_str)
    begin_date += timedelta(1)

time1,time2,time3,time4,time5=[],[],[],[],[]
for r in bo_result:
    time1.append(r[1])
for r in ba_result:
    time2.append(r[1])
for r in new_result:
    time3.append(r[1])
for r in chat_result:
    time4.append(r[1])
for r in bbs_result:
    time5.append(r[1])
    
time_new=pd.Series(time3).value_counts()
time_weibo=pd.Series(time1).value_counts()
time_wechat=pd.Series(time4).value_counts()
time_ba=pd.Series(time2).value_counts() 
time_bbs=pd.Series(time5).value_counts() 
 
def time_num(time_s):
    num=np.zeros(len(date_list))
    for i in range(len(date_list)):
        for j in range(len(time_s)):
            if date_list[i]==time_s.keys()[j]:
                num[i]=time_s[j]
            else:
                pass 
    return num  
    
media_time={}
timekey=['time','新闻','微信','微博','贴吧','论坛']
timevalue=[date_list,list(time_num(time_new)),list(time_num(time_wechat)),list(time_num(time_weibo)),list(time_num(time_ba)),list(time_num(time_bbs))]
for i in range(len(timekey)):
    media_time[timekey[i]]=timevalue[i]
source2=open('data/time.txt','w')
source2.write(json.dumps(media_time,ensure_ascii=False))
source2.close()