# encoding:utf-8
import happybase
import pandas as pd
import time,datetime
from datetime import datetime
import jieba
jieba.load_userdict('../data/dict_title.txt')   # 加载词典
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['font.sans-serif'] = ['SimHei']
import json

def read_dict(dict_file):
    dict = []
    for word in open(dict_file, "r"):
        dict.append(word.strip())
    return dict

def fre_word(data,dict):
    text = ""
    for line in data:
        text += line + ";"
    words = jieba.cut(text, cut_all=False)
    ww = [w for w in words if w.encode('utf-8') in dict]
    # 计算词频
    word_freq = {}
    for word in ww:
        if word in word_freq:
            word_freq[word] += 1
        else:
            word_freq[word] = 1
    freq_word = []
    for word, freq in word_freq.items():
        freq_word.append((word, freq))
    freq_word.sort(key=lambda x: x[1], reverse=True)
    return freq_word

def change_time(time):
    if u'年' in time:
        time = time.replace(u'年', '-')
    if u'月' in time:
        time = time.replace(u'月', '-')
    if u'日' in time:
        time = time.replace(u'日', '')
    # # print v['d:time'].decode('utf-8')
    if time:
        try:
            time_datetime = datetime.strptime(time.strip(), '%Y-%m-%d')
            time = time_datetime.strftime('%Y-%m-%d')
        except ValueError:
            time_datetime = datetime.strptime(time.encode('utf8'), '%Y年%m月%d日')
            time = time_datetime.strftime('%Y-%m-%d')
    return time

def get_time_title(table,prefix,time_name,title_name):
    new_title = []
    for k,v in table.scan(row_prefix=prefix):
        time = change_time(v[time_name])
        dict = {}
        dict['time'] = time
        dict['title'] = v[title_name]
        new_title.append(dict)
    time_title = pd.DataFrame(new_title)
    tm = pd.to_datetime(time_title['time'])
    time_title['to_time'] = tm
    time_title = time_title.set_index('to_time')
    before_title = time_title['2016-1-1':'2016-12-23'].title
    middle_title = time_title['2016-12-24':'2017-03-09'].title
    after_title = time_title['2017-03-10':'2017-04-27'].title
    return before_title,middle_title,after_title

def plot_barh(freq_word,plot_title,d):
    zhuti = []
    zhuti_fre = []
    for i in freq_word[:d]:
        # print i[0],i[1]
        zhuti.append(i[0])
        zhuti_fre.append(int(i[1]))
    y_pos = np.arange(d)
    # print y_pos
    plt.barh(y_pos, zhuti_fre, color='blue', align='center', alpha=0.4)
    plt.yticks(y_pos, zhuti)
    plt.xlabel(u'频率')
    plt.title(plot_title)
    plt.show()

if __name__ == "__main__":
    conn = happybase.Connection('192.168.10.24', timeout=300000)
    table = conn.table('public_sentiment')
    prefix01 = '嫘祖杯01'  # 新闻
    prefix02 = '嫘祖杯02'  # 微博
    prefix03 = '嫘祖杯03'  # 微信
    time_name = 'd:time'
    title_name = 'd:title'
    content_name = 'd:content'
    new_before_title, new_middle_title, new_after_title = get_time_title(table, prefix01, time_name, title_name)
    wechat_before_title, wechat_middle_title, wechat_after_title = get_time_title(table, prefix03, time_name,
                                                                                  title_name)
    weibo_before_title, weibo_middle_title, weibo_after_title = get_time_title(table, prefix02, time_name,
                                                                                content_name)

    dict_file = '../data/dict_title.txt'
    dict = read_dict(dict_file)
    # print wechat_after_title
    freq_word1 = fre_word(weibo_before_title, dict)
    freq_word2 = fre_word(weibo_middle_title, dict)
    freq_word3 = fre_word(weibo_after_title, dict)
    title_dict = {}
    new_title_dict1 = {}
    for i in freq_word1[:5]:
        # print i[0],i[1]
        new_title_dict1[i[0]] = i[1]
    new_title_dict2 = {}
    for i in freq_word2[:10]:
        print i[0], i[1]
        new_title_dict2[i[0]] = i[1]
    new_title_dict3 = {}
    for i in freq_word3[:5]:
        # print i[0], i[1]
        new_title_dict3[i[0]] = i[1]
    title_dict[u'赛前'] = new_title_dict1
    title_dict[u'赛中'] = new_title_dict2
    title_dict[u'赛后'] = new_title_dict3
    print title_dict
    print json.dumps(title_dict)
    # d = 5
    # plot_title = u'新闻赛前主题分布'
    # plot_barh(freq_word,plot_title,d)