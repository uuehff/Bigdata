# -*- coding: utf-8 -*-

from  pyspark import SparkContext,SparkConf
from pyspark.sql import SQLContext
from pyspark.sql.types import *
import re
import json

if __name__ == "__main__":
    # if len(sys.argv) > 2:
    #     host = sys.argv[1]
    #     hbase_table_read = sys.argv[2]
    #     hbase_table_save = sys.argv[3]
    # else:
    # host = '192.168.12.35'
    # hbase_table_read = 'laws_doc:judgment'
    # hbase_table_save = 'laws_doc:label'
    # PYSPARK_PYTHON = "C:\\Python27\\python.exe"    #多版本python情况下，需要配置这个变量指定使用哪个版本
    # os.environ["PYSPARK_PYTHON"] = PYSPARK_PYTHON

    # patt1 = re.compile(ur'(原告)(.*?)(?=被告|原告|$)')
    # patt2 = re.compile(ur'(被告)(.*?)(?=原告|被告|$)')

    patt1 = re.compile(
        ur'(原告|罪犯|申诉人|赔偿请求人|复议人|申请执行|申请人|申请复议|债权人|申请保全|异议人|案外人)(.*?)(?=被告|原告|申请人|执行人|申请复议|债务人|债权人|申请保全|第三人|申请执行|被保全人|$)')
    patt2 = re.compile(
        ur'(被告|被申请人|被执行人|被申请复议|债务人|被保全人|第三人|自诉人|上诉单位|上诉人)(.*?)(?=原告|被告|被申请人|债务人|债权人|被执行人|被申请复议|被申请保全|第三人|自诉人|上诉人|$)')

    conf = SparkConf()
    sc = SparkContext(conf=conf)
    sqlContext = SQLContext(sc)
    # sc.setLogLevel("ERROR")  # ALL, DEBUG, ERROR, FATAL, INFO, OFF, TRACE, WARN '(select id,uuid,plaintiff_info,defendant_info from tmp_lawyers ) tmp'
    df = sqlContext.read.jdbc(url='jdbc:mysql://cdh5-slave2:3306/laws_doc_lawyers', table='(select id,lawyer,law_office from lawyers) tmp',column='id',lowerBound=1,upperBound=715185,numPartitions=20,properties={"user": "weiwc", "password": "HHly2017."})
    df2 = sqlContext.read.jdbc(url='jdbc:mysql://cdh5-slave2:3306/laws_doc_adjudication', table='(select id,uuid,party_info,court_idea,judge_type from adjudication_civil_etl_v2 ) tmp2',column='id',lowerBound=1,upperBound=3600000,numPartitions=79,properties={"user": "weiwc", "password": "HHly2017."})


    # 取出律师、律所
    def get_lawyer(text):
        office = {}
        person = u''
        off = u''
        patt = re.compile(
            ur'(诉讼代理人|辩护人|委托代理人|委托代理|诉讼代理|委托代表人|诉讼代表人|代理人（特别授权）|代理人（特别授权代理）)[：]{0,1}([\u4e00-\u9fa5]{2,10})(，|（|,|、)(.*?)(事务所律师|律师事务所">|事物所律师|中心律师|中心律师（特别授权）|事务部律师|法律援助中心，律师|律师事务所，律师|援助处律师|援助律师|工作站律师|工作总站律师|分所律师|服务所律师|律师事务所主任|事务律师|顾问室律师|顾问处军队律师|办公室律师|局律师|指派律师|律师部律师|律师所律师|公司律师|分行律师|政府律师|队律师|。)')
        for s in text:
            o = re.findall(patt, s[1])  # s[1]
            if o:
                for i in range(len(o)):
                    if u'律师' in o[i][4] and u'该' not in o[i][3] and u'＊' not in o[i][1] and u'X' not in o[i][
                        1] and u'×' not in o[i][1] \
                            and u'Ｘ' not in o[i][1] and u'某' not in o[i][1] and u'x' not in o[i][1] and u'×' not in \
                            o[i][3] and u'Ｘ' not in o[i][3] \
                            and u'X' not in o[i][3] and u'x' not in o[i][3] and u'某' not in o[i][3] and u'＊' not in \
                            o[i][3] \
                            and u'A' not in o[i][3] and u'B' not in o[i][3] and u'C' not in o[i][3]:
                        lawy = o[i][1]
                        lawy = lawy.split(u'代理')[-1]
                        # lawy = lawy.strip(u'均为').lstrip(u'人').rstrip(u'上诉人')
                        lawy = lawy.strip(u'均为').rstrip(u'上诉人').strip(u'律师').strip(u'诉讼').strip(u'姓名')\
                            .lstrip(u'人').strip(u'代人').strip(u'理人')

                        a = o[i][3] + o[i][4]
                        a = a.replace(u'事物', u'事务')
                        a = a.replace(u'事务律师', u'事务所律师')
                        a = a.replace(u'律师事务所，律师', u'律师事务所律师')
                        a = a.replace(u'法律援助中心，律师', u'法律援助中心律师')
                        b = a.split(u'，')[-1]
                        b = b.split(u'、')[-1]
                        b = b.split(u'代理）')[-1]
                        b = b.split(u'授权）')[-1]
                        b = b.split(u',')[-1]
                        b = b.split(u'：')[-1]
                        b = b.split(u'委托）')[-1]
                        c = b.strip(u'律师').strip(u'均系').strip(u'均为').strip(u'分别为').strip(u'系').strip(u'分别').strip(
                            u'是').strip(u'主任').strip(u'军队').strip(u'指派').strip(u'\">')
                        if len(lawy) > 1 and c != u'律师事务所' and c != u'事务所' and c != u'法律援助中心' and len(c) > 3:
                            if c not in off:
                                off += c + u'||'
                            office[lawy] = c
                            if lawy not in person:
                                person += lawy + u'||'
        office_ = json.dumps(office, ensure_ascii=False)
        return office_, person[:-2], off[:-2]

    # 取出原告、被告内容
    def get_text(f):
        f = f.replace(u'\n', u'')
        plain = re.findall(patt1, f)
        defen = re.findall(patt2, f)
        return plain, defen


    def get_result(party_info):
        party = get_text(party_info)
        if party[0]:
            plaintiff = get_lawyer(party[0])[0]
            if plaintiff == u'{}':
                plaintiff = u''
        else:
            plaintiff = u''

        if party[1]:
            defendant = get_lawyer(party[1])[0]
            if defendant == u'{}':
                defendant = u''
        else:
            defendant = u''
        # lawyer_ = get_lawyer(party[0])[1]+u'||'+get_lawyer(party[1])[1]
        # lawyer_ = lawyer_.strip(u'||')
        # office_ = get_lawyer(party[0])[2]+u'||'+get_lawyer(party[1])[2]
        # office_ = office_.strip(u'||')
        return plaintiff, defendant

    def get_plaintiff_defendant(x):
        # id, uuid, party_info, court_idea, judge_type

        if x[4] != u"判决" and x[4] != u"裁定" and x[4] != "":
            if x[3] != "":
                plain, defen = get_result(x[3])
                return (str(x[0]),plain,defen,x[1])
            else:
                return None
        else:
            plain, defen = get_result(x[2])
            if plain == "" and defen == "":
                plain, defen = get_result(x[3])
            if plain == "" and defen == "":
                return None
            return (str(x[0]),plain,defen,x[1])

    def p(x):
        print type(x)
        print type(x[0]),type(x[1]),type(x[2])
        print x[0],x[1],x[2]
    def p_(x):
        # print type(x)
        print type(x)
        print type(x[0]),type(x[1])
        print x[0],x[1]
    def filter_(x):
        if x and  x != '':       #过滤掉数据库中，lawlist为Null或''的行。
            return True
        return False

    def get_ids(ids):
        l = []
        for x in ids:
            l.append(x)        #将分组结果ResultIterable转换为List
        return "||".join(l)
    def get_lawyer_ids(new_names):
        l = []
        for x in new_names:
            l.append(x)        #将分组结果ResultIterable转换为List
        return "||".join(l)
    def get_lawyer_id(x):
        lawyer_id = []
        if x[1][0] and x[1][0] != "":
            lawyer_id.append(x[1][0])
        if x[1][1] and x[1][1] != "":
            lawyer_id.append(x[1][1])
        return (x[0],(x[1][0],x[1][1],"||".join(lawyer_id)))
    def get_all_result(x):
        if x[1][1]:
            return (int(x[0]), x[1][0][0], x[1][0][1], x[1][0][2], x[1][1][0], x[1][1][1], x[1][1][2])
        else:
            return (int(x[0]),x[1][0][0],x[1][0][1],x[1][0][2],None,None,None)

    def deal_lawyer(lawyer,law_office):
        if lawyer:
            if lawyer == "":
                return None,None,None
            elif lawyer.startswith(u"一"):  #统计发现类似第一个为“一”的脏数据。
                lawyer = lawyer[1:]   #去掉第一个汉字
        else:
            return None,None,None

        s = ""
        if law_office and len(law_office) >= 6:  #律所的名字

            if law_office[2] == u'省' or law_office[2] == u'市' or law_office[2] == u'县':  # 同一律师名字下，将第三个字为省、市、县去掉。
                t = []
                for i in range(0, len(law_office)):
                    if i == 2:
                        continue
                    t.append(law_office[i])
                s = "".join(t)
            else:
                s = law_office
            s = s.replace(u"律师事务所", "")  # 统一将结尾处理为律师事务所,去重
            s = s.replace(u"事务所", "")
            s = s + u"律师事务所"
            # 内蒙古自治区
            # 宁夏回族自治区
            # 广西壮族自治区
            # 新疆维吾尔自治区
            # 西藏自治区
            # 黑龙江省
            s = s.replace(u"内蒙古自治区",u"内蒙古").replace(u"宁夏回族自治区",u"宁夏")\
                .replace(u"广西壮族自治区",u"广西").replace(u"新疆维吾尔自治区",u"新疆")\
                .replace(u"西藏自治区",u"西藏").replace(u"黑龙江省",u"黑龙江")

            k_v = lawyer + "|" + s

            return lawyer,s,k_v
        else:
            return None,None,None

    def trans(x):
        lawyer = []
        law_office = []
        plain = []
        defen = []
        if x[1] and x[1] != "":
            js = json.loads(x[1])
            for k in js:
                name,office,k_v = deal_lawyer(k, js[k])
                if not name:
                    continue
                lawyer.append(name)
                law_office.append(office)
                plain.append(k_v)

        if x[2] and x[2] != "":
            js2 = json.loads(x[2])
            for k2 in js2:
                name2, office2, k_v2 = deal_lawyer(k2, js2[k2])
                if not name2:
                    continue
                lawyer.append(name2)
                law_office.append(office2)
                defen.append(k_v2)


        return (x[0],plain,defen,"||".join(lawyer),"||".join(list(set(law_office))),x[3])

    lawyer_k_v = df.map(lambda x:(x[1]+"|"+x[2], str(x[0])))  #（unicode,str）(律师|律所，id)
    tr = df2.map(lambda x:get_plaintiff_defendant(x)).filter(lambda x:filter_(x)).map(lambda x:trans(x)).cache()    #（str list list），需要将id的类型int转为str，才可以join，连接。
    # tr.foreach(p)

    #注意：这里加不加filter(filter_)过滤函数都一样，flatMapValues对value为[]进行展开时，不会返回包含该[]对应key任何记录。
    s1 = tr.map(lambda x:(x[0],x[1])).flatMapValues(lambda x:x).filter(filter_).map(lambda x:(x[1],x[0])).groupByKey().mapValues(lambda v:get_ids(v))  # (plaintiff_info,id)
    # s1.foreach(p_)

    s2 = tr.map(lambda x:(x[0],x[2])).flatMapValues(lambda x:x).filter(filter_).\
        map(lambda x:(x[1],x[0])).groupByKey().mapValues(lambda v:get_ids(v))  #（defendant_info,id）

    lawyer_law_office = tr.map(lambda x:(x[0],(x[3],x[4],x[5])))
    # s2.foreach(p_)
    result_s1 = lawyer_k_v.join(s1).map(lambda x:x[1]).flatMapValues(lambda x:(x.split("||"))).map(lambda x:(x[1],x[0])).groupByKey().mapValues(lambda x:(get_lawyer_ids(x)))
    # result_s1.foreach(p_)
    result_s2 = lawyer_k_v.join(s2).map(lambda x:x[1]).flatMapValues(lambda x:(x.split("||"))).map(lambda x:(x[1],x[0])).groupByKey().mapValues(lambda x:(get_lawyer_ids(x)))
    # result_s2.foreach(p_)
    id_result = result_s1.fullOuterJoin(result_s2).map(lambda x:get_lawyer_id(x))
        # .map(lambda x:(x[0],x[1][0],x[1][1]))

    #id ，lawyer，law_office，plaintiff_id,defendant_id，lawyer_id

    all_result = lawyer_law_office.leftOuterJoin(id_result).map(lambda x:get_all_result(x))

    schema = StructType([StructField("id", IntegerType(), False),
                         StructField("lawyer", StringType(), True),
                         StructField("law_office", StringType(), True),
                         StructField("uuid", StringType(), True),
                         StructField("plaintiff_id", StringType(), True),
                         StructField("defendant_id", StringType(), True),
                         StructField("lawyer_id", StringType(), True)])

    f = sqlContext.createDataFrame(all_result, schema=schema)
    # f.show()
    # , mode = "overwrite"
    # useUnicode = true & characterEncoding = utf8，指定写入mysql时的数据编码，否则会乱码。
    f.write.jdbc(url='jdbc:mysql://cdh5-slave2:3306/laws_doc_adjudication?useUnicode=true&characterEncoding=utf8', table='adjudication_civil_etl_v2_lawyer_id',properties={"user": "weiwc", "password": "HHly2017."})

    sc.stop()