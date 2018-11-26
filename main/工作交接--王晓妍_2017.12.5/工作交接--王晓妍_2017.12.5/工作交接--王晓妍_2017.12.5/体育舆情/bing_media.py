# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 15:02:40 2017

@author: Administrator
"""
# 体育舆情关键词数、媒体数、评论数
import MySQLdb
conn = MySQLdb.connect(host='192.168.12.34',user='wxy',passwd='123456',db='spider',charset='utf8')
cursor = conn.cursor()
cursor.execute("select new_content,name,comments_num from tmp_weibo where sub_id=8")
bo_result = cursor.fetchall()

cursor.execute("select tie_title,tieba_name,reply_num from tmp_tieba where sub_id=8") 
ba_result=cursor.fetchall()

cursor.execute('select web_title,web_name,web_comment_num from tmp_news where sub_id=8')
new_result=cursor.fetchall()

cursor.execute("select content,name,comments_num from tmp_wechat where sub_id=8")
chat_result=cursor.fetchall()
   
cursor.execute("select bbs_content,bbs_name,comment_num from tmp_bbs where sub_id=8")
bbs_result=cursor.fetchall()  
# 关键词数
num_bo,num_ba,num_new,num_chat,num_bbs=0,0,0,0,0
comm_bo,comm_ba,comm_new,comm_chat,comm_bbs=0,0,0,0,0

media_bo,media_ba,media_new,media_chat,media_bbs=[],[],[],[],[]
for r in bo_result:
    media_bo.append(r[1])
    comm_bo +=r[2]
    if u'鸿星' in r[0] or u'比赛' in r[0] or u'联赛' in r[0] or u'冰球' in r[0] or u'KHL' in r[0] or u'昆仑' in r[0] or u'VHL' in r[0] or u'MHL' in r[0] or u'CWHL' in r[0]:
        num_bo +=int(r[2])

for r in ba_result:
    media_ba.append(r[1])
    comm_ba +=r[2]
    if u'鸿星' in r[0] or u'比赛' in r[0] or u'联赛' in r[0] or u'KHL' in r[0] or u'昆仑' in r[0] or u'VHL' in r[0] or u'MHL' in r[0] or u'CWHL' in r[0]:
        num_ba +=int(r[2])
        
for r in new_result:
    media_new.append(r[1])
    comm_new +=int(r[2])
    if u'鸿星' in r[0] or u'比赛' in r[0] or u'联赛' in r[0] or u'KHL' in r[0] or u'昆仑' in r[0] or u'VHL' in r[0] or u'MHL' in r[0] or u'CWHL' in r[0]:
        num_new +=1
        
for r in chat_result:
    media_chat.append(r[1])
    comm_chat +=int(r[2])
    if u'鸿星' in r[0] or u'比赛' in r[0] or u'联赛' in r[0] or u'KHL' in r[0] or u'昆仑' in r[0] or u'VHL' in r[0] or u'MHL' in r[0] or u'CWHL' in r[0]:
        num_chat +=1
        
for r in bbs_result:
    media_bbs.append(r[1])
    comm_bbs +=int(r[2])
    if u'鸿星' in r[0] or u'比赛' in r[0] or u'联赛' in r[0] or u'KHL' in r[0] or u'昆仑' in r[0] or u'VHL' in r[0] or u'MHL' in r[0] or u'CWHL' in r[0]:
        num_bbs +=1
        
print "微博、贴吧、新闻、微信、bbs关键词数分别为:" 
print  (num_bo,num_ba,num_new,num_chat,num_bbs)
print "微博、贴吧、新闻、微信、bbs评论数分别为:" 
print (comm_bo,comm_ba,comm_new,comm_chat,comm_bbs)

# 媒体数
media_bo=len(set(media_bo))
media_ba=len(set(media_ba))
media_new=len(set(media_new))
media_chat=len(set(media_chat))
media_bbs=len(set(media_bbs))
print "微博、贴吧、新闻、微信、bbs媒体数分别为：" 
print  (media_bo,media_ba,media_new,media_chat,media_bbs)



