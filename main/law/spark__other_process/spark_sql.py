# -*- coding: utf-8 -*-
from pyspark import SparkContext,SparkConf,SQLContext
import HTMLParser
import numpy as np
np.random.seed(1337)
import os
import sys
from six.moves import zip
from keras.preprocessing import sequence
from keras.models import Model
from keras.layers import Input, merge
from keras.layers import GRU, Dense, Embedding, ChainCRF, LSTM, Bidirectional, Dropout
from keras.layers.wrappers import TimeDistributed
from keras.layers.convolutional import Conv1D,ZeroPadding1D
from keras.optimizers import Adam, RMSprop
from keras.preprocessing.sequence import pad_sequences
from keras.utils.data_utils import get_file
from keras.callbacks import Callback
from subprocess import Popen, PIPE, STDOUT

def format_html_to_line(x):
   """filter html tag"""
   l = []
   l.append(x['type'] + "_" + x['casedate'] + "_" + x['uuid'])
   content = x['doc_content']
   content_text = HTMLParser.HTMLParser().unescape(content)
   from lxml import etree
   selector = etree.HTML(content_text)
   line = selector.xpath('string(*)').encode("utf8")
   line = line.replace(' ', '')
   if line == "":
        return ""
   else:
        l.append(line)
        return l

import pickle


X_train=pickle.load(open("/home/weiwc/pkl/X_train.pkl",'rb'))
Y_train=pickle.load(open("/home/weiwc/pkl/Y_train.pkl",'rb'))
index_word=pickle.load(open("/home/weiwc/pkl/index_word.pkl",'rb'))
dict_word=pickle.load(open("/home/weiwc/pkl/dict_word.pkl",'rb'))
index_tag=pickle.load(open("/home/weiwc/pkl/index_tag.pkl",'rb'))
dict_tag=pickle.load(open("/home/weiwc/pkl/dict_tag.pkl",'rb'))

# X_train=pickle.load(open("pkl/X_train.pkl",'rb'))
# Y_train=pickle.load(open("pkl/Y_train.pkl",'rb'))
# index_word=pickle.load(open("pkl/index_word.pkl",'rb'))
# dict_word=pickle.load(open("pkl/dict_word.pkl",'rb'))
# index_tag=pickle.load(open("pkl/index_tag.pkl",'rb'))
# dict_tag=pickle.load(open("pkl/dict_tag.pkl",'rb'))
# from keras.preprocessing.sequence import pad_sequences


def pad_sequences(sequences, maxlen=None, dtype='int32',
                  padding='pre', truncating='pre', value=0.):
    '''Pads each sequence to the same length:
    the length of the longest sequence.

    If maxlen is provided, any sequence longer
    than maxlen is truncated to maxlen.
    Truncation happens off either the beginning (default) or
    the end of the sequence.

    Supports post-padding and pre-padding (default).

    # Arguments
        sequences: list of lists where each element is a sequence
        maxlen: int, maximum length
        dtype: type to cast the resulting sequence.
        padding: 'pre' or 'post', pad either before or after each sequence.
        truncating: 'pre' or 'post', remove values from sequences larger than
            maxlen either in the beginning or in the end of the sequence
        value: float, value to pad the sequences to the desired value.

    # Returns
        x: numpy array with dimensions (number_of_sequences, maxlen)
    '''
    lengths = [len(s) for s in sequences]

    nb_samples = len(sequences)
    if maxlen is None:
        maxlen = np.max(lengths)

    # take the sample shape from the first non empty sequence
    # checking for consistency in the main loop below.
    sample_shape = tuple()
    for s in sequences:
        if len(s) > 0:
            sample_shape = np.asarray(s).shape[1:]
            break

    x = (np.ones((nb_samples, maxlen) + sample_shape) * value).astype(dtype)
    for idx, s in enumerate(sequences):
        if len(s) == 0:
            continue  # empty list was found
        if truncating == 'pre':
            trunc = s[-maxlen:]
        elif truncating == 'post':
            trunc = s[:maxlen]
        else:
            raise ValueError('Truncating type "%s" not understood' % truncating)

        # check `trunc` has expected shape
        trunc = np.asarray(trunc, dtype=dtype)
        if trunc.shape[1:] != sample_shape:
            raise ValueError('Shape of sample %s of sequence at position %s is different from expected shape %s' %
                             (trunc.shape[1:], idx, sample_shape))

        if padding == 'post':
            x[idx, :len(trunc)] = trunc
        elif padding == 'pre':
            x[idx, -len(trunc):] = trunc
        else:
            raise ValueError('Padding type "%s" not understood' % padding)
    return x

def get_X(ll):
    content = ll[1]
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

    X_test_cut=pad_sequences(X_test_cut,maxlen=max_sen_len,padding='post')
    l = []
    l.append(X_test_cut)
    l.append(X_test_len)
    l.append(word_sen)
    l.append(ll[0])       #rowkey
    return l
# f = open("ner_dev","r")
# get_X("山西省闻喜县人民法院刑事判决书（2016）晋0823刑初26号公诉机关山西省闻喜县人民检察院。被告人任新生，曾用名任广敏，男，1972年3月16日出生，汉族，初中文化，山东省人，农民。2015年12月9日因涉嫌犯危险驾驶罪经闻喜县公安局决定被取保候审，2016年3月10日经本院决定被取保候审。山西省闻喜县人民检察院以闻检公诉刑诉（2016）12号起诉书指控被告人任新生犯危险驾驶罪，于2016年3月8日向本院提起公诉。本院依法适用简易程序，实行独任审判，公开开庭审理了本案。闻喜县人民检察院指派代理检察员张方舟出庭支持公诉，被告人任新生到庭参加诉讼。现已审理终结。经审理查明，2015年11月30日15时48分，被告人任新生醉酒后驾驶鲁R*****起亚牌小型轿车，由运城上高速前往闻喜，行驶至闻喜县高速出口时，被闻喜县公安局交警大队秩序中队民警查获。经山西省运城市道路交通事故司法鉴定所鉴定，其血样中酒精含量为174.83mg/100ml。上述事实在开庭审理时被告人任新生未提出异议，且有闻喜县公安局受案登记表、立案决定书，查获经过，涉嫌酒后驾车驾驶人血样提取登记表及照片，证人黄某某、卫某、关某某的证言，驾驶证及驾驶人信息查询结果单，行车证及机动车信息查询结果单，山西省运城道路交通事故司法鉴定所运城道交所[2015]酒检字第1650号血液酒精含量检验报告书，户籍证明，被告人任新生的供述与辩解等证据予以证实，相互印证，足以认定。本院认为，被告人任新生醉酒后驾驶机动车在高速公路上行驶，其行为已构成危险驾驶罪，且应从重处罚。鉴于其归案后能如实供认自己的罪行，庭审中又自愿认罪，依法可酌情从轻处罚。据此，依据《中华人民共和国刑法》第一百三十三条之一、第五十二条之规定，判决如下：被告人任新生犯危险驾驶罪，判处拘役二个月，并处罚金人民币2000元（已缴纳）。（刑期从判决执行之日起计算。判决执行以前先行羁押的，羁押一日折抵刑期一日。）如不服本判决，可在接到判决书的第二日起十日内，通过本院或者直接向山西省运城市中级人民法院提出上诉。书面上诉的，应当提交上诉状正本一份，副本二份。代理审判员u3000u3000尹国锋二〇一六年三月十六日书u3000记u3000员u3000u3000樊泽明")

def save_result_to_hbase(x):
    nb_word = len(index_word)  # 1008
    nb_tag = len(index_tag)  # 16/14
    maxlen = 100
    word_embedding_dim = 100
    lstm_dim = 100
    batch_size = 64

    word_input = Input(shape=(maxlen,), dtype='float32', name='word_input')
    word_emb = Embedding(nb_word, word_embedding_dim, input_length=maxlen, dropout=0.2, name='word_emb')(word_input)
    bilstm = Bidirectional(LSTM(lstm_dim, dropout_W=0.1, dropout_U=0.1, return_sequences=True))(word_emb)
    bilstm_d = Dropout(0.1)(bilstm)

    half_window_size = 5

    paddinglayer = ZeroPadding1D(padding=half_window_size)(word_emb)
    conv = Conv1D(nb_filter=50, filter_length=(2 * half_window_size + 1), border_mode='valid')(paddinglayer)
    conv_d = Dropout(0.1)(conv)
    dense_conv = TimeDistributed(Dense(50))(conv_d)
    rnn_cnn_merge = merge([bilstm_d, dense_conv], mode='concat', concat_axis=2)

    dense = TimeDistributed(Dense(nb_tag))(rnn_cnn_merge)
    crf = ChainCRF()
    crf_output = crf(dense)

    model = Model(input=[word_input], output=[crf_output])

    model.compile(loss=crf.sparse_loss,
                  optimizer=RMSprop(0.001),
                  metrics=['sparse_categorical_accuracy'])

    model.load_weights('/home/weiwc/pkl/model.weights')
    # model.load_weights('model.weights')
    X_test_cut = x[0]
    X_test_len = x[1]
    X_word = x[2]
    rowkey = str(x[3])


    Y_pred = model.predict(X_test_cut)

    j2=0
    i2=0
    t = []
    tt = []
    for i in range(12):
        tt.append([])
    for j1 in range(len(X_word)):
        # index_tag {0: 'PAD', 1: 'O', 2: 'B-ROLE', 3: 'I-ROLE', 4: 'B-PER', 5: 'I-PER', 6: 'B-CRIME', 7: 'I-CRIME', 8: 'B-TIME',
        #  9: 'I-TIME', 10: 'B-ORG', 11: 'I-ORG', 12: 'B-LOC', 13: 'I-LOC'}
        w = X_word[j1]
        tags = Y_pred[i2][j2]
        tag_flag  = False
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
    # taglist = ['B_ROLE','I_ROLE','B_PER','I_PER','B_CRIME','I_CRIME','B_TIME','I_TIME','B_ORG','I_ORG','B_LOC','I_LOC']
    ret_t = {'PER': [], 'LOC': [], 'ORG': [], 'TIME': [], 'ROLE': [], 'CRIME': []}
    # index_tag {0: 'PAD', 1: 'O', 2: 'B-ROLE', 3: 'I-ROLE', 4: 'B-PER', 5: 'I-PER', 6: 'B-CRIME', 7: 'I-CRIME', 8: 'B-TIME',
    #  9: 'I-TIME', 10: 'B-ORG', 11: 'I-ORG', 12: 'B-LOC', 13: 'I-LOC'}
    id = 0
    for i in l22:
        ret_t[i[0].split("-")[1]].append(l23[id])
        id += 1

    t2 = []
    for i in ret_t.keys():
        tmp = (rowkey, [rowkey, "d", i, ",".join(ret_t[i])])
        t2.append(tmp)
    # for i in t2:
    #     print i[1][2],i[1][3]

    return t2
    # return "-"

def p(i):
    print "=================="
    print type(i)
    for s in i :
        print type(s), s
        print "--------------------------------------"



if __name__ == "__main__":
    if len(sys.argv) > 2:
        host = sys.argv[1]
        hbase_table = sys.argv[2]
        # hbase_table = sys.argv[3]
    else:
        host = '192.168.10.24'
        # hbase_table = 'laws_doc:judgment'
        hbase_table = 'laws_doc:label'

    conf = SparkConf()
    sc = SparkContext(conf=conf)
    sqlContext = SQLContext(sc)
    # sc.setLogLevel("ERROR")  # ALL, DEBUG, ERROR, FATAL, INFO, OFF, TRACE, WARN

    df = sqlContext.read.jdbc(url='jdbc:mysql://cdh-slave2:3306/laws_doc', table='judgment',
                              predicates=["id > 0 and id <= 3000", "id > 3000 and id <= 6000",
                                          "id > 6000 and id <= 9000"],
                              properties={"user": "root", "password": "root"})
    # df = sqlContext.read.jdbc(url='jdbc:mysql://cdh-slave2:3306/laws_doc', table='judgment',predicates=["id <= 10000","id > 10000 and id <= 20000","id > 20000 and id <= 30000","id > 30000 and id <= 40000","id > 40000 and id <= 50000","id > 50000 and id <= 60000","id > 60000 and id <= 70000","id > 70000 and id <= 80000","id > 80000 and id <= 90000","id > 90000 and id <= 10000"],properties={"user":"root","password":"root"})
    # df = sqlContext.read.jdbc(url='jdbc:mysql://cdh-slave2:3306/laws_doc', table='judgment',predicates=["id <= 10000","id > 10000 and id <= 20000","id > 20000 and id <= 30000","id > 30000 and id <= 40000","id > 40000 and id <= 50000","id > 50000 and id <= 60000","id > 60000 and id <= 70000","id > 70000 and id <= 80000","id > 80000 and id <= 90000","id > 90000 and id <= 100000"],properties={"user":"root","password":"root"})
    # df = sqlContext.read.jdbc(url='jdbc:mysql://cdh-slave2:3306/laws_doc', table='judgment',predicates=["id <= 2","id > 2 and id <=4","id > 4 and id <=6","id > 6 and id <=8","id > 8 and id <=10","id > 10 and id <=12","id > 12 and id <=14"],properties={"user":"root","password":"root"})
    # df = sqlContext.read.jdbc(url='jdbc:mysql://cdh-slave2:3306/laws_doc', table='judgment',predicates=["id <= 1","id > 1 and id <=2"],properties={"user":"root","password":"root"})
    conf = {"hbase.zookeeper.quorum": host,
            "hbase.mapred.outputtable": hbase_table,
            "mapreduce.outputformat.class": "org.apache.hadoop.hbase.mapreduce.TableOutputFormat",
            "mapreduce.job.output.key.class": "org.apache.hadoop.hbase.io.ImmutableBytesWritable",
            "mapreduce.job.output.value.class": "org.apache.hadoop.io.Writable"}
    keyConv = "hbase.pythonconverters.StringToImmutableBytesWritableConverter"
    valueConv = "hbase.pythonconverters.StringListToPutConverter"

    df.map(lambda x: format_html_to_line(x)).map(lambda x: get_X(x)).flatMap(lambda x: save_result_to_hbase(x)).\
        saveAsNewAPIHadoopDataset(conf=conf, keyConverter=keyConv, valueConverter=valueConv)

    sc.stop()