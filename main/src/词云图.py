# -*- coding: utf-8 -*-
import jieba
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud


jieba.load_userdict('E:\\PycharmProjects\\data_etl\\data\\dict.txt')

def stopWord(stopword_file):
    stopwords = []
    for word in open(stopword_file, 'r'):
        stopwords.append(word.strip())
    return stopwords

def fre_word(text_file,stopwords):
    data = pd.read_csv(text_file, sep=',', skiprows=[1], encoding='gb18030')
    text = ""
    for line in data.title:
        text += line + ";"
    words = jieba.cut(text, cut_all=False)
    ww = [w for w in words if w.encode('utf-8') not in stopwords]
    word_freq = {}
    for word in ww:
        if word in word_freq:
            word_freq[word] += 1
        else:
            word_freq[word] = 1

    # for word, freq in word_freq.items():
    #     if freq > 1:
    #         print word,"\t",freq
    freq_word = []
    for word, freq in word_freq.items():
        freq_word.append((word, freq))
    freq_word.sort(key=lambda x: x[1], reverse=True)
    return freq_word

def word_cloud(freq_word):
    wc = WordCloud(font_path='C:\Python27\Lib\site-packages\matplotlib\mpl-data\fonts\ttf\simhei.ttf',
                   max_font_size=200, random_state=30).fit_words(freq_word[:100])

    plt.imshow(wc)
    plt.axis("off")
    plt.show()

if __name__ == '__main__':
    stopword_file = 'E:\\PycharmProjects\\data_etl\\data\\stopword.txt'
    stopwords = stopWord(stopword_file)
    text_file = 'E:\\PycharmProjects\\data_etl\\data\weixin_new.csv'
    freq_word = fre_word(text_file, stopwords)
    # print freq_word[:100]
    #
    word_cloud(freq_word)