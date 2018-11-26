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

    def get_uuids(uuids):
        l = []
        for x in uuids:
            l.append(x)  # 将分组结果ResultIterable转换为List
        return "||".join(l)  # 列表不能直接存入Mysql


    def filter_(x):
        if x[1] and x[1] != '':  # 过滤掉数据库中，lawlist为Null或''的行。
            return True
        return False


    def get_lawlist_ids(uuid_ids):
        uuid, ids = uuid_ids[0], uuid_ids[1]
        lawlist_id = []
        for x in ids:
            lawlist_id.append(x)
        return (uuid, "||".join(lawlist_id))


    def get_title_short_id(x):  # 保证lawlist和law_id的有序！
        k = x[0] + "|" + x[1]
        v = str(x[2])
        return (k, v)

    # lawlist = sqlContext.read.jdbc(url='jdbc:mysql://cdh-slave1:3306/civil', table='uuid_reason_lawlist',column='id',lowerBound=0,upperBound=100000,numPartitions=70,properties={"user": "root", "password": "HHly2017."})
    lawlist_id = sqlContext.read.jdbc(url='jdbc:mysql://cdh5-slave3:3306/law',
                                      table='(select id,title_short,art_num,lawlist_id from law_rule_result2) tmp',
                                      column='id', lowerBound=1, upperBound=2881160, numPartitions=69,
                                      properties={"user": "weiwc", "password": "HHly2017."})


    # judgment_new：556万,3030306	3392975
    lawlist = sqlContext.read.jdbc(url='jdbc:mysql://cdh5-slave2:3306/laws_doc_zhangye_v2',
                               table='(select id,uuid,court_idea from judgment_zhangye_xingshi_v4_result ) tmp',
                               column='id', lowerBound=846537, upperBound=3777923, numPartitions=30,properties={"user": "weiwc", "password": "HHly2017."})

    def get_lawlist(x):
        lawlist = ""
        court_idea = x[2]

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
                fa = re.search(ur'''《[\u4e00-\u9fa5、，；： ]{5,100}》''', i).group(0)
                tiao = re.findall(ur'''第[一二三四五六七八九十百千]{1,10}条''', i)
                for j in tiao:
                    # ["《中华人民共和国刑法》第七十八条", "《中华人民共和国刑事诉讼法》第二百六十二条第二款", "《中华人民共和国刑法》第七十九条"]
                    l.append('''"''' + fa + j + '''"''')

            lawlist = "[" + ",".join(l) + "]"  # 存到mysql时，结果结构为（带[]的）：  ["《中华人民共和国刑法》第二百八十条","《中华人民共和国刑法》第六十七条","《中华人民共和国刑法》第五十二条"]

        return (x[1],lawlist)

    def etl_lawlist(p1, p2, lawlist):
        if lawlist and lawlist.strip() != '':
            # if not (lawlist.strip().startswith("[") and lawlist.strip().endswith("]")):  # 去掉前后的所有"
            r1 = re.findall(ur'"{0,5}\["{0,5}', lawlist.strip())
            r2 = re.findall(ur'"{0,5}\]"{0,5}', lawlist.strip())
            if r1 and r2:
                start = r1.pop(0)
                end = r2.pop()
                lawlist = lawlist.strip().replace(start, "").replace(end, "")
                # l = list(eval(lawlist.strip()))                 #有脏数据不能直接使用eval()

                l = lawlist.split('","')      #lawlist类似于：《最高人民法院关于审理建设工程施工合同纠纷案件适用法律问题的解释》第三条", "《中华人民共和国合同法》第九十七条", "最高人民法院关于审理建设工程施工合同纠纷案件适用法律问题的解释》第十条", "《中华人民共和国合同法》第九十八条
                if l:
                    tl = []
                    for i in l:
                        r1 = re.split(p2, i)
                        if len(r1) > 2:            #确保既有《，又有》
                            r2 = re.search(p1, r1[2])
                            if r2:                  #判断是否找到了条
                                tl.append(r1[1] + "|" + r2.group(0))
                    return list(set(tl))  # 去重
                return []
            return []
        return []

    lawlist_id2 = lawlist_id.select('title_short','art_num','lawlist_id').map(lambda x:get_title_short_id(x))
    p1 = ur'\u7b2c[\u4e00\u4e8c\u4e09\u56db\u4e94\u516d\u4e03\u516b\u4e5d\u5341\u767e\u5343]{1,10}\u6761'
    p2 = ur'[\u300a\u300b]'  # 按《》切分

    tmp_data = lawlist.map(lambda x:x).map(lambda x:get_lawlist(x)).cache()
    c = tmp_data.flatMapValues(lambda x: etl_lawlist(p1, p2, x)).filter(filter_).map(lambda x: (x[1], x[0])).groupByKey().mapValues(lambda v: get_uuids(v))

    lawlist_title_id_result = lawlist_id2.join(c).map(lambda x: x[1]).filter(filter_).flatMapValues(lambda x: (x.split("||"))).map(lambda x: (x[1], x[0])).groupByKey().map(lambda x: get_lawlist_ids(x)).cache()

    result = lawlist_title_id_result.join(tmp_data).map(lambda x:(x[0],x[1][0],x[1][1]))

    schema = StructType([StructField("uuid", StringType(), False),
                         StructField("law_id", StringType(), True),
                         StructField("lawlist", StringType(), True)
                         ])

    f = sqlContext.createDataFrame(result, schema=schema)
    # , mode = "overwrite"
    # useUnicode = true & characterEncoding = utf8，指定写入mysql时的数据编码，否则会乱码。
    # print str(f.count()) + "======================"
    f.write.jdbc(url='jdbc:mysql://cdh5-slave2:3306/laws_doc_zhangye_v2?useUnicode=true&characterEncoding=utf8', table='uuid_law_id_zhangye_xingshi_v4',properties={"user": "weiwc", "password": "HHly2017."})

    sc.stop()