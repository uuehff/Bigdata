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

    def valid_casedate(strdate):
        '''''判断是否是一个有效的日期字符串'''
        try:
            time.strptime(strdate, "%Y-%m-%d")
            return True
        except:
            return False


    def get_date(j, a):
        d = re.split(ur"年|月|日", j)
        if len(d) == 4:
            if len(d[0]) == 4:
                year = a.get(d[0][0], "0") + a.get(d[0][1], "0") + a.get(d[0][2], "0") + a.get(d[0][3], "0")
                m = a.get(d[1], "00")
                if len(m) == 1:
                    m = "0" + m
                day = a.get(d[2], "00")
                if len(day) == 1:
                    day = "0" + day
                elif day == "00" and d[2].startswith(u"十"):
                    day = "1" + a.get(d[2][1], "0")
                elif day == "00" and d[2].startswith(u"二十"):
                    day = "2" + a.get(d[2][2], "0")
                strdate = year + "-" + m + "-" + day
                try:
                    time.strptime(strdate, "%Y-%m-%d")
                    return strdate
                except:
                    return ""
        else:
            return ""


    def get_casedate(doc_footer):
        a = {u"Ｏ": "0", u"0": "0", u"○": "0", u"〇": "0", u"０": "0", u"元": "1", u"一": "1", u"二": "2", u"三": "3",
             u"四": "4", u"五": "5",
             u"六": "6", u"七": "7", u"八": "8", u"九": "9", u"十": "10", u"十一": "11", u"十二": "12", u"二十": "20", u"三十": "30",
             u"三十一": "31"}
        s = re.split('[\n]', doc_footer)
        if len(s) < 2:
            d = re.split(ur"〇|0|○|Ｏ|０|日", doc_footer)
            if len(d) > 2:
                return get_date(u"二〇" + d[1] + u"日", a)
            else:
                return ""
        else:
            for i in s:
                j = i.replace(" ", "")
                if (j.startswith(u"一") or j.startswith(u"二")) and u"日" in j:
                    return get_date(j, a)
                else:
                    continue
            return ""

    def filter_(x):
        if x :
            if len(x) == 17:
                return True
        return False

    def p(x):
        print type(x),type(x[0]),type(x[1])
        # print type(x)
        # print type(x[0]),type(x[1])
        print x[0],x[1][0],x[1][1]


    df = sqlContext.read.jdbc(url='jdbc:mysql://cdh5-slave2:3306/laws_doc_zhangye_v2',
                               table='(select * from judgment_zhangye_400w_v2_01 ) tmp',
                               column='id', lowerBound=1, upperBound=8450136, numPartitions=79,
                               properties={"user": "weiwc", "password": "HHly2017."})

    df1 = sqlContext.read.jdbc(url='jdbc:mysql://cdh5-slave2:3306/laws_doc_zhangye_v2',
                               table='(select id,uuid,title,reason_type,caseid,type,casedate from judgment_zhangye_zhixing_v2  ) tmp',
                               column='id', lowerBound=1, upperBound=2404927, numPartitions=20,
                               properties={"user": "weiwc", "password": "HHly2017."})

    # id,uuid,party_info,trial_process,trial_request,court_find,court_idea,judge_result,doc_footer,court,uuid_,judge_type
    uuid_x = df.map(lambda x:(x[1],x))

    # id,doc_id,case_name,case_type,case_number,jud_pro,jud_date
    uuid_x2 = df1.map(lambda x:(x[1],(x[2],x[3],x[4],x[5],x[6])))


    def get_result(x):

        return (x[0][0],x[0][1],x[0][2],x[0][3],x[0][4],x[0][5],x[0][6],x[0][7],x[0][8],x[0][9],x[0][10],x[0][11],x[1][0],x[1][1],x[1][2],x[1][3],x[1][4])

    result = uuid_x.join(uuid_x2).map(lambda x:x[1]).map(lambda x:get_result(x))   #id,doc_id,case_name,case_type,case_number,jud_pro,jud_date

    # lawyer_k_v.foreach(p)
    # print "len===========" + str(lawyer_k_v.count())

    # lawyer_k_v_civil = result.filter(lambda x:filter_civil(x[13]))
    # lawyer_k_v_xingshi = result.filter(lambda x:filter_xingshi(x[13]))
    # lawyer_k_v_xingzheng = result.filter(lambda x:filter_xingzheng(x[13]))
    # lawyer_k_v_zhixing = result.filter(lambda x:filter_zhixing(x[13]))



    # id,uuid,party_info,trial_process,trial_request,court_find,court_idea,judge_result,doc_footer,court,uuid_,judge_type
    schema = StructType([StructField("id", StringType(), False),
                         StructField("uuid", StringType(), False),
                         StructField("party_info", StringType(), True),
                         StructField("trial_process", StringType(), True),
                         StructField("trial_request", StringType(), True),
                         StructField("court_find", StringType(), True),
                         StructField("court_idea", StringType(), True),
                         StructField("judge_result", StringType(), True),
                         StructField("doc_footer", StringType(), True),
                         StructField("court", StringType(), True),
                         StructField("uuid_", StringType(), True),
                         StructField("judge_type", StringType(), True),
                         StructField("title", StringType(), True),
                         StructField("reason_type", StringType(), True),
                         StructField("caseid", StringType(), True),
                         StructField("type", StringType(), True),
                         StructField("casedate", StringType(), True)
                         ])

    # f = sqlContext.createDataFrame(lawyer_k_v_civil, schema=schema)
    # f.write.jdbc(url='jdbc:mysql://cdh5-slave2:3306/laws_doc_zhangye_v2?useUnicode=true&characterEncoding=utf8', table='judgment_zhangye_civil_v2',properties={"user": "weiwc", "password": "HHly2017."})

    f = sqlContext.createDataFrame(result, schema=schema)
    f.write.jdbc(url='jdbc:mysql://cdh5-slave2:3306/laws_doc_zhangye_v2?useUnicode=true&characterEncoding=utf8', table='judgment_zhangye_zhixing_v2_result',properties={"user": "weiwc", "password": "HHly2017."})

    # f = sqlContext.createDataFrame(lawyer_k_v_xingzheng, schema=schema)
    # f.write.jdbc(url='jdbc:mysql://cdh5-slave2:3306/laws_doc_zhangye_v2?useUnicode=true&characterEncoding=utf8', table='judgment_zhangye_xingzheng_v2',properties={"user": "weiwc", "password": "HHly2017."})
    #
    # f = sqlContext.createDataFrame(lawyer_k_v_zhixing, schema=schema)
    # f.write.jdbc(url='jdbc:mysql://cdh5-slave2:3306/laws_doc_zhangye_v2?useUnicode=true&characterEncoding=utf8', table='judgment_zhangye_zhixing_v2',properties={"user": "weiwc", "password": "HHly2017."})

    sc.stop()