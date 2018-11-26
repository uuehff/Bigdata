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


    def foot_get(items):
        # judge_result:
        # 准许原告暨诉讼代表人撤回起诉。
        # 案件受理费50元，减半收取25元，由原告暨诉讼代表人负担。
        # 审判长吴铁梅
        # 审判员殷载媛
        # 人民陪审员肖正江
        # 二〇一七年一月十日
        # 书记员欧阳小玲

        # ?  0或1次，+ 1或多， * 0或多
        # reg_footer = re.compile(ur'\n(?:\S{0,2}审判).*(?:书记员|\S+年\S+月)\S+', re.S)
        # 附里面的当事人信息里面也有年月的匹配。
        # re.S开启了.匹配任意字符串，用(?:和)将其之间的内容作为一个整体，而不是用（），\n(?:\S{0,2}审判)，其中judge_result中的空格都已去掉，有的只是
        # 换行回车等：\f\n\r\t\v，审判前面匹配0-2个非空字符，可能匹配到代理等词，再前面是\n，是判决结果那句话与下面的换行符。
        # .*匹配任意字符，(?:书记员|\S+年\S+月)\S+，这里能匹配到“书记员，代书记员，或者多个书记员等等”，匹配到最后一个符合条件的值，
        # 拆开为：匹配到最后一个.*书记员\S+ 或 匹配到最后一个.*\S+年\S+月\S+，哪个的值在最最后，就以哪个的匹配值结尾。\S+匹配任意非空，遇空（\f\n\r\t\v）就停止。
        # reg_footer = re.compile(ur'\n(?:\S{0,2}审判|\S{0,2}执行员|\S{0,2}院长).*(?:\S{0,2}书记员|\S+年\S+月)\S+', re.S)
        reg_footer = re.compile(
            ur'\n(?:\S{0,2}审[　  ]{0,2}判|\S{0,2}执[　  ]{0,2}行员|\S{0,2}院[　  ]{0,2}长).*(?:书[　  ]{0,2}记员|\S+年\S+月)\S+', re.S)
        items = items.replace("\\n", '\n')
        footer_result = re.findall(reg_footer, items)

        if footer_result:
            # footer_result[0]中可能有特殊符号：类似？号等等，？在split的pattern中属于特殊字符，因此要替换掉再分割.
            items_tmp = items.replace(footer_result[0], "!1qw23er4!")

            lp = re.split("!1qw23er4!", items_tmp)
            doc_footer = footer_result[0].strip() + lp[1]

            doc_footer = doc_footer.replace(u"审判长", u" 审判长  ").replace(u"代理审判员", u" 代理审判员") \
                .replace(u"审判员", u" 审判员  ").replace(u"书记员", u" 书记员  ").replace(u"陪审员", u" 陪审员  ") \
                .replace(u"二", u" 二").replace(u"院长", u" 院长  ").replace(u"执行员", u" 执行员  ")
            return lp[0], doc_footer  # result,doc_footer
        else:
            return items, ""

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


    def get_judge(doc_footer):
        doc_footer = doc_footer.replace(u"　", "").replace(" ", "")
        split_result = doc_footer.split("\n")
        reg_footer = re.compile(ur'(?:\S{0,2}审判|\S{0,2}院长|\S{0,2}陪审)\S{2,}')
        judge_result = ""
        l = []
        for i in split_result:
            if re.search(reg_footer, i):
                l.append(i)
        # 审判长|院长|审判员|代理审判员|人民审判员|助理审判员|陪审员|人民陪审员
        judge_result = "||".join(l).replace(u"代理审判长", "||").replace(u"审判长", "||").replace(u"代理院长", "||").replace(u"院长",
                                                                                                                 "||") \
            .replace(u"代理审判员", "||").replace(u"人民审判员", "||") \
            .replace(u"助理审判员", "||").replace(u"审判员", "||").replace(u"人民陪审员", "||").replace(u"代理陪审员", "||").replace(
            u"陪审员", "||") \
            .replace("||||", "||").lstrip("||")
        s = []
        for j in judge_result.split("||"):  # 由于reg_footer
            if len(j) < 5:
                s.append(j)
        judge_result = "||".join(s)

        # reg_footer2 = re.compile(ur'(?:\S{0,2}审判|\S{0,2}院长)\S?', re.S)
        # 如果为空，说明全部有换行，例如：
        # 审判员
        # 某某某
        # if doc_footer_result == "":
        #     for i in range(len(split_result)):
        #         if re.search(reg_footer2, split_result[i]) and len(split_result[i + 1]) < 4:
        #             l.append(split_result[i + 1])
        #
        #     doc_footer_result = "||".join(l)

        return judge_result


    def get_doc_footer_one_line(doc_footer):
        doc_footer = doc_footer.replace(u"　", "").replace(" ", "")
        split_result = doc_footer.split("\n")
        reg_footer = re.compile(ur'(?:\S{0,2}审判|\S{0,2}院长|\S{0,2}陪审|执行员|书记员|\S+年\S+月)\S{2,}')
        reg_footer1 = re.compile(ur'(?:\S{0,2}审判|\S{0,2}院长|\S{0,2}陪审|执行员|书记员)\S{0,1}')
        # reg_footer2 = re.compile(ur'^(?:\S{0,2}审判|\S{0,2}院长|\S{0,2}陪审)\S{2,3}', re.S)
        doc_footer_result = ""
        l = []
        for i in range(len(split_result)):
            if re.search(reg_footer, split_result[i]):
                l.append(split_result[i])
            elif re.search(reg_footer1, split_result[i]):
                if i + 1 < len(split_result):
                    if len(split_result[i + 1]) < 4:
                        l.append(split_result[i] + split_result[i + 1].replace("\n", ""))

        doc_footer_result = "\n".join(l).replace(u"代理审判长", u" 代理审判长 ").replace(u"审判长", u" 审判长  ").replace(u"代理审判员",u" 代理审判员") \
            .replace(u"人民审判员", u" 人民审判员").replace(u"助理审判员", u" 助理审判员").replace(u"审判员", u" 审判员  ").replace(u"书记员",u" 书记员  ") \
            .replace(u"人民陪审员", u" 人民陪审员  ").replace(u"代理陪审员", u" 代理陪审员  ").replace(u"陪审员", u" 陪审员  ") \
            .replace(u"二", u" 二").replace(u"代理院长", u" 代理院长  ").replace(u"院长", u" 院长  ").replace(u"执行员", u" 执行员  ")

        return doc_footer_result


    def get_result(x):
        # id,uuid,court,court_idea,judge_result,doc_footer,judge_type
        court_idea = x[3]
        judge_result = x[4].replace("?", "  ")
        doc_footer = x[5].replace("?", "  ")
        judge_type = x[6]
        doc_footer_tmp = ""

        # 针对有分段的文书进行法官提取。
        if judge_type == u"判决" or judge_type == u"裁定":

            # reg_footer_tmp = re.compile(ur'\n(?:\S{0,2}审[　  ]{0,2}判|\S{0,2}执[　  ]{0,2}行员|\S{0,2}院[　  ]{0,2}长)[ ]{0,6}\S{2,}')
            reg_footer_tmp = re.compile(ur'\n(?:\S{0,2}审[　 ]{0,2}判|\S{0,2}执[　 ]{0,2}行员|\S{0,2}院[　 ]{0,2}长).*', re.S)
            ss = re.search(reg_footer_tmp, judge_result)
            if ss:
                judge_result = judge_result.replace(ss.group(0), "")
                doc_footer_tmp = ss.group(0) + "\n"

                doc_footer_tmp = doc_footer_tmp.replace(" ", "").replace(u"审判长", u" 审判长  ").replace(u"代理审判员", u" 代理审判员") \
                    .replace(u"审判员", u" 审判员  ").replace(u"书记员", u" 书记员  ").replace(u"陪审员", u" 陪审员  ") \
                    .replace(u"二", u" 二").replace(u"院长", u" 院长  ").replace(u"执行员", u" 执行员  ")

            doc_footer = doc_footer_tmp + doc_footer
            doc_footer = get_doc_footer_one_line(doc_footer)

            judge = get_judge(doc_footer)

            court_idea.replace("?", "  ")
            if judge == "":  # doc_footer和judge_result都没有提取出法官，说明可能是无法分段，整篇放到court_idea字段里。
                judge_result, doc_footer = foot_get(court_idea)
                doc_footer = get_doc_footer_one_line(doc_footer)
                judge = get_judge(doc_footer)
                return (x[0],x[1],x[2],judge, None, None, court_idea)

            return (x[0],x[1],x[2],judge, judge_result, doc_footer, court_idea)

        else:  # 针对没有分段的数据提取法官。

            court_idea = court_idea.replace("?", "  ")
            # print court_idea

            judge_result, doc_footer = foot_get(court_idea)
            doc_footer = get_doc_footer_one_line(doc_footer)
            judge = get_judge(doc_footer)

            return (x[0],x[1],x[2],judge, None, None, court_idea)


    df = sqlContext.read.jdbc(url='jdbc:mysql://cdh5-slave2:3306/laws_doc_zhangye_v2',
                               table='(select id,uuid,court,court_idea,judge_result,doc_footer,judge_type from judgment_zhangye_xingshi_v2_result  ) tmp',
                               column='id', lowerBound=1, upperBound=7644815, numPartitions=98,
                               properties={"user": "weiwc", "password": "HHly2017."})
    # court:4778条
    df1 = sqlContext.read.jdbc(url='jdbc:mysql://cdh5-slave2:3306/laws_doc',
                               table='(select id,name,court_cate from court ) tmp1',
                               column='id', lowerBound=1, upperBound=5000, numPartitions=1,
                               properties={"user": "weiwc", "password": "HHly2017."})

    # acc = sc.accumulator(0)
    # print "df.count()======================" + str(df.count())
    # reason_broadcast = sc.broadcast(df2.map(lambda x:(x[1],x[2])).collect())
    court_kv = df.map(lambda x:x).map(lambda x:get_result(x)).map(lambda x:(x[2],x))    #title_trial_process
    court_court_cate_kv = df1.map(lambda x:(x[1],x[2]))   #court,province,full_uid
    result = court_kv.leftOuterJoin(court_court_cate_kv).map(lambda x:x[1]).\
        map(lambda x:(x[0][0],x[0][1],x[0][2],x[0][3],x[0][4],x[0][5],x[0][6],x[1]))

    # id,uuid,court,judge, judge_result, doc_footer, court_idea
    schema = StructType([StructField("id", StringType(), False),
                         StructField("uuid", StringType(), False),
                         StructField("court", StringType(), True),
                         StructField("judge", StringType(), True),
                         StructField("judge_result", StringType(), True),
                         StructField("doc_footer", StringType(), True),
                         StructField("court_idea", StringType(), True),
                         StructField("court_cate", StringType(), True)])

    f = sqlContext.createDataFrame(result, schema=schema)
    # , mode = "overwrite"
    # useUnicode = true & characterEncoding = utf8，指定写入mysql时的数据编码，否则会乱码。
    # print str(f.count()) + "======================"
    f.write.jdbc(url='jdbc:mysql://cdh5-slave2:3306/laws_doc_zhangye_v2?useUnicode=true&characterEncoding=utf8', table='judgment_zhangye_xingshi_v2_result_court_cate_judge_footer',properties={"user": "weiwc", "password": "HHly2017."})

    sc.stop()