# -*- coding: utf-8 -*-
import HTMLParser

import pymysql
import re
from keras.models import model_from_json
# get_X()
import pickle

X_train=pickle.load(open("/home/weiwc/pkl/X_train.pkl",'rb'))
Y_train=pickle.load(open("/home/weiwc/pkl/Y_train.pkl",'rb'))
index_word=pickle.load(open("/home/weiwc/pkl/index_word.pkl",'rb'))
dict_word=pickle.load(open("/home/weiwc/pkl/dict_word.pkl",'rb'))
index_tag=pickle.load(open("/home/weiwc/pkl/index_tag.pkl",'rb'))
dict_tag=pickle.load(open("/home/weiwc/pkl/dict_tag.pkl",'rb'))
model = model_from_json(open("/home/weiwc/pkl/model_ner.json").read())
model.load_weights('/home/weiwc/pkl/model.weights')

from keras.preprocessing.sequence import pad_sequences


from keras.models import Model
from keras.layers import Input, merge
# from keras.layers import Dense, Embedding, ChainCRF, LSTM, Bidirectional, Dropout
from keras.layers.wrappers import TimeDistributed
from keras.layers.convolutional import Conv1D,ZeroPadding1D
from keras.optimizers import RMSprop


def format_html_to_line(content):
   """filter html tag"""
   content_text = HTMLParser.HTMLParser().unescape(content)
   from lxml import etree
   selector = etree.HTML(content_text)
   line = selector.xpath('string(*)').encode("utf8")
   line = line.replace(' ', '')
   if line == "":
        return ""
   else:
        return line

def get_X(content):
    x_sen=[]
    word_sen=[]
    content = content.decode("utf-8")
    for line in content:
        line=line.strip().encode("utf-8")
        word_sen.append(line)
        if line in dict_word:
            x_sen.append(dict_word[line])
        else:
            x_sen.append(1)
    X_test_cut=[]
    X_test_len=[]
    max_sen_len=100
    while len(x_sen)>max_sen_len:
        flag=False
        for j in reversed(range(100)):
            if x_sen[j]==dict_word['，'] or x_sen[j]==dict_word['、']:
                X_test_cut.append(x_sen[:j+1]) #将，、及其之前的字符添加到X_test_cut
                X_test_len.append(j+1)
                x_sen=x_sen[j+1:]
                break
            if j==0:
                flag=True
        if flag:
            X_test_cut.append(x_sen[:100])
            x_sen=x_sen[100:]
            X_test_len.append(100)
    if len(x_sen) <= max_sen_len:
        X_test_cut.append(x_sen)
        X_test_len.append(len(x_sen))
    # print "===========7...%s" % time.time()
    # X_test_cut=pad_sequences(X_test_cut,maxlen=max_sen_len,padding='post')
    # print "===========8...%s" % time.time()
    # l = []
    # l.append(X_test_cut)
    # l.append(X_test_len)
    # l.append(word_sen)
    # l.append(ll[0])       #rowkey

    return X_test_cut,X_test_len,word_sen

def save_result_to_hbase(Y_pred,word_sen,X_test_len):

    # Y_pred = model.predict(X_test_cut)

    j2=0
    i2=0
    t = []
    for j1 in range(len(word_sen)):
        w = word_sen[j1]
        tags = Y_pred[i2][j2]
        t_tmp = []
        for i in range(14):
            if (tags[i] == 1) and i > 1:
                t_tmp.append(index_tag[i])
                t_tmp.append(w)
                t.append(t_tmp)
                break
        j2 += 1
        if j2 == X_test_len[i2]:       #X_test_len = [89, 37, 95, 86, 90, 100, 90, 94, 80, 79, 44, 59]
            j2 = 0
            i2 += 1
    if t:
        l2 = []
        l3 = []
        l22 = []
        l23 = []
        c = 0
        ttl = 0
        for i in t:
            if  i[0].startswith('B') and c == 0:
                l2.append(i[0])
                l3.append(i[1].decode("utf-8"))
                ttl = i[0].replace('B','I')
                c = c + 1

            elif i[0] == ttl:
                l2.append(i[0])
                l3.append(i[1].decode("utf-8"))
            elif i[0].startswith('B') and c != 0:
                l22.append(l2)
                l23.append("".join(l3))
                l2 = []
                l3 = []
                l2.append(i[0])
                l3.append(i[1].decode("utf-8"))
                ttl = i[0].replace('B', 'I')
        l22.append(l2)
        l23.append("".join(l3))
        # print l22
        # print l23
        ret_t = {'PER': [], 'LOC': [], 'ORG': [], 'TIME': [], 'ROLE': [], 'CRIME': []}
        id = 0
        for i in l22:
            ret_t[i[0].split("-")[1]].append(l23[id])
            id += 1
        # t2 = []
        # for i in ret_t.keys():
        #     tmp = ("rowkey", ["rowkey", "d", i, ",".join(ret_t[i])])
        #     t2.append(tmp)
        # for i in t2:
        #     print i[1][2],i[1][3]

        return ret_t

def predict():
    """predict"""
    import time
    print "===========3...%s" % time.time()

    conn = pymysql.connect(host='192.168.10.24', user='root', passwd='root', db='laws_doc', charset='utf8')
    # conn = pymysql.connect(host='localhost', user='root', passwd='root', db='laws_doc', charset='utf8')
    cursor = conn.cursor()
    # sql = 'select a.uuid,a.doc_content from judgment a,tmp_weiwenchao2 b where a.uuid = b.uuid and b.id > 0 and b.id <= 2000 and b.loc is null and b.per is null '
    # sql = 'select a.uuid,a.doc_content from judgment a,tmp_weiwenchao2 b where a.uuid = b.uuid and b.id > 0 and b.id <= 2000 and b.loc is null and b.per is null '
    # cursor.execute(sql2)
    i = 0
    for i in range(2):
        sql = 'select uuid,doc_content from judgment where id > ' + str(i*1000) + ' and id <= ' + str((i+1)*1000)
        # sql = 'select uuid,doc_content from tb_doc where id > 0 and id <= 3 '
        # sql = 'select uuid,doc_content from tb_doc where id > 0 and id <= 3 '
        cursor.execute(sql)
        # row_1 = cursor.fetchone()
        # row_2 = cursor.fetchmany(5)
        row_2 = cursor.fetchall()
        print "===========4...%s" % time.time()
        X_test_cuts = []
        word_sens = []
        X_test_lens = []
        X_test_nums = []
        max_sen_len = 100
        uuids = []
        # l1 = row_2[:1000]
        rl = len(row_2)
        for i in range(rl):

            uuids.append(row_2[i][0])
            content = format_html_to_line(row_2[i][1])

            X_test_cut, X_test_len, word_sen = get_X(content)
            X_test_cuts.extend(X_test_cut)
            word_sens.append(word_sen)
            X_test_lens.append(X_test_len)  #

            X_test_nums.append(len(X_test_len))  # 每个文本的句子个数

        print "===========11...%s" % time.time()
        X_test_cuts = pad_sequences(X_test_cuts, maxlen=max_sen_len, padding='post')
        print "===========12...%s" % time.time()
        Y_preds = model.predict(X_test_cuts)
        print "===========13...%s" % time.time()
        start = 0
        end = 0
        for i in range(rl):
            uuid = uuids[i]
            end += X_test_nums[i]
            Y_pred = Y_preds[start:end]
            start += X_test_nums[i]
            s = save_result_to_hbase(Y_pred,word_sens[i],X_test_lens[i])
            # print "===========14...%s" % time.time()
            if s:
                for i in s.keys():
                    ss = ",".join(s[i]).replace("'", "\\\'").replace('"', '\\\"')  # 替换30°18' 为 30°18\'
                    sql = " update tmp_weiwenchao2 set " + i + " ='" + ss + "' where uuid= '" + uuid + "'"
                    # cursor.executemany(sql)
                    cursor.execute(sql)
                    # print uuid,i, ",".join(s[i])
                    # break
                # print "========================="
                # print "===========15...%s" % time.time()
        conn.commit()

    cursor.close()
    conn.close()
    print "===========16...%s" % time.time()
    print "===========success...%s" % time.time()



if __name__ == "__main__":
    predict()
    

