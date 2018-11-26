# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 18:50:34 2017

@author: Administrator
"""

# 用户画像分析
import MySQLdb
import pandas as pd
import json

conn=MySQLdb.connect(host='192.168.12.34',user='wxy',passwd='123456',db='spider',charset='utf8')
cursor=conn.cursor()
cursor.execute("select id,province,sex,tag,summary from tmp_weibo where sub_id=7")
bo_result=cursor.fetchall()

sex,area,tag=[],[],[]
for r in bo_result:
    if r[1]!=None:
        area.append(r[1])
    if r[2]!=None:
        sex.append(r[2])    
    if r[3]!=u'':
        tag.append(r[3])
    if r[4]!=u'':
        tag.append(r[4])        
            
sex_ = pd.Series(sex).value_counts()
area_ = pd.Series(area).value_counts()
print "网民性别分布:" % sex_
#print "网民地域分布:\n%s" % area_

sex_j={}
sex_j['男']=sex_[0]
sex_j['女']=sex_[1]

area_j={}
for i in range(len(area_)):
    area_j[area_.keys()[i].encode('utf8')]=int(area_[i])
        
    
source3=open('data/figure.txt','w')
source3.write(json.dumps(area_j,ensure_ascii=False)) 
source3.close()

# 兴趣标签
import jieba
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud,ImageColorGenerator
from PIL import Image

tag=list(set(tag)) 
stopword=[line.strip().decode('utf8') for line in open('D:\\study\\dictionary\\stopword.txt').readlines()]
def wordCount(file): 
    bow=[]
    for i in tag:
        if i!=None:
            n=set(jieba.cut(i,cut_all=False))-set(stopword)
            bow.append(list(n))
    
    word_l=[]
    for i in range(len(bow)):
        #fout.write(str(bow[i]))#显示的是unicode
        if len(bow[i])!=0:
            for j in range(len(bow[i])):
                word_l.append(bow[i][j])
    wordCount={}
    for word in word_l:
        if word in wordCount.keys():
            wordCount[word]=wordCount[word]+1
        else:
            wordCount[word]=1
    return [(k,wordCount[k]) for k in wordCount.keys()]
#print wordCount(path)            

def generateCloud(filename,imagename,cloudname,fontname):  
   alice = np.array(Image.open(imagename))            # 读取背景图片  
   wc = WordCloud(background_color="white", # 背景颜色max_words=2000,# 词云显示的最大词数  
               mask=alice,            # 设置背景图片  
               stopwords=stopword,      # 停止词  
               font_path=fontname,       # 兼容中文字体  
               max_font_size=150)        # 字体最大值  
       
        #txtFreq例子为[('词a', 100),('词b', 90),('词c', 80)]  
   txtFreq = wordCount(filename)  
   wc.generate_from_frequencies(txtFreq)  
        # 生成图片  
   img_color = ImageColorGenerator(np.array(Image.open(imagename)))#颜色与原图片一样
   plt.imshow(wc.recolor(color_func=img_color))  
   plt.axis("off")  
        # 绘制词云  
   plt.figure()  
        # 保存词云  
   wc.to_file(cloudname)  

if __name__ == '__main__':  
      # 获取当前文件路径  
    fontname = 'D://tool//simhei.ttf'    # 中文字体路径  
    filename = tag      # txt文件路径  
    imagename = 'E:\\record\\go\\weibo.jpg' # 背景图片路径  
    cloudname = 'E:\\record\\service2\\title.png'  # 标签云路径  
    generateCloud(filename,imagename, cloudname,fontname) 