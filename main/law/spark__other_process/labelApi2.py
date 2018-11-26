# -*- coding: utf-8 -*-
import HTMLParser

import pymysql
import re

# get_X()
import pickle
X_train=pickle.load(open("pkl/X_train.pkl",'rb'))
Y_train=pickle.load(open("pkl/Y_train.pkl",'rb'))
index_word=pickle.load(open("pkl/index_word.pkl",'rb'))
dict_word=pickle.load(open("pkl/dict_word.pkl",'rb'))
index_tag=pickle.load(open("pkl/index_tag.pkl",'rb'))
dict_tag=pickle.load(open("pkl/dict_tag.pkl",'rb'))

# X_train=pickle.load(open("/home/weiwc/pkl/X_train.pkl",'rb'))
# Y_train=pickle.load(open("/home/weiwc/pkl/Y_train.pkl",'rb'))
# index_word=pickle.load(open("/home/weiwc/pkl/index_word.pkl",'rb'))
# dict_word=pickle.load(open("/home/weiwc/pkl/dict_word.pkl",'rb'))
# index_tag=pickle.load(open("/home/weiwc/pkl/index_tag.pkl",'rb'))
# dict_tag=pickle.load(open("/home/weiwc/pkl/dict_tag.pkl",'rb'))

from keras.preprocessing.sequence import pad_sequences

# save_to_Hbase()

from keras.models import Model
from keras.layers import Input, merge
from keras.layers import Dense, Embedding, ChainCRF, LSTM, Bidirectional, Dropout
from keras.layers.wrappers import TimeDistributed
from keras.layers.convolutional import Conv1D,ZeroPadding1D
from keras.optimizers import RMSprop

def get_X(o_content):

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
    # model.load_weights('/home/weiwc/pkl/model.weights')
    model.load_weights('model.weights')

    x_sen=[]
    word_sen=[]
    content_re = o_content.replace(" ","")
    for line in content_re:
        word_sen.append(line)
        if line in dict_word:
            x_sen.append(dict_word[line])
        else:
            x_sen.append(1)
    X_test_cut=[]
    X_test_len=[]
    max_sen_len=100
    if len(x_sen) <= max_sen_len:
        X_test_cut.append(x_sen)
        X_test_len.append(len(x_sen))

    X_test_cut=pad_sequences(X_test_cut,maxlen=max_sen_len,padding='post')
    Y_pred = model.predict(X_test_cut)

    j2=0
    i2=0
    t = []
    for j1 in range(len(word_sen)):
        w = word_sen[j1]
        tags = Y_pred[i2][j2]
        t_tmp = []
        for i in range(14):
            if (tags[i] == 1):
                # t_tmp.append(index_tag[i])
                # t_tmp.append(w)
                # t.append(t_tmp)
                t.append(index_tag[i])
                break
        j2 += 1
        # if j2 == X_test_len[i2]:       #X_test_len = [89, 37, 95, 86, 90, 100, 90, 94, 80, 79, 44, 59]
        #     j2 = 0
        #     i2 += 1
    wl = re.split("[ ]{1,100}", o_content)
    tt = []
    start = 0
    end = 0
    for i in wl:
        end += len(i)
        tt.append(t[start:end])
        start += len(i)
    tt2 = []
    for i in range(len(tt)):
        flag = False
        for j in tt[i]:
            if j.startswith('B'):
                flag = True
                tt2.append("".join(wl[i]) + "|" + j.split("-")[1])
                break
        if not flag:
            for j in tt[i]:
                if j.startswith('I'):
                    flag = True
                    tt2.append("".join(wl[i]) + "|" + j.split("-")[1])
                    break
        if not flag:
            for j in tt[i]:
                tt2.append("".join(wl[i]) + "|" + j)
                break

    return "   ".join(tt2)

if __name__ == '__main__':

    o_content = u"没  满   十六  16  周岁  抢劫  学生   七八  78  次  没用  过  凶器  属于  从犯  这种  情况  要  判   几年"

    print get_X(o_content)