from __future__ import print_function, unicode_literals

import numpy as np

np.random.seed(1337)
from keras.models import Model, save_model
from keras.layers import Input, merge
from keras.layers import Dense, Embedding, LSTM, Bidirectional, Dropout, ChainCRF
from keras.layers.wrappers import TimeDistributed
from keras.layers.convolutional import Conv1D,ZeroPadding1D
from keras.optimizers import RMSprop
from keras.callbacks import Callback
import data
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "1"
X_test_cut,X_test_len,X_word = data.get_X('ner_dev1')
# print("len X_test_cut",len(X_test_cut)) #4043
# print("x_test_cut",X_test_cut[0]) #[ 2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 14 15 18 12 19 20 21 22 23...0 0 0 0]
# print("X_test_len",len(X_test_len)) #4043
# print("X_test_len",X_test_len[0]) #70
# print("X_word",len(X_word)) #4008
# print("X_word",X_word[10])

class Callback(Callback):
    def on_epoch_end(self, epoch, logs={}):
        
        Y_pred = model.predict(X_test_cut)
        data.write_result_to_file('ner_pre', Y_pred, X_test_len, X_word)
        print()
        os.system('python evaluate.py ner_pre ner_dev1')

maxlen = 100 
word_embedding_dim = 100
lstm_dim = 100
batch_size = 64

print('Loading data...')

nb_word = len(data.index_word)
nb_tag = len(data.index_tag)

X_train = data.X_train
Y_train = data.Y_train
Y_train = np.expand_dims(Y_train, -1)

print('Unique words:', nb_word)
print('Unique tags:', nb_tag)
print('X_train shape:', X_train.shape)
print('Y_train shape:', Y_train.shape)

print('Build model...')

word_input = Input(shape=(maxlen,), dtype='float32', name='word_input')
word_emb = Embedding(nb_word, word_embedding_dim, input_length=maxlen, dropout=0.2, name='word_emb')(word_input)
bilstm = Bidirectional(LSTM(lstm_dim, dropout_W=0.1, dropout_U=0.1, return_sequences=True))(word_emb)
bilstm_d = Dropout(0.1)(bilstm)

half_window_size=5

paddinglayer=ZeroPadding1D(padding=half_window_size)(word_emb)
conv=Conv1D(nb_filter=50,filter_length=(2*half_window_size+1),border_mode='valid')(paddinglayer)
conv_d = Dropout(0.1)(conv)
dense_conv = TimeDistributed(Dense(50))(conv_d)
rnn_cnn_merge=merge([bilstm_d,dense_conv], mode='concat', concat_axis=2)


dense = TimeDistributed(Dense(nb_tag))(rnn_cnn_merge)
crf = ChainCRF()
crf_output = crf(dense)

model = Model(input=[word_input], output=[crf_output])

model.compile(loss=crf.sparse_loss,
              optimizer=RMSprop(0.01),
              metrics=['sparse_categorical_accuracy'])

model.summary()

# model.load_weights('model.weights')
mCallBack = Callback()
model.fit(X_train, Y_train,
        batch_size=batch_size, nb_epoch=8, callbacks=[mCallBack])
save_model(model, "model_ner.hd5")
model.save_weights('model.weights')
