# -*- coding: utf-8 -*-
import pymysql
import re
import jieba

# 支持三种分词模式：
#
# 全模式，把句子中所有的可以成词的词语都扫描出来, 速度非常快，但是不能解决歧义；
# 精确模式，试图将句子最精确地切开，适合文本分析；
# 搜索引擎模式，在精确模式的基础上，对长词再次切分，提高召回率，适合用于搜索引擎分词。

if __name__ == '__main__':
    # seg_list = jieba.cut(u"我来到北京清华大学", cut_all=True)        #全模式
    # seg_list = jieba.cut(u"我来到北京清华大学")        #默认是精确模式
    # seg_list = jieba.cut_for_search(u"我来到北京清华大学",HMM=True)        #检索模式，对长词再进行切分

    seg_list = jieba.lcut(u"我来到北京清华大学", cut_all=True)  # 全模式,返回list
    # seg_list = jieba.lcut_for_search(u"我来到北京清华大学", HMM=True)  # 检索模式，返回list
    print("Full Mode: " + "/ ".join(seg_list))
    print(type(seg_list))

