# -*- coding: utf-8 -*-
"""
Created on Wed May 24 15:38:34 2017
信息来源、时间走势、网友画像、关键词曝光、媒体价值分析
@author: 晓妍
"""
import happybase
import pandas as pd
from datetime import datetime
import json
import numpy as np
from datetime import timedelta
import charts
import pygal

# 时间清洗为‘1900-01-01’的格式
def cleanTime(time):
    if time!='':
        try:
            time_datetime=datetime.strptime(time.strip(),'%Y-%m-%d')
            time=time_datetime.strftime('%Y-%m-%d')
        except ValueError:
            time_datetime=datetime.strptime(time.encode('utf8'),'%Y年%m月%d日')
            time=time_datetime.strftime('%Y-%m-%d')
    else:
        pass
    return time

# 贴吧带时间的日期 清洗为‘1900-01-01’的格式    
def tiebaTime(time):
    if time!='':
        time_datetime=datetime.strptime(time.strip(),'%Y-%m-%d %H:%M')
        time=time_datetime.strftime('%Y-%m-%d')
    else:
        pass
    return time

# 根据时间区分赛前、赛中、赛后文章数
def duration(time):
    a1,b1,c1=0,0,0
    for i in time:
        if i<'2016-12-24':
            a1 +=1
        elif i >='2016-12-24' and i <= '2017-03-09':
            b1 +=1
        elif i>'2017-03-09':
            c1 +=1
    return a1,b1,c1

# 根据生日确定是60、70、80、90还是00后
def age_dur(birth):
    a1,b1,c1,d1,e1=0,0,0,0,0    
    for i in birth:
        try:
            if i >= '1960-01-01' and i <= '1969-12-31':
                a1 +=1
            elif i >= '1970-01-01' and i <= '1979-12-31':
                b1 +=1
            elif i >= '1980-01-01' and i <= '1989-12-31':
                c1 +=1 
            elif i >= '1990-01-01' and i <= '1999-12-31':
                d1 +=1
            elif i >= '2000-01-01' and i <= '2025-12-31':
                e1 +=1
            else:
                pass                
        except ValueError:
            pass
    return a1,b1,c1,d1,e1

#时间序列 从开始报名到结束统计      
date_list=[]
begin_date = datetime.strptime('2016-11-28', "%Y-%m-%d")
end_date = datetime.strptime('2017-04-30', "%Y-%m-%d")
while begin_date <= end_date:
    date_str = begin_date.strftime("%Y-%m-%d")
    date_list.append(date_str)
    begin_date += timedelta(1)
    
# 每个日期的文章数
def time_num(time_s):
    num=np.zeros(len(date_list))
    for i in range(len(date_list)):
        for j in range(len(time_s)):
            if date_list[i]==time_s.keys()[j]:
                num[i]=time_s[j]
            else:
                pass 
    return num        

# 标题中关键词的曝光数    
def keyword(word,title):
    num=np.zeros(len(word))
    for i in range(len(title)):
        for j in range(len(num)):
            if word[j].encode('utf8') in title[i]:
                num[j] +=1            
    return num

#地名清洗 根据市给出省份
def place(name):
    data = pd.read_csv('../location.csv', sep=',',encoding='gbk')
    for i in range(len(data)):
        if name[:2] in data['city'][i]:
            name=data['province'][i]
        else:
            pass
    
    return name
    
# 新闻网站清洗    
def new_name_clean(name):
    name=name.replace('新华社','新华网')
    name=name.replace('中新网','中国新闻网')
    name=name.replace('•','')
    name=name.replace(' ','')
    name=name.replace('弈城围棋网mp','弈城围棋网')
    return name
    
if __name__ == '__main__':
    conn = happybase.Connection('192.168.10.24',timeout=300000)
    table=conn.table('public_sentiment')
    
#每个渠道文章数分布
    title_new=[]
    for key,data in table.scan(row_prefix='嫘祖杯01',columns=['d:title']):
        title_new.append(data.values()[0])
    
    
    title_wechat=[]
    for key,data in table.scan(row_prefix='嫘祖杯03',columns=['d:title']):
        title_wechat.append(data.values()[0])
    
    title_weibo=[]
    for key,data in table.scan(row_prefix='嫘祖杯02',columns=['d:content']):
        title_weibo.append(data.values()[0])
    
    title_ba=[]
    for key,data in table.scan(row_prefix='嫘祖杯05',columns=['d:tie_title']):
        title_ba.append(data.values()[0])    
    
# 信息来源分布饼图
    series=[{
             'type':'pie',             
             'data':[
                ['新闻',len(title_new)],
                ['微信',len(title_wechat)],
                ['微博',len(title_weibo)],
                ['贴吧',len(title_ba)]
            ]
        }]
    options={
         'title':{'text':'信息来源分布'},
         'plotOptions':{'pie':{'dataLabels':{'enabled':True,'format':'{point.name}:<b> {point.percentage:.1f} %</b>'
                        }
                    }              
        }
        }
    #charts.plot(series,options=options)

    
# 时间走势
    time1=[]
    for key,data in table.scan(row_prefix='嫘祖杯01',columns=['d:time']):
        for i in data.values():
            time1.append(cleanTime(i))
    time_new=pd.Series(time1).value_counts()
    dur_new=duration(time1) 
     
        
    time2=[]
    for key,data in table.scan(row_prefix='嫘祖杯02',columns=['d:time']):
        for i in data.values():
            time2.append(i)
    time_weibo=pd.Series(time2).value_counts()
    dur_weibo=duration(time2) 
    
    
    time3=[]
    for key,data in table.scan(row_prefix='嫘祖杯03',columns=['d:time']):
        for i in data.values():
            time3.append(cleanTime(i))
    time_wechat=pd.Series(time3).value_counts()
    dur_wechat=duration(time3) 
    
    time5=[]
    for key,data in table.scan(row_prefix='嫘祖杯05',columns=['d:tie_time']):
        for i in data.values():
            time5.append(tiebaTime(i))
    time_ba=pd.Series(time5).value_counts()    
    dur_ba=duration(time5) 
    
    series_t=[
        {'name':'新闻',
         'data':list(time_num(time_new)),
         'type':'line'},
        {'name':'微信',
         'data':list(time_num(time_wechat)),
         'type':'line'},
        {'name':'贴吧',
         'data':list(time_num(time_ba)),
         'type':'line'},         
         {'name':'微博',
         'data':list(time_num(time_weibo)),
         'type':'line'}
        ]
    options_t={
             'title':{'text':'时间走势'},
             'xAxis':{'categories':date_list}
             
    }
    
    #charts.plot(series_t,options=options_t)
    
    print "赛前新闻、微博、微信、贴吧文章数分别为：%s,%s,%s,%s" % (dur_new[0],dur_weibo[0],dur_wechat[0],dur_ba[0])
    print "赛中新闻、微博、微信、贴吧文章数分别为：%s,%s,%s,%s" % (dur_new[1],dur_weibo[1],dur_wechat[1],dur_ba[1])
    print "赛后新闻、微博、微信、贴吧文章数分别为：%s,%s,%s,%s" % (dur_new[2],dur_weibo[2],dur_wechat[2],dur_ba[2])

    series1=[{
             'type':'pie',             
             'data':[
                ['新闻',dur_new[0]],
                ['微信',dur_wechat[0]],
                ['微博',dur_weibo[0]],
                ['贴吧',dur_ba[0]]
            ]
    }]
    options1={
         'title':{'text':'赛前信息来源分布'},
         'plotOptions':{'pie':{'dataLabels':{'enabled':True,'format':'{point.name}:<b> {point.percentage:.1f} %</b>'
                        }
                    }              
        }
        }   
    #charts.plot(series1,options=options1)

    series2=[{
             'type':'pie',             
             'data':[
                ['新闻',dur_new[1]],
                ['微信',dur_wechat[1]],
                ['微博',dur_weibo[1]],
                ['贴吧',dur_ba[1]]
            ]
    }]
    options2={
         'title':{'text':'赛中信息来源分布'},
         'plotOptions':{'pie':{'dataLabels':{'enabled':True,'format':'{point.name}:<b> {point.percentage:.1f} %</b>'
                        }
                    }              
        }
        }
    #charts.plot(series2,options=options2)
    
    series3=[{
             'type':'pie',             
             'data':[
                ['新闻',dur_new[2]],
                ['微信',dur_wechat[2]],
                ['微博',dur_weibo[2]],
                ['贴吧',dur_ba[2]]
            ]
    }]
    options3={
         'title':{'text':'赛后信息来源分布'},
         'plotOptions':{'pie':{'dataLabels':{'enabled':True,'format':'{point.name}:<b> {point.percentage:.1f} %</b>'
                        }
                    }              
        }
        }    
    #charts.plot(series3,options=options3)
    
# 网民性别、地区、年龄,地图可用RemapC 看怎么调用
    sex=[]
    area=[]
    age=[]
    for key,data in table.scan(row_prefix= '嫘祖杯02',columns=['d:info']):
        for i in data.values():
                 j=json.loads(i)
                 if j['sex']!=None:
                     sex.append(j['sex'])
                 if j['area']!=None:
                     area.append(place(j['area'].split(' ')[0]))
                 if j['birth']!=None:
                     age.append(j['birth'])
    
    for key,data in table.scan(row_prefix='嫘祖杯01',columns=['d:comment_list']):
        for i in data.values():
            j=json.loads(i)
            for k in range(len(j)):
                if 'area' in j[k].keys():
                    area.append(place(j[k]['area']))
            
            
    sex_ = pd.Series(sex).value_counts()
    area_ = pd.Series(area).value_counts()
    print "网民性别分布:\n%s" % sex_
    print "网民地域分布:\n%s" % area_
    print "网民中60后、70后、80后、90后、00后的人数分别为：" 
    print age_dur(age)[0],age_dur(age)[1],age_dur(age)[2],age_dur(age)[3],age_dur(age)[4]
    
        
    series4=[{
             'type':'pie',             
             'data':[
                ['60后',age_dur(age)[0]],
                ['70后',age_dur(age)[1]],
                ['80后',age_dur(age)[2]],
                ['90后',age_dur(age)[3]],
                ['00后',age_dur(age)[4]]
            ]
    }]
    options4={
         'title':{'text':'年龄分布'},
         'plotOptions':{'pie':{'dataLabels':{'enabled':True,'format':'{point.name}:<b> {point.percentage:.1f} %</b>'
                        }
                    }              
        }
        }
    charts.plot(series4,options=options4)
    
    #标题中关键词曝光    
    word=[u'嫘祖',u'祭祖',u'盐亭',u'绵阳']   
    for i in range(len(word)):
        a=keyword(word,title_new)[i]+keyword(word,title_wechat)[i]+keyword(word,title_weibo)[i]+keyword(word,title_ba)[i]
        print "关键词:%s" % word[i],"出现总次数为:%s" % a,"新闻出现次数为：%s" % keyword(word,title_new)[i],"微信出现次数为：%s" % keyword(word,title_wechat)[i],"微博出现次数为：%s" % keyword(word,title_weibo)[i],"贴吧出现次数为：%s" % keyword(word,title_ba)[i]
    key_new=0                # 新闻中关键词曝光总次数
    key_weibo=0              # 微博中关键词曝光总次数
    key_wechat=0
    key_ba=0
    for i in range(len(word)):
        key_new +=keyword(word,title_new)[i]
        key_weibo +=keyword(word,title_weibo)[i]
        key_wechat +=keyword(word,title_wechat)[i]
        key_ba +=keyword(word,title_ba)[i]
        
    radar_chart=pygal.Radar()
    radar_chart.x_labels=word
    radar_chart.add(u'新闻',[keyword(word,title_new)[0],keyword(word,title_new)[1],keyword(word,title_new)[2],keyword(word,title_new)[3]])    
    radar_chart.add(u'微博',[keyword(word,title_weibo)[0],keyword(word,title_weibo)[1],keyword(word,title_weibo)[2],keyword(word,title_weibo)[3]])    
    radar_chart.add(u'微信',[keyword(word,title_wechat)[0],keyword(word,title_wechat)[1],keyword(word,title_wechat)[2],keyword(word,title_wechat)[3]])    
    radar_chart.add(u'贴吧',[keyword(word,title_ba)[0],keyword(word,title_ba)[1],keyword(word,title_ba)[2],keyword(word,title_ba)[3]])    
    radar_chart.render_to_file('hello.svg')

# 微博账号数与粉丝数
    name_weibo=[]
    fensi_weibo=[]
    for key,data in table.scan(row_prefix='嫘祖杯02',columns=['d:info']):
        for i in data.values():
            j=json.loads(i)
        if j['name'] not in name_weibo:                           
                fensi_weibo.append(eval(j['fensi']))
                name_weibo.append(j['name'])
        else:
                pass  
    weibo_fen={'name':name_weibo,'fensi':fensi_weibo}
    wei_fensi = pd.DataFrame(weibo_fen,columns=['name','fensi']) 
    a=wei_fensi.sort_values(by='fensi',ascending=False)[:10]
    print "微博粉丝数Top10:\n%s" % a
    fennum_weibo=0                       # 微博粉丝总数 
    for i in range(len(fensi_weibo)):
        if fensi_weibo[i]:
            fennum_weibo +=fensi_weibo[i]

#微博粉丝数条形图,展示不全，改柱图，但显示不全 
    
    name=[]
    for i in a['name']:
        name.append(i)
    fensi=[]
    for j in a['fensi']:
        fensi.append(j)
    list=[]
    for i in range(len(name)):
        data1={
              'name':name[i],
              'data':[fensi[i]],
              'type':'column'
        }
        list.append(data1)

    options_f={
             'title':{'text':'微博粉丝数排行Top'},
                      'plotOptions':{'column':{'dataLabels':{'enabled':True}}}
             }
                  
    #charts.plot(list,options=options_f) 
   
# 微信公众号数与粉丝数    
    name3=[]
    fensi3=[]
    name_wechat=[]
    fensi_wechat=[]
    for key,data in table.scan(row_prefix='嫘祖杯03',columns=['d:name']):
        for i in data.values():
            name3.append(i)

    for key,data in table.scan(row_prefix='嫘祖杯03',columns=['d:fans_num_estimate']):
        for i in data.values(): 
            fensi3_str=i.replace('万','0000')
            fensi3.append(eval(fensi3_str))

    for k in range(len(name3)):
        if name3[k] not in name_wechat:
            name_wechat.append(name3[k])
            fensi_wechat.append(fensi3[k])
        else:
            pass
    fennum_wechat=0
    for i in range(len(fensi_wechat)):
        if fensi_wechat[i]:
            fennum_wechat +=fensi_wechat[i]     

# 新闻媒体数与传播力度         
    name_new=[]
    for key,data in table.scan(row_prefix='嫘祖杯01',columns=['d:web_name']):
        for i in data.values():
            name_new.append(new_name_clean(i))              
    

    fennum_new=0
    table1=conn.table('web_traffic')
    for key,data in table1.scan(columns=['d:uv']):
        for i in data.values():
            j=json.loads(i)
            fennum_new +=j['trimester']
    fennum_new=fennum_new*0.1 # 因为有子网站 所以以三月日均uv的10%粗略作为粉丝数    
        
    print "新闻、微博、微信、贴吧媒体数分别为:%s,%s,%s,%d" % (len(set(name_new)),len(name_weibo),len(name_wechat),5)      
    print "新闻、微博、微信、贴吧传播范围:%s,%s,%s,%d" % (fennum_new,fennum_weibo,fennum_wechat,157055)
    print "新闻、微博、微信、贴吧曝光关键词数:%s,%s,%s,%s" % (key_new,key_weibo,key_wechat,key_ba)
    print "新闻、微信、微博、贴吧文章数分别是：%s,%s,%s,%s" % (len(title_new),len(title_wechat),len(title_weibo),len(title_ba))
    
    
    
    
    