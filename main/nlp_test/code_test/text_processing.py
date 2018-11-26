# -*- coding: utf-8 -*-
# 加工原料文本

# 捕获用户输入
# 有时我们想捕捉用户与我们的程序交互时输入的文本。调用Python 函数raw_input()
# 提示用户输入一行数据。保存用户输入到一个变量后，我们可以像其他字符串那样操纵它。
# >>> s = raw_input("Enter some text: ")
# Enter some text: On an exceptionally hot evening early in July
# >>> print "You typed", len(nltk.word_tokenize(s)), "words."
# You typed 8 words.


#不换行
# 我们可以写一个for 循环，遍历字符串中的字符。print 语句结尾加一个逗号，这是为
# 了告诉Python 不要在行尾输出换行符。
# import nltk
# sent = 'colorless green ideas sleep furiously'
# for word in nltk.word_tokenize(sent):
#     print word,         #加，可保证不换行

# colorless green ideas sleep furiously
# =============================================================
# 字符串操作：
# s.find(t) 字符串s 中包含t 的第一个索引（没找到返回-1）
# s.rfind(t) 字符串s 中包含t 的最后一个索引（没找到返回-1）
# s.index(t) 与s.find(t)功能类似，但没找到时引起ValueError
# s.rindex(t) 与s.rfind(t)功能类似，但没找到时引起ValueError
# s.join(text) 连接字符串s 与text 中的词汇
# s.split(t) 在所有找到t 的位置将s 分割成链表（默认为空白符）
# s.splitlines() 将s 按行分割成字符串链表
# s.lower() 将字符串s 小写
# s.upper() 将字符串s 大写
# s.titlecase() 将字符串s 首字母大写
# s.strip() 返回一个没有首尾空白字符的s 的拷贝
# s.replace(t, u) 用u 替换s 中的t

# 编码
# import nltk
# import codecs
# path = nltk.data.find('corpora/unicode_samples/polish-lat2.txt')
# f = codecs.open(path, encoding='latin2')
# codecs.open()

# 序列操作

# for item in s 遍历s 中的元素
# for item in sorted(s) 按顺序遍历s 中的元素
# for item in set(s) 遍历s 中的无重复的元素
# for item in reversed(s) 按逆序遍历s 中的元素
# for item in set(s).difference(t) 遍历在集合s 中不在集合t 的元素
# for item in random.shuffle(s) 按随机顺序遍历s 中的元素

# ；例如：要获得无重复的逆序排列的
# s 的元素，可以使用reversed(sorted(set(s)))。
# 我们可以在这些序列类型之间相互转换。例如：tuple(s)将任何种类的序列转换成一个
# 元组，list(s)将任何种类的序列转换成一个链表。我们可以使用join()函数将一个字符串链
# 表转换成单独的字符串，例如：':'.join(words)。

# 字典操作

# d = {} 创建一个空的字典，并将分配给d
# d[key] = value 分配一个值给一个给定的字典键
# d.keys() 字典的键的链表
# list(d) 字典的键的链表
# sorted(d) 字典的键，排序
# key in d 测试一个特定的键是否在字典中
# for key in d 遍历字典的键
# d.values() 字典中的值的链表
# dict([(k1,v1), (k2,v2), ...]) 从一个键-值对链表创建一个字典
# d1.update(d2) 添加d2 中所有项目到d1
# defaultdict(int) 一个默认值为0 的字典


# 开发一个已标注语料库是一个重大的任务。
from nltk import UnigramTagger
UnigramTagger.evaluate()