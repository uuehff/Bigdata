# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 15:52:34 2017
刑事二审字段提取1：包括尾部、新的court_idea、新的judge_result、检察院、审判长、是否无罪|剥夺政治权利|自首|累犯|未遂、关联uuid
注 更新完history分隔符改完||
@author: wxy
"""

import MySQLdb 
import re
from datetime import datetime
import xlrd

def read_location_xcel(path):
    data = xlrd.open_workbook(path)
    table = data.sheet_by_name("sheet")
    result_list = []
    for i in range(0,table.nrows):
        row_content = table.row_values(i,0,table.ncols)
        result_list.append(row_content)
    return result_list

city_list, dis_list, prov_list,place_list = [],[],[],[]
location_list = read_location_xcel("E:/record/law_data_2/location_law.xlsx")#E:/record/law_data_2/

def clean_place(name,org):
    place=name
    str=[u'中华人民共和国',u'暨附带民事诉讼原告人',u'暨刑事附带民事诉讼原告人',u'暨提起附带民事诉讼机关',u'暨附带民事诉讼原告人',u'暨附带民事诉讼原告',u'暨代表国家提起附带民事诉讼原告人']
    #选诉讼机关及原告人以后的
    for s in str:
        place=place.replace(s,u'')

    if u'某' in place or u'×' in place or u'X' in place or u'□' in place:
        place=u''
    place=re.sub(ur'[^\u4e00-\u9fa5]',u'',place)
    if len(place) > 0:
        location_pattern = re.compile(u'(?P<province>[\u4e00-\u9fa5]{2,10}?(?:省|自治区)){0,1}'
                                u'(?P<city>[\u4e00-\u9fa5]{2,10}?(?:市|州|盟 |地区)){0,1}'
                                u'(?P<district>[\u4e00-\u9fa5]{1,10}(?:市|区|开发区|县|自治县|旗)){0,1}')
        location_result = re.search(location_pattern, place)
        province = location_result.group("province")
        city = location_result.group("city")
        district = location_result.group("district") 
        s=[u'白云区',u'宝山区',u'朝阳区',u'城关区',u'城郊地区',u'城区',u'城中区',u'东宁县',u'高新技术产业开发区',u'鼓楼区',u'海州区',u'和平区',u'河东区',u'江北区',u'郊区',u'经济技术开发区',u'矿区',u'南山区',u'普陀区',u'桥东区',u'桥西区',u'青山区',u'清河区',u'市中区',u'铁东区',u'铁西区',u'通州区',u'西安区',u'西湖区',u'向阳区',u'新城区',u'新华区',u'新市区',u'宣恩县',u'永定区',u'长安区']                
        for item in location_list:
            if city!=None:
                if city==item[1] and district==item[2]:
                    place = item[3]+org                    
                elif city==item[0] and district==item[2]:
                    place=item[3]+org                    
                elif city==item[2]:
                    place = item[3]+org
            elif city==None:
                if province==None and district==item[2]:
                    if district not in s:
                        place=item[3]+org          
                if province==item[0] and district==item[2]:
                    place=item[3]+org                                        
    if place=='':
        place=u''
    if len(name)==0:
        place=u''
    return place
#print clean_place(u'广东省中山市中级人民法院',u'人民法院')
#print clean_place(u'甘肃省金昌市中级人民法院',u'人民法院') #甘肃省嘉峪关市金昌市人民法院

   
def clean_date(time):
    try:
        date1 = datetime.strptime(time,'%Y-%m-%d').date()
        now = datetime.now().date()
        if (now-date1).days <0:
            date1=''
        year=date1.year
        month=date1.month
        day=date1.day
        date=date1.strftime('%Y-%m-%d')
        if month in range(1,13) and day in range(1,32) and year in range(1970,2020):
            pass
        else:
            date=''
    except:
        date=''    
    return date.decode('utf8')
    
#审判长、审判员、尾部来自judge_result   
def judge_chief_member(sf):
    if sf!=None:
        sr=[u'\\n',u'&nbsp；',u'',u'?',u'+']
        s=sf
        for i in sr:
            s=s.replace(i,u'')
        s1=sf
        sb=[u'&nbsp；',u'',u'?',u'+']
        for i in sb:
            s1=s1.replace(i,u'')
        pattern1=re.compile(ur"(?<=审判长)([\u4e00-\u9fa5]*?)(?=审理员|本件与|代理审判员|代理判判员|审判员|助理审判员|代审员|二〇|一九|人民陪审员|陪审员|代理陪审员|裁判员|人民审判员)") 
        pattern2=re.compile(ur"(审判员|代理审判员|代理判判员|助理审判员|代审员)([\u4e00-\u9fa5]+)(?=书记员|二〇|二○|二0|二?|二一|二O|二０|二Ｏ|法官助理|一九|人民陪审员|陪审员|审判长)")
        pattern3=re.compile(ur"(?:副庭长|庭长|主审法官|法官助理|助理执行员|审判长|审判员|代审判|代理审判)([\s\S]*?)(?=声明|附法律|附相关|附：|附引用|附本判决|附判决|附动产|公章法院|附本案|发改（|《中华|法条|本案|附:|本裁定|本件与|（本页|本文|附有关|相关|本刑事|附适用|适用|附告|附表|当事人|本判决|附录|附页|附判决|附裁判|附1|附本|附二审|（附上诉|附一|刑事判决|相关|相关法律|法律|附所适用|扣押|本裁判|所引用|附注|所适用|附件|判决书|附裁定|附主要|主要法|附清单|附上诉|附证据|附相关|附赔偿|附释|附与|附援|附相应|附依据|附原告|附裁决|附转换|附依据|附案件|附利息|附执行|附据以|附民事|附参考|附计算|附带|附所援引|附刑法|附（)")
        pattern4=re.compile(ur"(?:副庭长|庭长|助理执行员|主审法官|法官助理|审判长|审判员|代审判|代理审判)([\s\S]*)")
        f=re.search(pattern1,s)
        g=re.search(pattern2,s)
        h=re.search(pattern3,s1)
        k=re.search(pattern4,s1)
        if f:
            judge_chief=f.group()
            judge_chief=judge_chief.replace(u'审判长',u'||')

        else:
            judge_chief=u''
        if h:
            foot=h.group()
        else:
            if k:
                foot=k.group()
            else:
                foot=u''   
        
        if g:
            judge_member=g.group(2)
            h=[u'代判理审员',u'审员员',u'代理审审员',u'代理审理员',u'代理陪审员',u'助理审判员',u'代理审判员',u'审判员']
            for i in h:
                judge_member=judge_member.replace(i,u'||')
        else:
            judge_member=u''
    else:
        judge_chief=u''
        judge_member=u''
        foot=u''
    return judge_chief,judge_member,foot
#print judge_chief_member(u'审判员范君义\n二〇一四年五月二十一日\n书记员许云翔\n附相应的')[2]
#print judge_chief_member(u'以前先行羁押的，羁押一日折抵刑期一日。即自2015年10月1日起至2018年9月30日止。罚金刑限本判决宣告或者送达后三十日内缴纳）\n本判决为终审判决。\n审&nbsp；判&nbsp；长&nbsp；靳&nbsp；&nbsp；&nbsp；皓\n代理审判员&nbsp；刘贵波\n代理审判员&nbsp；陈&nbsp；&nbsp；&nbsp；波\n二〇一六年五月二十五日\n书&nbsp；记&nbsp；员&nbsp；蔡成成') 
#print judge_chief_member(u'判决为终审判决。\n审判长钟彬\n审判员张玉军\n代理审判员梁云\n二○二○一七年一月三日\n书记员李蕙\n速录员钟中')
#print judge_chief_member(u'毫然犯聚众斗殴罪，判处有期徒刑一年六个月，缓刑一年六个月。\n二、撤销北京市海淀区人民法院（2016）京0108刑初561号刑事判决第三项，即被告人蒋天军犯聚众斗殴罪，判处有期徒刑二年，缓刑二年六个月。\n三、原审被告人蒋天军犯聚众斗殴罪，判处有期徒刑二年。\n（刑期从判决执行之日起计算，判决执行以前先行羁押的，羁押一日折抵刑期一日，即自2016年10月20日起至2018年9月25日止。）\n本判决为终审判决。\n审?判?长???杨跃进\n审?判?员???赖?琪\n代理审判员\n仇芳芳\n二〇一六年十月二十日\n书?记?员???索?探')

# 检查院来自party_info
def party(text,process):
    patt0=re.compile(ur"(公诉机关|抗诉机关|原公诉）机关)(.*?)(检察院)")
    a=re.search(patt0,text)
    if a:
        doc_o=a.group(2)+a.group(3)
        doc_o=doc_o.replace(u'（原公诉机关）',u'')
        doc_o=doc_o.replace(u'（原审公诉机关）',u'')
        doc_o=doc_o.replace(u'（抗诉机关）',u'')
        doc_o=doc_o.replace(u'（原诉机关）',u'')
        doc_o=doc_o.replace(u'（一审公诉机关）',u'')
        doc_o=doc_o.replace(u'：',u'')
    else:
        patt1=re.compile(ur"(?<=法院审理)[\u4e00-\u9fa5]+?(?:检察院)")
        b=re.search(patt1,process)
        if b:
            doc_o=b.group()
        else:
            doc_o=u''
    return doc_o
   
# court_idea_new,judge_result_new 来自court_idea,judge_result
def new_idea(text):
    patt0=re.compile(ur"([\s\S]*)(?=依照《|综上，《中华|综上所述，《中华人民|综上，依《中华|据此，|依照，《|据此《中|依据中华人民共和国|综上《中华|依照最高|按照《中|依据最高|根据最高|根据《|依据《)")
    if text!=None:
        d=re.search(patt0,text)
        if d:
            if u'。' in d.group(): #可能依据法条前没有句号
                s=d.group().split(u'。')
                b=u''
                for i in s[:-1]:
                    b +=i+u'。'
            else:
                b=d.group()
    
        else:
            b=text
    else:
        b=u''
    return b

def new_result(idea,result):
    if idea==None:
        res=result
        idea=u''
    if result==None:
        result=u''
        res=u''
    sb=[u'&nbsp；',u'',u'?',u'+']
    for i in sb:
        result=result.replace(i,u'')
    patt0=re.compile(ur"(依照《|综上，《中华|综上所述，《中华人民|综上，依《中华|据此，|依照，《|据此《中|依据中华人民共和国|综上《中华|依照最高|按照《中|依据最高|根据最高|根据《|依据《)([\s\S]*)(判决如下：|判决如下:|判决：|裁定如下：|裁定如下:)")
    patt1=re.compile(ur"([\s\S]*?)(?=书记员|副庭长|庭长|助理执行员|主审法官|法官助理|审判长|审判员|代理审判|代审判)")  
    d=re.search(patt0,idea)
    c=re.search(patt1,result)
    if d:
        if c:
            res=d.group()+u'\n'+c.group()
        else:
            res=d.group()+u'\n'+result
    else:
        if c:
            res=c.group()
        else:
            res=result
    return res 
# 提取刑事及民事案件中的公司
def org_name(org):
    org_b=u''
    if org!=[]:
        for i in range(len(org)):
            s=[u'公司',u'合作社',u'信用社',u'电视台',u'委员会',u'村委会',\
            u'服务',u'经济社',u'水库',u'中心',u'酒店',u'厂',u'办公室',\
            u'医院',u'农村信用',u'政府',u'局',u'处',u'银行',u'所',u'站',u'会所',u'部队']
# u'办事处'，u'食品站',u'供热站',u'供应站'
            for j in s:
                if j in org[i][1] and len(org[i][1])>4:  
                    if u'某' not in org[i][1] and u'判处' not in org[i][1] and u'不服' not in org[i][1]:
                        a=org[i][1]
                        if u'人' in a[:1]:                        
#and u'代表' not in org[i][1] and u'负责' not in org[i][1] and u'员工' not in org[i][1] and u'经理' not in org[i][1] and u'主任' not in org[i][1]:
                            org_b +=a[1:] + u'||'
                        if u'单位' in a[:2]:
                            org_b +=a[2:]+u'||'
                        else:
                            org_b +=a+u'||'
                        
        org_b=org_b[:-2]
    else:
        pass
    return org_b

# 原告及被告公司
def organization(name):
    patt1=re.compile(ur'(一审原告）|诉讼原告人）|反诉被告）|反诉被告）：|原告|原告人|原告：|一审原告）：|原审原告）|原审原告）：)([\u4e00-\u9fa5]*?)(，|。|,|（)')  
    org1=re.findall(patt1,name.replace(u')',u'）'))
        # 被告公司  
    patt0=re.compile(ur'(原审被告人）|反诉原告）|反诉原告）：|被告|被告人|被告：|原审被告）：|原审被告）|一审被告）|一审被告）：|诉讼被告）|诉讼被告人）|诉讼被告）：|被告单位）|被告单位)([\u4e00-\u9fa5]*?)(，|。|,|（)')
    org0=re.findall(patt0,name.replace(u')',u'）'))
    a=org_name(org1)
    b=org_name(org0)
    return a,b

# 争议焦点
def contro(idea):
    patt=re.compile(ur'(争议焦点|争议的焦点)([\s\S]*?)(。|？\n|争议焦点|本院)')   
    #争议焦点为：|争议焦点：|争议焦点是|争议焦点是：|争议焦点如下：|争议的焦点是：|争议的焦点是，|争议焦点|争议焦点在于|争议焦点在于：|争议焦点包括|争议焦点包括：|争议焦点涉及|争议焦点主要|争议焦点问题：)([\s\S]*?)(。|？)')   
    g=re.search(patt,idea)    
    if g:
        a=g.group(2)
        s=[u'为',u'：',u'是',u'，',u'如下',u'在于',u'包括',u'涉及',u'以下',u'两点',u'问题',u'有',u'二',u'主要']
        for i in s:        
            if i in a[:2]:
                a=a.replace(i,u'')
        a=a.replace(u'：',u'')
        if len(a)>3:
            contro=a+g.group(3)
        else:
            contro=u''
        if u'评判' in contro[:5] or u'分析' in contro[:5] or u'本院' in contro[:5]:
            contro=u''            
    else:
        contro=u''
    return contro 
    
def clean_his(uuid,history):
    his_n=''
    if len(history)!=0:
        a=history.replace(u'["',u'')
        a=a.replace(u'"]',u'')
        a=a.replace(u'", "',u'||')
        for i in a.split(u'||'):
            if i not in uuid:
                his_n +=i+u'||'
        his_n=his_n[:-2]
    else:
        pass
    return his_n  
#print clean_his(results[0][1],results[0][8])[0]
    
conn=MySQLdb.connect(host='192.168.12.34',user='wxy',passwd='123456',db='laws_doc2',charset='utf8')
cursor=conn.cursor()

"""
#有问题的调试
cursor.execute("select id,uuid,party_info,trial_process,trial_request,court_find,court_idea,judge_result,history,court,casedate,title from judgment where judge_type='%s' and uuid='%s'" % (u'判决',u'f44e6d2a-e6d6-46cd-a069-a775010d257e'))
r=cursor.fetchone()

judge_chief=judge_chief_member(r[7])[0]
foot=judge_chief_member(r[7])[2]
court_idea=new_idea(r[6])
judge_result = new_result(r[6],r[7])        
history=r[8]
casedate=clean_date(r[10])
court=clean_place(r[9],u'人民法院')
org_plaintiff=organization(r[2])[0]
org_defendant=organization(r[2])[1]
contro0=contro(r[6])

print len(org_plaintiff),len(org_defendant)
""" 
# 民事更新了 判决书完事更新裁定书
a=0
b=50000
c=0
while a < 40000: 
    cursor.execute("select id,uuid,party_info,trial_process,trial_request,court_find,court_idea,judge_result,history,court,casedate,title from judgment2 where is_format=1 limit %s,%s" % (a,b))
    results=cursor.fetchall()
    for r in results:
        judge_chief=judge_chief_member(r[7])[0]
        #judge_member=judge_chief_member(r[7])[1]
        foot=judge_chief_member(r[7])[2]
        #print foot        
        doc_b=clean_place(party(r[2],r[3]),u'人民检察院') #检察院
        court_idea=new_idea(r[6])
        judge_result = new_result(r[6],r[7])        

        #print "doc_oriligation:%s" % doc_b
        #print "court_idea:%s" % court_idea[-50:]
        #print "judge_result:%s" % judge_result[:50]
        history=clean_his(r[1],r[8])       
        casedate=clean_date(r[10])
        court=clean_place(r[9],u'人民法院')
        org_plaintiff=organization(r[2])[0]
        org_defendant=organization(r[2])[1]
        contro0=contro(r[6])
        """  
            # 民事插入
        tmp=(r[0],r[1],judge_chief,foot,court_idea,judge_result,history,\
                 court,casedate,org_plaintiff,org_defendant,r[11],contro0)
        sql="insert into tmp_wxy(id,uuid,judge_chief_new,doc_footer,\
            court_idea_new,judge_result_new,history_new,\
            court_new,casedate_new,org_plaintiff,org_defendant,title,dispute) VALUES \
            (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql,tmp)
        conn.commit()
        """             
            # 刑事二审插入
        if u'自首' in r[6]:
                if_surrender=1
        else:
                if_surrender=0
        if u'累犯' in r[6]:
                if_accumulate=1
        else:
                if_accumulate=0
        if u'未遂' in r[6]:
                if_nosuccess=1
        else:
                if_nosuccess=0
        if u'无罪' in r[7]:
                if_guity=1
        else:
                if_guity=0
        if u'剥夺政治权利' in r[7]:
                if_right=1
        else:
                if_right=0   
        type_new=1
        tmp=(r[0],r[1],type_new,judge_chief,foot,court_idea,judge_result,history,doc_b,\
                 court,casedate,org_plaintiff,org_defendant,r[11],contro0,\
                 if_surrender,if_accumulate,if_nosuccess,if_guity,if_right)
        sql="insert into tmp_wxy(id,uuid,type,judge_chief_new,doc_footer,\
            court_idea_new,judge_result_new,history_new,doc_oriligation_new,\
            court_new,casedate_new,org_plaintiff,org_defendant,title,dispute,\
            if_surrender,if_accumulate,if_nosuccess,if_guity,if_right) VALUES \
            (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"               
        cursor.execute(sql,tmp)
        conn.commit()
        
        c +=1
    a +=500000

    



