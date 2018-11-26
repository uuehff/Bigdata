# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 18:51:34 2017

@author: Administrator
"""
# 媒体排行
import pandas as pd
import MySQLdb
import json

def rank_wechat(result):
    name2,dianzan,comm,zhuanfa=[],[],[],[]
    for r in result:
        name2.append(r[0])
        dianzan.append(r[3])
        comm.append(r[2])
        zhuanfa.append(r[1])
    frame=pd.DataFrame({'name2':name2,'dianzan':dianzan,'comm':comm,'zhuanfa':zhuanfa},columns=['name2','dianzan','comm','zhuanfa'])
    
    #按名称统计点赞、转发数并与粉丝数合并 被转发数有问题没考虑
    zan_num=frame['dianzan'].groupby(frame['name2']).sum()
    comm_num=frame['comm'].groupby(frame['name2']).sum()
    fa_num=frame['zhuanfa'].groupby(frame['name2']).sum()
    bo_num=frame['name2'].groupby(frame['name2']).count()
    
    #归一化总分 粉丝和其他特征的i要对上
    def rank(zan,comm,fa,bo):
        a_=(zan-min(zan_num))*1.0/(max(zan_num)-min(zan_num))
        b_=(comm-min(comm_num))*1.0/(max(comm_num)-min(comm_num))
        c_=(fa-min(fa_num))*1.0/(max(fa_num)-min(fa_num))
        e_=(bo-min(bo_num))*1.0/(max(bo_num)-min(bo_num))
    
        return a_+b_+c_+e_
    
    df3=pd.DataFrame({'name':zan_num.keys(),'zan_num':zan_num.values,'comm_num':comm_num.values,'fa_num':fa_num.values,'num':bo_num.values},columns=['name','zan_num','num','comm_num','fa_num'])
    
    score=[]
    for i in range(len(zan_num)):
        score.append(rank(df3.zan_num[i],df3.comm_num[i],df3.fa_num[i],df3.num[i]))
    df3['score']=score       
    a=df3.sort_values(by='score',ascending=False)[:5]   
    name=[]
    for i in a['name']:
        name.append(i)
    fensi=[]
    for j in a['score']:
        fensi.append(j)
            
    fensi_w={}
    for i in range(len(name)):
        fensi_w[name[i]]=fensi[i]
    return fensi_w

def rank_ba(result):
    fensi,name2,dianzan=[],[],[]
    for r in result:
        name2.append(r[0])
        fensi.append(r[2])
        dianzan.append(r[1])
    frame=pd.DataFrame({'name2':name2,'fensi':fensi,'dianzan':dianzan},columns=['name2','fensi','dianzan'])
    
    #按名称统计点赞、转发数并与粉丝数合并 被转发数有问题没考虑
    fen_num=frame['fensi'].groupby(frame['name2']).mean() #应该是mean
    zan_num=frame['dianzan'].groupby(frame['name2']).sum()
    bo_num=frame['name2'].groupby(frame['name2']).count()
    
    #归一化总分 粉丝和其他特征的i要对上
    def rank(zan,fen,bo):
        a_=(zan-min(zan_num))*1.0/(max(zan_num)-min(zan_num))
        d_=(fen-min(fen_num))*1.0/(max(fen_num)-min(fen_num)) 
        if max(bo_num)!=min(bo_num):
            e_=(bo-min(bo_num))*1.0/(max(bo_num)-min(bo_num))
        else:
            e_=0    
        return a_+d_+e_
    
    df3=pd.DataFrame({'name':zan_num.keys(),'fen_num':fen_num.values,'zan_num':zan_num.values,'num':bo_num.values},columns=['name','fen_num','zan_num','num'])
    
    score=[]
    for i in range(len(zan_num)):
        score.append(rank(df3.zan_num[i],df3.fen_num[i],df3.num[i]))
    df3['score']=score       
    a=df3.sort_values(by='score',ascending=False)[:5]   
    name=[]
    for i in a['name']:
        name.append(i)
    fensi=[]
    for j in a['score']:
        fensi.append(j)
            
    fensi_w={}
    for i in range(len(name)):
        fensi_w[name[i]]=fensi[i]
    return fensi_w

def rank_new(result):
    fensi,name2,dianzan=[],[],[]
    for r in result:
        name2.append(r[0])
        fensi.append(r[2])
        dianzan.append(r[1])
    frame=pd.DataFrame({'name2':name2,'fensi':fensi,'dianzan':dianzan},columns=['name2','fensi','dianzan'])
    
    #按名称统计点赞、转发数并与粉丝数合并 被转发数有问题没考虑
    fen_num=frame['fensi'].groupby(frame['name2']).sum()
    zan_num=frame['dianzan'].groupby(frame['name2']).sum()
    bo_num=frame['name2'].groupby(frame['name2']).count()
    
    #归一化总分 粉丝和其他特征的i要对上
    def rank(zan,fen,bo):
        if max(zan_num)!=min(zan_num):
            a_=(zan-min(zan_num))*1.0/(max(zan_num)-min(zan_num))
        else:
            a_=0
        if max(fen_num)!=min(fen_num):
            d_=(fen-min(fen_num))*1.0/(max(fen_num)-min(fen_num)) 
        else:
            d_=0
        e_=(bo-min(bo_num))*1.0/(max(bo_num)-min(bo_num))
    
        return a_+d_+e_
    
    df3=pd.DataFrame({'name':zan_num.keys(),'fen_num':fen_num.values,'zan_num':zan_num.values,'num':bo_num.values},columns=['name','fen_num','zan_num','num'])
    
    score=[]
    for i in range(len(zan_num)):
        score.append(rank(df3.zan_num[i],df3.fen_num[i],df3.num[i]))
    df3['score']=score       
    a=df3.sort_values(by='score',ascending=False)[:5]   
    name=[]
    for i in a['name']:
        name.append(i)
    fensi=[]
    for j in a['score']:
        fensi.append(j)
            
    fensi_w={}
    for i in range(len(name)):
        fensi_w[name[i]]=fensi[i]
    return fensi_w
    
def rank_bo(result):
    fensi,name2,dianzan,comm,zhuanfa=[],[],[],[],[]
    for r in result:
        name2.append(r[0])
        fensi.append(r[4])
        dianzan.append(r[3])
        comm.append(r[2])
        zhuanfa.append(r[1])
    frame=pd.DataFrame({'name2':name2,'fensi':fensi,'dianzan':dianzan,'comm':comm,'zhuanfa':zhuanfa},columns=['name2','fensi','dianzan','comm','zhuanfa'])
    
    #按名称统计点赞、转发数并与粉丝数合并 被转发数有问题没考虑
    fen_num=frame['fensi'].groupby(frame['name2']).mean()
    zan_num=frame['dianzan'].groupby(frame['name2']).sum()
    comm_num=frame['comm'].groupby(frame['name2']).sum()
    fa_num=frame['zhuanfa'].groupby(frame['name2']).sum()
    bo_num=frame['name2'].groupby(frame['name2']).count()
    
    #归一化总分 粉丝和其他特征的i要对上
    def rank(zan,comm,fa,fen,bo):
        a_=(zan-min(zan_num))*1.0/(max(zan_num)-min(zan_num))
        b_=(comm-min(comm_num))*1.0/(max(comm_num)-min(comm_num))
        c_=(fa-min(fa_num))*1.0/(max(fa_num)-min(fa_num))
        d_=(fen-min(fen_num))*1.0/(max(fen_num)-min(fen_num)) 
        e_=(bo-min(bo_num))*1.0/(max(bo_num)-min(bo_num))
    
        return a_+b_+c_+d_+e_
    
    df3=pd.DataFrame({'name':zan_num.keys(),'fen_num':fen_num.values,'zan_num':zan_num.values,'comm_num':comm_num.values,'fa_num':fa_num.values,'num':bo_num.values},columns=['name','fen_num','zan_num','num','comm_num','fa_num'])
    
    score=[]
    for i in range(len(zan_num)):
        score.append(rank(df3.zan_num[i],df3.comm_num[i],df3.fa_num[i],df3.fen_num[i],df3.num[i]))
    df3['score']=score       
    a=df3.sort_values(by='score',ascending=False)[:5]   
    name=[]
    for i in a['name']:
        name.append(i)
    fensi=[]
    for j in a['score']:
        fensi.append(j)
            
    fensi_w={}
    for i in range(len(name)):
        fensi_w[name[i]]=fensi[i]
    return fensi_w

     
conn = MySQLdb.connect(host='192.168.12.34',user='wxy',passwd='123456',db='spider',charset='utf8')
cursor = conn.cursor()
cursor.execute("select name,followers,relays_num,comments_num,likes_num from tmp_weibo where sub_id=4")
bo_result = cursor.fetchall()

cursor.execute("select tieba_name,reply_num,tie_follow from tmp_tieba where sub_id=4") 
ba_result=cursor.fetchall()

cursor.execute('select web_name,web_read_num,web_comment_num from tmp_news where sub_id=4')
new_result=cursor.fetchall()

cursor.execute("select name,comments_num,read_num,likes_num from tmp_wechat where sub_id=4")
chat_result=cursor.fetchall()

# 微信
a1=rank_wechat(chat_result)
#source1=open('data/rank_chat.txt','w')
print json.dumps(a1,ensure_ascii=False)

# 微博
a2=rank_bo(bo_result)
#source2=open('data/rank_bo.txt','w')
print json.dumps(a2,ensure_ascii=False)

# 贴吧
a3=rank_ba(ba_result)
#source3=open('data/rank_ba.txt','w')
print json.dumps(a3,ensure_ascii=False)

# 新闻
a4=rank_new(new_result)
#source4=open('data/rank_news.txt','w')
print json.dumps(a4,ensure_ascii=False)
