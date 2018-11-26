# -*- coding: utf-8 -*-

from  pyspark import SparkContext,SparkConf
from pyspark.sql import SQLContext
from pyspark.sql.types import *
import os
import time

import re
if __name__ == "__main__":

    conf = SparkConf()
    sc = SparkContext(conf=conf)
    sqlContext = SQLContext(sc)

    # PYSPARK_PYTHON = "C:\\Python27\\python.exe"    #多版本python情况下，需要配置这个变量指定使用哪个版本
    # os.environ["PYSPARK_PYTHON"] = PYSPARK_PYTHON

    def p(x):
        print type(x),type(x[0]),type(x[1])
        # print type(x)
        # print type(x[0]),type(x[1])
        print x[0],x[1][0],x[1][1]
    def filter_(x):
        if x[1] and x[1] != '':       #过滤掉数据库中，lawlist为Null或''的行。
            return True
        return False

    def extact_reason(x):
        # if x and x != '':
        uid_l = x.split("||")
        return uid_l

    def get_uuids(uuids):
        l = []
        for x in uuids:
            l.append(x)        #将分组结果ResultIterable转换为List
        return "||".join(l)      #列表不能直接存入Mysql

    def get_lawlsit(court_idea):

        l = ""
        return l


    def get_date(j, a):
        d = re.split(ur"年|月|日", j)
        if len(d) == 4:
            if len(d[0]) == 4:
                year = a.get(d[0][0], "a") + a.get(d[0][1], "a") + a.get(d[0][2], "a") + a.get(d[0][3], "a")
                m = a.get(d[1], "aa")
                if len(m) == 1:
                    m = "0" + m
                day = a.get(d[2], "aa")
                if len(day) == 1:
                    day = "0" + day
                elif day == "aa" and d[2].startswith(u"十"):
                    day = "1" + a.get(d[2][1], "a")
                elif day == "aa" and d[2].startswith(u"二十"):
                    day = "2" + a.get(d[2][2], "a")
                strdate = year + "-" + m + "-" + day
                try:
                    time.strptime(strdate, "%Y-%m-%d")
                    return strdate
                except:
                    return ""
        else:
            return ""


    # 代理 审判员  庞芸 二Ｏ一一年四月 二十一日 书记员  王燕
    #  代理 审判员  庞芸 二Ｏ一一年四月 二十一日
    #   二Ｏ一一年四月 二十一日 书记员  王燕

    def casedate_get(doc_footer):
        # [u'一',u'二',u'三',u'四',u'五',u'六',u'七',u'八',u'九',u'十',u'百',u'千',u'第',u'条']
        # [u'\u4e00', u'\u4e8c', u'\u4e09', u'\u56db', u'\u4e94', u'\u516d', u'\u4e03', u'\u516b', u'\u4e5d', u'\u5341', u'\u767e', u'\u5343', u'\u7b2c', u'\u6761']
        # 搜索以 ‘第’开头，以‘条’结束，中间包含：1-10个[u'一',u'二',u'三',u'四',u'五',u'六',u'七',u'八',u'九',u'十',u'百',u'千']中的汉字

        a = {u"О": "0", u"O": "0", u"o": "0", u"Ο": "0", u"Ｏ": "0", u"0": "0", u"○": "0", u"〇": "0", u"０": "0",
             u"元": "1", u"一": "1", u"二": "2", u"三": "3", u"四": "4", u"五": "5", u"六": "6", u"七": "7", u"八": "8",
             u"九": "9", u"十": "10", u"十一": "11", u"十二": "12", u"二十": "20", u"三十": "30", u"三十一": "31"}

        p1 = ur'[一二][ ]{0,8}[ОOoΟＯ0○〇０九][ ]{0,8}[ОOoΟＯ0○〇０一二九][ ]{0,8}[ОOoΟＯ0○〇０一二三四五六七八九][ ]{0,8}年[ ]{0,8}年{0,1}[ ]{0,8}[元一二三四五六七八九十][ ]{0,8}[一二]{0,1}[ ]{0,8}月[ ]{0,8}月{0,1}[ ]{0,8}[一二三四五六七八九十][ ]{0,8}[一二三四五六七八九十]{0,1}[ ]{0,8}[一二三四五六七八九十]{0,1}'
        r2 = re.search(p1, doc_footer)

        if r2:
            j = r2.group(0).replace(" ", "").replace(u"年年", u"年").replace(u"月月", u"月") + u"日"
            return get_date(j, a)
        else:
            return ""


    def flat_uid(uid):
        reason_uid = []
        if len(uid) == 7:
            reason_uid.append(uid[:4])
        elif len(uid) == 10:
            reason_uid.append(uid[:4])
            reason_uid.append(uid[:7])
        elif len(uid) == 13:
            reason_uid.append(uid[:4])
            reason_uid.append(uid[:7])
            reason_uid.append(uid[:10])
        elif len(uid) == 16:
            reason_uid.append(uid[:4])
            reason_uid.append(uid[:7])
            reason_uid.append(uid[:10])
            reason_uid.append(uid[:13])
        else:
            pass
        # reason_uid.append(uid)       #这里的自己uid传过来是唯一的，且要与reason_name保持顺序一致，这里就不添加，后面使用字符串连接上去
        return reason_uid
    def get_reason(x):
        # (x[1], x[3], x[4], x[5], x[6])
        # id, uuid, court, title, trial_request, trial_process, court_find, doc_footer
        # id, uuid, court, title, trial_request, trial_reply, trial_process, court_find, doc_footer
        # acc.add(1)
        # uuid,title,trial_process
        title = x[3]
        trial_request = x[4]
        # trial_reply = x[5]
        trial_process = x[5]
        court_find = x[6]
        doc_footer = x[7]
        court_idea = x[8]
        # casedate = casedate_get(doc_footer)
        casedate = ""

        plt_claim, dft_rep, crs_exm = get_plt_text((casedate,trial_request,""))

        lawlist = ""


        if court_idea and court_idea != "":
            # 依照《中华人民共和国刑法》第七十八条、第五十七条第二款、《最高人民法院关于办理减刑、假释案件具体应用法律的规定》第二条、
            # 第八条第一款、第十七条第二款、《中华人民共和国刑事诉讼法》第二百六十二条第二款、
            # 《最高人民法院关于减刑、假释案件审理程序的规定》第十六条第一款（一）项的规定，裁定如下：

            # 依照《中华人民共和国刑法》第七十八条、第五十七条第二款、《最高人民法院关于办理减刑、假释案件具体应用法律的规定》第二条、
            # 第八条第一款、第十七条第二款、《中华人民共和国刑事诉讼法》第二百六十二条第二款、
            # 《最高人民法院关于减刑、假释案件审理程序的规定》第十六条第一款（一）项的规定，裁定如下：

            # [u'一',u'二',u'三',u'四',u'五',u'六',u'七',u'八',u'九',u'十',u'百',u'千',u'第',u'条']
            # [u'\u4e00', u'\u4e8c', u'\u4e09', u'\u56db', u'\u4e94', u'\u516d', u'\u4e03', u'\u516b', u'\u4e5d', u'\u5341', u'\u767e', u'\u5343', u'\u7b2c', u'\u6761']
            # 搜索以 ‘第’开头，以‘条’结束，中间包含：1-10个[u'一',u'二',u'三',u'四',u'五',u'六',u'七',u'八',u'九',u'十',u'百',u'千']中的汉字
            p1 = ur'\u7b2c[\u4e00\u4e8c\u4e09\u56db\u4e94\u516d\u4e03\u516b\u4e5d\u5341\u767e\u5343]{1,10}\u6761'
            # 按《》切分
            p2 = ur'[\u300a\u300b]'


            lawlist_re = re.findall(ur'''《[\u4e00-\u9fa5、，；： ]{5,100}》\u7b2c[\u4e00\u4e8c\u4e09\u56db\u4e94\u516d\u4e03\u516b\u4e5d\u5341\u767e\u5343]{1,10}\u6761[\u4e00-\u9fa5]{0,50}、{0,1}\u7b2c{0,1}[\u4e00\u4e8c\u4e09\u56db\u4e94\u516d\u4e03\u516b\u4e5d\u5341\u767e\u5343]{0,10}\u6761{0,1}[\u4e00-\u9fa5]{0,50}、{0,1}\u7b2c{0,1}[\u4e00\u4e8c\u4e09\u56db\u4e94\u516d\u4e03\u516b\u4e5d\u5341\u767e\u5343]{0,10}\u6761{0,1}[\u4e00-\u9fa5]{0,50}\u7b2c{0,1}[\u4e00\u4e8c\u4e09\u56db\u4e94\u516d\u4e03\u516b\u4e5d\u5341\u767e\u5343]{0,10}\u6761{0,1}[\u4e00-\u9fa5]{0,50}\u7b2c{0,1}[\u4e00\u4e8c\u4e09\u56db\u4e94\u516d\u4e03\u516b\u4e5d\u5341\u767e\u5343]{0,10}\u6761{0,1}[\u4e00-\u9fa5]{0,50}\u7b2c{0,1}[\u4e00\u4e8c\u4e09\u56db\u4e94\u516d\u4e03\u516b\u4e5d\u5341\u767e\u5343]{0,10}\u6761{0,1}[\u4e00-\u9fa5]{0,50}\u7b2c{0,1}[\u4e00\u4e8c\u4e09\u56db\u4e94\u516d\u4e03\u516b\u4e5d\u5341\u767e\u5343]{0,10}\u6761{0,1}[\u4e00-\u9fa5]{0,50}\u7b2c{0,1}[\u4e00\u4e8c\u4e09\u56db\u4e94\u516d\u4e03\u516b\u4e5d\u5341\u767e\u5343]{0,10}\u6761{0,1}[\u4e00-\u9fa5]{0,50}\u7b2c{0,1}[\u4e00\u4e8c\u4e09\u56db\u4e94\u516d\u4e03\u516b\u4e5d\u5341\u767e\u5343]{0,10}\u6761{0,1}[\u4e00-\u9fa5]{0,50}''',court_idea)

            # In[51]: for i in d:
            #     ...:     print i
            #     ...:
            #     ...:
            #     《中华人民共和国刑法》第七十八条、第五十七条第二款、
            #     《最高人民法院关于办理减刑、假释案件具体应用法律的规定》第二条、第八条第一款、第十七条第二款
            #     《中华人民共和国刑事诉讼法》第二百六十二条第二款、
            #     《最高人民法院关于减刑、假释案件审理程序的规定》第十六条第一款
            l = []

            for i in lawlist_re:
                fa = re.search(ur'''《[\u4e00-\u9fa5、，；： ]{5,100}》''',i).group(0)
                tiao = re.findall(ur'''第[一二三四五六七八九十百千]{1,10}条''',i)
                for j in tiao:
                    # ["《中华人民共和国刑法》第七十八条", "《中华人民共和国刑事诉讼法》第二百六十二条第二款", "《中华人民共和国刑法》第七十九条"]
                    l.append('''"''' + fa + j + '''"''')

            lawlist = "[" + ",".join(l) + "]"     # 存到mysql时，结果结构为（带[]的）：  ["《中华人民共和国刑法》第二百八十条","《中华人民共和国刑法》第六十七条","《中华人民共和国刑法》第五十二条"]

        name = []
        uid = []
        for i in reason_broadcast.value:  #
            if i[0] in title or i[0] in trial_process or i[0] in trial_request or i[0] in court_find:
                name.append(i[0])
                uid.append(i[1])
        uid_l = list(set(uid))
        t3 = []
        for uid in uid_l:       #这里的uid_l已经是唯一的，经前面的get_unique_uids函数处理过
            t3.extend(flat_uid(uid))
        t3.extend(uid_l)
        reason_uids = "||".join(list(set(t3)))

        return (x[1],("||".join(list(set(name))),reason_uids,casedate,plt_claim, dft_rep, crs_exm,lawlist))

    def get_plt_text(row):

        casedate = row[0]
        trial_request = row[1]
        trial_reply = row[2]

        if  trial_request:
            trial_request_lst =trial_request.split('\n')
            trial_request = trial_request_lst[0]
            if len(trial_request_lst)>1:
                trial_reply = trial_request_lst[1]

                trial_together = trial_request + trial_reply
            else:
                trial_together = trial_request

            dft_idx = [] # defendent
            dft_no_idx = []
            qst_idx = [] # question

            plt =[]
            dft =[]
            qst =[]

            trial_lst = trial_together.split(u'。')#split by '\n' or '。'
            for idx,cnt in enumerate(trial_lst):
                if (u'被告' in cnt and u'辩' in cnt) or (u'被告' in cnt and u'异议' in cnt) :
                    dft_idx.append(idx)
                if (u'未' in cnt or u'没' in cnt) :
                    dft_no_idx.append(idx)
                if (u'审理查明' in cnt )  or (u'被告' in cnt and u'反驳' in cnt):
                    qst_idx.append(idx)
            if len(dft_idx) >0 :
                if len(qst_idx)>0:
                    plt = trial_lst[:dft_idx[0]]
                    dft = trial_lst[dft_idx[0]:qst_idx[0]]
                    qst = trial_lst[qst_idx[0]:]
                else:
                    plt = trial_lst[:dft_idx[-1]]
                    dft = trial_lst[dft_idx[-1]:]
            else:
                plt = trial_lst[:]
            plt_text = ''.join(plt)
            dft_text = ''.join(dft)
            qst_text = ''.join(qst)
            dft_text = dft_text.replace("\n","")
            # trial_request = str(trial_request
            # trial_reply = str(trial_reply)
            # ` (`uuid`, `id`, `trial_request`, `trial_reply`, `plt_claim`, `dft_rep`, `crs_exm`)
            # VALUES( % s, % s, % s, % s, % s, % s, % s)"
            # cur.execute(sql, (uuid, dbid, trial_request, trial_reply, plt_text, dft_text, qst_text))
            return plt_text, dft_text, qst_text
        return "","",""

    # judgment_new：556万,3030306	3392975
    df = sqlContext.read.jdbc(url='jdbc:mysql://cdh-slave1:3306/laws_doc_zhangye_etl2',
                               table='(select id,uuid,court,title,trial_request,trial_process,court_find,doc_footer,court_idea from judgment_zhangye_180wan_join_all  ) tmp',
                               column='id', lowerBound=4816522, upperBound=6290661, numPartitions=100,
                               properties={"user": "weiwc", "password": "HHly2017."})
    # court:4778条
    df1 = sqlContext.read.jdbc(url='jdbc:mysql://cdh-slave1:3306/civil',
                               table='(select id,name,province,full_uid from court ) tmp1',
                               column='id', lowerBound=1, upperBound=5000, numPartitions=1,
                               properties={"user": "weiwc", "password": "HHly2017."})
    # reason：1497条
    df2 = sqlContext.read.jdbc(url='jdbc:mysql://cdh-slave1:3306/civil',
                               table='(select id,name,uid from reason ) tmp2',
                               column='id', lowerBound=1, upperBound=1500, numPartitions=1,
                               properties={"user": "weiwc", "password": "HHly2017."})


    # acc = sc.accumulator(0)
    # print "df.count()======================" + str(df.count())
    reason_broadcast = sc.broadcast(df2.map(lambda x:(x[1],x[2])).collect())
    uuid_reason = df.map(lambda x:x).map(lambda x:get_reason(x))    #title_trial_process
    # (x[1], ("||".join(list(set(name))), reason_uids, casedate, plt_claim, dft_rep, crs_exm))
    # print "uuid_reason.count()======================" + str(uuid_reason.count())
    # uuid_reason.foreach(p)
    # print "uuid_reason=============="+str(uuid_reason.count())
    uuid_court = df.map(lambda x:(x[2],x[1]))  #court,uuid
    # print "uuid_court==============" + str(uuid_court.count())
    court_province_full_uid = df1.map(lambda x:(x[1],(x[2],x[3])))   #court,province,full_uid
    uuid_province_full_uid = uuid_court.join(court_province_full_uid).map(lambda x:x[1])  #uuid_court中的法院，court表里面可能没有，court表不全，因此uuid记录数会少。
    # .map(lambda x: (x[0], x[1][0], x[1][1]))  # uuid,province,full_uid
    # print "uuid_province_full_uid.count()======================" + str(uuid_province_full_uid.count())

    def get_result(x):
        if x[1][1] is None:
            return (x[0], x[1][0][0], x[1][0][1], x[1][0][3], x[1][0][4], x[1][0][5],x[1][0][6], "", "")
        else:
            return (x[0], x[1][0][0], x[1][0][1], x[1][0][3], x[1][0][4], x[1][0][5],x[1][0][6], x[1][1][0], x[1][1][1])

    # print "uuid_province_full_uid==============" + str(uuid_province_full_uid.count())
    result = uuid_reason.leftOuterJoin(uuid_province_full_uid).map(lambda x:get_result(x))  #避免由于court未匹配，导致的其他字段丢失。
    # print "acc======================" + str(acc.value)

    # print "result==============" + str(result.count())
    # reason_uids2 = reason_uid.map(lambda x:(x[6],x[6].encode("utf-8")+"_"+x[5].encode("utf-8")))
    # reason_uids2.foreach(p)
    # print str(reason_uids2.count()) + "=================="
    # c1 = reason_null.select('uuid','doc_reason').map(lambda x:(x[0],x[1])).filter(lambda x:filter_(x)).flatMapValues(lambda x:extact_reason(x)).map(lambda x:(x[1],x[0])).cache()

    # c2 = c1.groupByKey().mapValues(lambda v:get_uuids(v)).cache()

    # c3 = reason_uids.join(c2).map(lambda x:x[1]).flatMapValues(lambda x:(x.split("||"))).map(lambda x:(x[1],x[0])).cache()

    # c4 = c3.groupByKey().mapValues(lambda x:(get_unique_uids(x))).cache()

    # d = c4.flatMapValues(lambda x:(extact_reason(x))).map(lambda x:(x[1],x[0])).groupByKey().mapValues(lambda v:get_uuids(v))
    # reason_uids_result = reason_uids2.join(d).map(lambda x:x[1]).flatMapValues(lambda x:(x.split("||"))).map(lambda x:(x[1],x[0])).groupByKey().map(lambda x:(get_reason_name_and_uids(x)))

    # plt_claim, dft_rep, crs_exm
    schema = StructType([StructField("uuid", StringType(), False),
                         StructField("reason", StringType(), True),
                         StructField("reason_uid", StringType(), True),
                         # StructField("casedate", StringType(), True),
                         StructField("plt_claim", StringType(), True),
                         StructField("dft_rep", StringType(), True),
                         StructField("crs_exm", StringType(), True),
                         StructField("lawlist", StringType(), True),
                         StructField("province", StringType(), True),
                         StructField("court_uid", StringType(), True)])

    f = sqlContext.createDataFrame(result, schema=schema)
    # , mode = "overwrite"
    # useUnicode = true & characterEncoding = utf8，指定写入mysql时的数据编码，否则会乱码。
    # print str(f.count()) + "======================"
    f.write.jdbc(url='jdbc:mysql://cdh-slave1:3306/laws_doc_zhangye_etl2?useUnicode=true&characterEncoding=utf8', table='judgment_zhangye_180wan_other_fields',properties={"user": "weiwc", "password": "HHly2017."})

    sc.stop()