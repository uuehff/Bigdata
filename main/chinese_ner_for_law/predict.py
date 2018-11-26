# -*- coding: utf-8 -*-

#from __future__ import print_function, unicode_literals
import numpy as np
np.random.seed(1337)
from keras.models import load_model
import data
#
# nb_word = len(data.index_word)  #1008
# nb_tag = len(data.index_tag) #16/14
# maxlen = 100
# word_embedding_dim = 100
# lstm_dim = 100
# batch_size = 64
#
# word_input = Input(shape=(maxlen,), dtype='float32', name='word_input')
# word_emb = Embedding(nb_word, word_embedding_dim, input_length=maxlen, dropout=0.2, name='word_emb')(word_input)
# bilstm = Bidirectional(LSTM(lstm_dim, dropout_W=0.1, dropout_U=0.1, return_sequences=True))(word_emb)
# bilstm_d = Dropout(0.1)(bilstm)
#
# half_window_size=5
#
# paddinglayer=ZeroPadding1D(padding=half_window_size)(word_emb)
# conv=Conv1D(nb_filter=50,filter_length=(2*half_window_size+1),border_mode='valid')(paddinglayer)
# conv_d = Dropout(0.1)(conv)
# dense_conv = TimeDistributed(Dense(50))(conv_d)
# rnn_cnn_merge=merge([bilstm_d,dense_conv], mode='concat', concat_axis=2)
#
#
# dense = TimeDistributed(Dense(nb_tag))(rnn_cnn_merge)
# crf = ChainCRF()
# crf_output = crf(dense)
#
#
#
#
# model = Model(input=[word_input], output=[crf_output])
#
# model.compile(loss=crf.sparse_loss,
#               optimizer=RMSprop(0.001),
#               metrics=['sparse_categorical_accuracy'])
load_model("model_ner.hd5")
model.load_weights('model.weights')



# from pyspark import SparkContext,SparkConf,SQLContext
# from pyspark.sql import DataFrameReader

# conf  = SparkConf().setMaster("local[4]").setAppName("test_mysql")
# sc = SparkContext(conf=conf)
# sqlContext = SQLContext(sc)
#
# df = sqlContext.read.jdbc(url='jdbc:mysql://localhost:3306/test', table='test123',properties={"user":"root","password":"root"})

# tt.printSchema()
# root  # 所有字段类型都是string的！
# | -- columnFamily: string(nullable=true)
# | -- qualifier: string(nullable=true)
# | -- row: string(nullable=true)
# | -- timestamp: string(nullable=true)
# | -- type: string(nullable=true)
# | -- value: string(nullable=true)
#
# tt.select("columnFamily").show()
# tt.select("columnFamily").distinct().show()
# tt.select("row", "value").show()

# tt.select(tt['columnFamily'], tt.columnFamily).show()
# tt.filter(tt['qualifier'] == 'url').count()

# print df.show()
# sc.stop()

X_test_cut,X_test_len,X_word= data.get_X("ner_dev1")

Y_pred = model.predict(X_test_cut)
print X_test_len
print X_word
print type(Y_pred)
print Y_pred
print len(Y_pred[0])
print len(Y_pred)
print len(Y_pred[1])
# data.write_result_to_file("ner_pre2",Y_pred,X_test_len,X_word)
