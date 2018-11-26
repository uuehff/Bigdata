# -*- coding: utf-8 -*-
"""
# mysql 体育数据清洗 
#微博清洗
import MySQLdb
from datetime import datetime
import re
import json

# 时间清洗为‘1900-01-01’的格式
def weiboTime(time):
    if time!='':
        time_datetime=datetime.strptime(time.strip(),'%Y-%m-%d %H:%M:%S')
        time=time_datetime.strftime('%Y-%m-%d')
    else:
        pass
    return time

def verify_c(data):
    if u'公司' in data or u'集团' in data:
        tag=u'企业'
    elif u'运动员' in data or u'创始人' in data or u'总监' in data:
        tag=u'名人'
    elif u'达人' or u'博主' in data:
        tag=u'达人'
    elif u'官方微博' in data:
        tag=u'媒体'
    else:
        tag=u'普通'    
    return tag

def clean_at(text):
    text=text.replace(u'u3000',u'')
    if text!=u'':
        pat1=re.compile(ur'(?:@)(.*)?(?:\s)')
        g=re.search(pat1,text)
        if g:
            text=text.replace(g.group(),u'')            
        pattern = re.compile(ur'(.*)(?=@|u200b)')
        f = re.search(pattern,text)
        if f:
            content=f.group()
        else:
            content=text
    else:
        content = u''
    return content
    
def clean_content(text):
    content=clean_at(text)
    if content !=u'':
        if content[-1]==u' ':
            content=content[:-1]
    return content

def clean_comment(text):    
    if text!=u'':
        comment=[]
        data=json.loads(text.encode('utf-8'))
        for i in range(len(data)):
            if data.values()[i][0]!=u'':
                if u'回复' not in data.values()[i][0] and u'转发微博' not in data.values()[i][0]:
                    if clean_at(data.values()[i][0]) !=u'':
                        comment.append(clean_at(data.values()[i][0]))
        comment=json.dumps(comment,ensure_ascii=False)
        if comment=='[]':
            comment=u''
    
    if text==u'':
        comment=u''

    return comment
    
conn=MySQLdb.connect(host='192.168.12.34',user='wxy',passwd='123456',db='spider',charset='utf8')
cursor=conn.cursor()
cursor.execute("select id,mid,verify,area,pub_date,content,comments,name,sex,tag,level,summary,followers,relays_num,comments_num,likes_num,relay_id,sub_id from weibo where sub_id=8")
bo_result=cursor.fetchall()

for r in bo_result:
    verify_cat=verify_c(r[2])
    if r[3]!=None:
        province=r[3].split(' ')[0]
    else:
        province=r[3]
    date=weiboTime(r[4])
    content=clean_content(r[5])
    comment=clean_comment(r[6])
    tmp=(r[0],r[1],verify_cat,r[7],r[8],province,r[9],r[10],r[11],r[12],date,content,r[13],r[14],r[15],comment,r[16],r[17])
    sql="insert into tmp_weibo(id,mid,verify_cate,name,sex,province,tag,level,summary,followers,date,new_content,relays_num,comments_num,likes_num,new_comment,relay_id,sub_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    cursor.execute(sql,tmp)
    conn.commit()
cursor.close()
conn.close()

# 清洗体育贴吧数据 主要就是评论、时间
import MySQLdb
from datetime import datetime
import json

def baTime(time):
    if time!='':
        time_datetime=datetime.strptime(time.strip(),'%Y-%m-%d %H:%M')
        time=time_datetime.strftime('%Y-%m-%d')
    else:
        pass
    return time

def ba_comment(text):    
    if text!=u'[]':
        comment=[]
        data=json.loads(text)
        for i in range(len(data)):
            if data[i][u'tie_content']!=u'':
               comment.append(data[i][u'tie_content'])
        comment=json.dumps(comment,ensure_ascii=False)
        if comment=='[]':
            comment=u''    
    if text==u'[]':
        comment=u''

    return comment

def length(comm):
    if len(comm)!=0:
        num=len(json.loads(comm))
    else:
        num=0
    return num
    
conn=MySQLdb.connect(host='192.168.12.34',user='wxy',passwd='123456',db='spider',charset='utf8')
cursor=conn.cursor()
cursor.execute("select id,tie_time,tie_reply_list,sub_id,tie_url,tie_title,tieba_name,tie_content,tie_follow from tieba where sub_id=8") 
bo_result=cursor.fetchall()
    
for r in bo_result:
    try:
        date=baTime(r[1])
        comment=ba_comment(r[2])
        comm_num=length(comment)
        tmp=(r[0],r[3],r[4],r[5],r[6],r[7],r[8],date,comment,comm_num)
        sql="insert into tmp_tieba(id,sub_id,tie_url,tie_title,tieba_name,tie_content,tie_follow,tie_date,reply,reply_num) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql,tmp)
        conn.commit()
    except:
        pass
cursor.close()
conn.close()

# 清洗微信
import MySQLdb
from datetime import datetime
def weiboTime(time):
    if time!='':
        time_datetime=datetime.strptime(time.strip(),'%Y-%m-%d %H:%M:%S')
        time=time_datetime.strftime('%Y-%m-%d')
    else:
        pass
    return time
def clean_assum(text): 
    text=text.replace(u'\\x0a',u'')
    text=text.replace(u'u200b',u'')
    text=text.replace(u'\\x26quot;',u'')
    return text
conn=MySQLdb.connect(host='192.168.12.34',user='wxy',passwd='123456',db='spider',charset='utf8')
cursor=conn.cursor()
cursor.execute("select id,pub_date,title,name,asummary,summary,content,comments_num,read_num,likes_num,comments,sub_id from wechat where sub_id=8") 
bo_result=cursor.fetchall()
    
for r in bo_result:
    date=weiboTime(r[1])
    assu=clean_assum(r[4])
    tmp=(r[0],r[2],r[3],assu,r[5],date,r[6],r[7],r[8],r[9],r[10],r[11])
    sql="insert into tmp_wechat(id,title,name,asummary,summary,date,content,comments_num,read_num,likes_num,comments,sub_id) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    cursor.execute(sql,tmp)
    conn.commit()
cursor.close()
conn.close()    

# 新闻表清洗
import MySQLdb
import json
from datetime import datetime
def new_comment(text):    
    if text!=None and text!=u'':
            comment=[]
            data=json.loads(text)
            for i in range(len(data)):
                if data[i][u'content']!=u'':
                   comment.append(data[i][u'content'])
            comment=json.dumps(comment,ensure_ascii=False)
            if comment=='[]':
                comment=u''   
    else:
        comment=u''
    return comment

def newTime(time):
    if time!='':
        try:
            time_datetime=datetime.strptime(time.strip(),'%Y-%m-%d %H:%M')
            time=time_datetime.strftime('%Y-%m-%d')
        except:
            time_datetime=datetime.strptime(time.strip(),'%Y-%m-%d %H:%M:%S')
            time=time_datetime.strftime('%Y-%m-%d')
    else:
        pass
    return time
    
conn=MySQLdb.connect(host='192.168.12.34',user='wxy',passwd='123456',db='spider',charset='utf8')
cursor=conn.cursor()
cursor.execute("select id,sub_id,web_time,web_source,web_name,web_title,web_content,web_comment_list,web_read_num,web_comment_num from news where sub_id=8") 
bo_result=cursor.fetchall()
    
for r in bo_result:
    try:
        if r[8]==None:
            read_num=0
        else:
            read_num=int(r[8].encode('utf-8'))
        if r[9]==None:
            comm_num=0
        else:
            comm_num=int(r[9].encode('utf-8'))
        comment=new_comment(r[7])
        date=newTime(r[2])
        tmp=(r[0],r[1],date,r[3],r[4],r[5],r[6],comment,read_num,comm_num)
        sql="insert into tmp_news(id,sub_id,web_time,web_source,web_name,web_title,web_content,web_comment,web_read_num,web_comment_num) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql,tmp)
        conn.commit()
    except:
        pass
cursor.close()
conn.close() 
"""
# bbs清洗
import MySQLdb
import json
from datetime import datetime
def baTime(time):
    if time!='':
        time_datetime=datetime.strptime(time.strip(),'%Y-%m-%d %H:%M')
        time=time_datetime.strftime('%Y-%m-%d')
    else:
        pass
    return time
def bbs_comment(text):    
    if text!=u'[]':
        comment=[]
        data=json.loads(text)
        for i in range(len(data)):
            if data[i][u'bbs_content']!=u'':
               comment.append(data[i][u'bbs_content'])
        comment=json.dumps(comment,ensure_ascii=False)
        if comment=='[]':
            comment=u''    
    if text==u'[]':
        comment=u''
    return comment  

def baTime(time):
    if time!='':
        time_datetime=datetime.strptime(time.strip(),'%Y-%m-%d %H:%M')
        time=time_datetime.strftime('%Y-%m-%d')
    else:
        pass
    return time
    
conn=MySQLdb.connect(host='192.168.12.34',user='wxy',passwd='123456',db='spider',charset='utf8')
cursor=conn.cursor()
cursor.execute("select id,sub_id,bbs_name,bbs_title,bbs_time,read_num,comment_num,bbs_content,bbs_reply_list from bbs where sub_id=8") 
bo_result=cursor.fetchall()
    
for r in bo_result:
    try:
        date=baTime(r[4])
        if r[5]==u'':
            read_num=0
        else:
            read_num=int(r[5].encode('utf-8'))
        if r[6]==u'':
            comm_num=0
        else:
            comm_num=int(r[6].encode('utf-8'))
        reply=bbs_comment(r[8])
        tmp=(r[0],r[1],r[3],r[2],date,read_num,comm_num,r[7],reply)
        sql="insert into tmp_bbs(id,sub_id,bbs_title,bbs_name,date,read_num,comment_num,bbs_content,bbs_reply) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql,tmp)
        conn.commit()
    except:
        pass
cursor.close()
conn.close() 
