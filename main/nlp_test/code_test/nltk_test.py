# -*- coding: utf-8 -*-

# NLTK官网:   http://www.nltk.org/data
# 语料库使用：    http://www.nltk.org/howto/
# http://www.baidu.com

# 古腾堡语料库
# print gutenberg.fileids()
# text_emma = nltk.Text(nltk.corpus.gutenberg.words('austen-emma.txt'))
# text_emma.concordance("surprize")

# emma = gutenberg.words('austen-emma.txt')
# 这个程序显示每个文本的三个统计量：平均词长、平均句子长度和本文中每个词出现的
# 平均次数（我们的词汇多样性得分）。
# for fileid in gutenberg.fileids():
#     num_chars = len(gutenberg.raw(fileid))
#     num_words = len(gutenberg.words(fileid))
#     num_sents = len(gutenberg.sents(fileid))
#     num_vocab = len(set([w.lower() for w in gutenberg.words(fileid)]))
#     print int(num_chars/num_words), int(num_words/num_sents), int(num_words/num_vocab), fileid
# 注意：raw()函数给我们没有进行过任何语言学处理的文件的内容。因此，例如：len(gutenberg.raw('blake-poems.txt')告诉我们文本中出现的词汇个数，包括词之间的空格。s
# raw:原生的。

# sents()函数把文本划分成句子，其中每一个句子是一个词链表。
# macbeth_sentences = gutenberg.sents('shakespeare-macbeth.txt')
# macbeth_sentences
# [['[', 'The', 'Tragedie', 'of', 'Macbeth', 'by', 'William', 'Shakespeare',
# '1603', ']'], ['Actus', 'Primus', '.'], ...]

# macbeth_sentences[0][1]

# macbeth_sentences[1037]
# ['Double', ',', 'double', ',', 'toile', 'and', 'trouble', ';','Fire', 'burne', ',', 'and', 'Cauldron', 'bubble']
# longest_len = max([len(s) for s in macbeth_sentences])
# [s for s in macbeth_sentences if len(s) == longest_len]
# [['Doubtfull', 'it', 'stood', ',', 'As', 'two', 'spent', 'Swimmers', ',', 'that',
# 'doe', 'cling', 'together', ',', 'And', 'choake', 'their', 'Art', ':', 'The',
# 'mercilesse', 'Macdonwald', ...], ...]
# ========================================================================================================

# 网络和聊天文本
# from nltk.corpus import webtext
# for fileid in webtext.fileids():
# ... print fileid, webtext.raw(fileid)[:65], '...'
# 其中webtext.raw(fileid)[:65]输出从头开始的65个字符，包括原文本中的空格。

#聊天室文本
# from nltk.corpus import nps_chat
# chatroom = nps_chat.posts('10-19-20s_706posts.xml')
# chatroom[123]
# ['i', 'do', "n't", 'want', 'hot', 'pics', 'of', 'a', 'female', ',',
# 'I', 'can', 'look', 'in', 'a', 'mirror', '.']

# ============================================================================
# 布朗语料库
# 我们可以将语料库作为词链表或者句子链表来访问（每个句子本身也是一个词链表）。我们可以指定特定的类别或文件阅读：
# from nltk.corpus import brown
# brown.categories()
# ['adventure', 'belles_lettres', 'editorial', 'fiction', 'government', 'hobbies',
# 'humor', 'learned', 'lore', 'mystery', 'news', 'religion', 'reviews', 'romance',
# 'science_fiction']

# fileids参数和categories参数不能同时指定
# brown.words(categories='news')
# ['The', 'Fulton', 'County', 'Grand', 'Jury', 'said', ...]
# brown.words(fileids=['cg22'])
# ['Does', 'our', 'society', 'have', 'a', 'runaway', ',', ...]
# brown.sents(categories=['news', 'editorial', 'reviews'])
# [['The', 'Fulton', 'County'...], ['The', 'jury', 'further'...], ...]

# from nltk.corpus import brown
# news_text = brown.words(categories='news')
# fdist = nltk.FreqDist([w.lower() for w in news_text])
# fdist
# FreqDist({u'the': 6386, u',': 5188, u'.': 4030, u'of': 2861, u'and': 2186, u'to': 2144, u'a': 2130, u'in': 2020, u'for': 969, u'that': 829, ...})
# modals = ['can', 'could', 'may', 'might', 'must', 'will']
# for m in modals:
# ... print m + ':', fdist[m],
# ...
# can: 94 could: 87 may: 93 might: 38 must: 53 will: 389

# cfd = nltk.ConditionalFreqDist(
#     (genre, word)
#     for genre in brown.categories()
#     for word in brown.words(categories=genre))
# genres = ['news', 'religion', 'hobbies', 'science_fiction', 'romance', 'humor']
# modals = ['can', 'could', 'may', 'might', 'must', 'will']
# cfd.tabulate(conditions=genres, samples=modals)
#
# can could   may might  must  will
#            news    93    86    66    38    50   389
#        religion    82    59    78    12    54    71
#         hobbies   268    58   131    22    83   264
# science_fiction    16    49     4    12     8    16

# ===================================================================================
# 路透社语料库
# fileids()方法传入类别categories，输出该类别下的文档。
# categories方法传入文档的fileids，输出该文档属于或涉及的类别。
from nltk.corpus import reuters
reuters.fileids()
reuters.categories()
# 与布朗语料库不同，路透社语料库的类别是有互相重叠的，只是因为新闻报道往往涉及
# 多个主题。我们可以查找由一个或多个文档涵盖的主题，也可以查找包含在一个或多个类别
# 中的文档。为方便起见，语料库方法既接受单个的fileid 也接受fileids 列表作为参数。
# reuters.categories('training/9865')
# ['barley', 'corn', 'grain', 'wheat']
# reuters.categories(['training/9865', 'training/9880'])
# ['barley', 'corn', 'grain', 'money-fx', 'wheat']
# reuters.fileids('barley')
# ['test/15618', 'test/15649', 'test/15676', 'test/15728', 'test/15871', ...]
# reuters.fileids(['barley', 'corn'])
# ['test/14832', 'test/14858', 'test/15033', 'test/15043', 'test/15106',
# 'test/15287', 'test/15341', 'test/15618', 'test/15618', 'test/15648', ...]
# 类似的，我们可以以文档或类别为单位查找我们想要的词或句子。这些文本中最开始的
# 几个词是标题，按照惯例以大写字母存储。
# reuters.words('training/9865')[:14]
# ['FRENCH', 'FREE', 'MARKET', 'CEREAL', 'EXPORT', 'BIDS',
# 'DETAILED', 'French', 'operators', 'have', 'requested', 'licences', 'to', 'export']
# reuters.words(['training/9865', 'training/9880'])
# ['FRENCH', 'FREE', 'MARKET', 'CEREAL', 'EXPORT', ...]
# reuters.words(categories='barley')
# ['FRENCH', 'FREE', 'MARKET', 'CEREAL', 'EXPORT', ...]
# reuters.words(categories=['barley', 'corn'])
# ['THAI', 'TRADE', 'DEFICIT', 'WIDENS', 'IN', 'FIRST', ...]

# ================================================================================
# 就职演说语料库
# 1.1 节中，我们看到了就职演说语料库，但是把它当作一个单独的文本对待。在图1-2
# 中使用的“词偏移”就像是一个坐标轴，它是语料库中词的索引数，从第一个演讲的第一个
# 词开始算起。然而，语料库实际上是55 个文本的集合，每个文本都是一个总统的演说。这
# 个集合的一个有趣特性是它的时间维度：
# import nltk
# from nltk.corpus import inaugural
# inaugural.fileids()
# ['1789-Washington.txt', '1793-Washington.txt', '1797-Adams.txt', ...]
# [fileid[:4] for fileid in inaugural.fileids()]
# ['1789', '1793', '1797', '1801', '1805', '1809', '1813', '1817', '1821', ...]

# 在2.2 节学习条件频率分布，现在只考虑输出，如图2-1 所示。
#  原文Pdf中有错，(target, file[:4])  改为 (target, fileid[:4])

# cfd = nltk.ConditionalFreqDist(
#     (target, fileid[:4])
#     for fileid in inaugural.fileids()
#     for w in inaugural.words(fileid)
#     for target in ['america', 'citizen']
#     if w.lower().startswith(target))
# cfd.plot()
# ==================================================
# 标注文本语料库
# ==========================

# NLTK 中定义的基本语料库函数：使用help(nltk.corpus.reader)可以找到更多的文档，
# 也可以阅读http://www.nltk.org/howto 上的在线语料库的HOWTO。

# fileids() 语料库中的文件
# fileids([categories]) 这些分类对应的语料库中的文件
# categories() 语料库中的分类
# categories([fileids]) 这些文件对应的语料库中的分类
# raw() 语料库的原始内容
# raw(fileids=[f1,f2,f3]) 指定文件的原始内容
# raw(categories=[c1,c2]) 指定分类的原始内容
# words() 整个语料库中的词汇
# words(fileids=[f1,f2,f3]) 指定文件中的词汇
# words(categories=[c1,c2]) 指定分类中的词汇
# sents() 指定分类中的句子
# sents(fileids=[f1,f2,f3]) 指定文件中的句子
# sents(categories=[c1,c2]) 指定分类中的句子
# abspath(fileid) 指定文件在磁盘上的位置
# encoding(fileid) 文件的编码（如果知道的话）
# open(fileid) 打开指定语料库文件的文件流
# root() 到本地安装的语料库根目录的路径
# ============================================================================
# 载入自己的语料库

# 如果你有自己收集的文本文件，并且想使用前面讨论的方法访问它们，你可以很容易地
# 在NLTK 中的PlaintextCorpusReader 帮助下载入它们。检查你的文件在文件系统中的位
# 置；在下面的例子中，我们假定你的文件在/usr/share/dict 目录下。不管是什么位置，将变量
# corpus_root􀁣的值设置为这个目录。PlaintextCorpusReader 初始化函数􀁤的第二个参
# 数可以是一个如['a.txt', 'test/b.txt']这样的fileids 链表，或者一个匹配所有fileids 的模式，
# 如：'[abc]/.*\.txt'（关于正则表达式的信息见3.4 节）。
# >>> from nltk.corpus import PlaintextCorpusReader
# >>> corpus_root = '/usr/share/dict' 􀁣
# >>> wordlists = PlaintextCorpusReader(corpus_root, '.*') 􀁤
# >>> wordlists.fileids()
# ['README', 'connectives', 'propernames', 'web2', 'web2a', 'words']
# >>> wordlists.words('connectives')
# ['the', 'of', 'and', 'to', 'a', 'in', 'that', 'is', ...]

# from nltk.corpus import PlaintextCorpusReader
# corpus_root = 'E:\\PycharmProjects\\data_etl\\data\\test'
# wordlists = PlaintextCorpusReader(corpus_root, '[a-z]')
# wordlists.fileids()
# wordlists.words('connectives')
# ====================================================================================================
# 条件频率分布，绘制分布图和分布表
# import nltk
# from nltk.corpus import brown
# u'of': 2849, u'and': 2146, u'to': 2116, u'a': 1993, u'in': 1893, u'for': 943, u'The': 806
# ['of','and','to','a','in','for','The']

# cfd = nltk.ConditionalFreqDist(
#     (genre, word)
#     for genre in brown.categories()
#     for word in brown.words(categories=genre))

# cfd.plot()
# 选择部分条件和文本,进行画图（plot）或打印（tabulate）。
# cfd.plot(conditions=['news'],samples=['of','and','to','a','in','for','The'])
# cfd.tabulate(conditions=['news'],samples=['of','and','to','a','in','for','The'])
#        of  and   to    a   in  for  The
# news 2849 2146 2116 1993 1893  943  806
# genre_word = [(genre, word)
#     for genre in ['news', 'romance']
#     for word in brown.words(categories=genre)]
# len(genre_word)

# 因此，在下面的代码中我们可以看到：链表genre_word 的前几个配对将是('news',
# word)的形式，而最后几个配对将是('romance', word)的形式。
# genre_word[:4]
# [('news', u'The'), ('news', u'Fulton'), ('news', u'County'), ('news', u'Grand')]
# genre_word[-4:]
# [('romance', u'afraid'), ('romance', u'not'), ('romance', u"''"), ('romance', u'.')]
# genre_word[-170576:4]
# [('news', u'The'), ('news', u'Fulton'), ('news', u'County'), ('news', u'Grand')]
# genre_word[-170576:-170572]
# [('news', u'The'), ('news', u'Fulton'), ('news', u'County'), ('news', u'Grand')]

# 现在，我们可以使用此配对链表创建一个ConditionalFreqDist，并将它保存在一个变
# 量cfd 中。像往常一样，我们可以输入变量的名称来检查它，并确认它有两个条件：
# cfd = nltk.ConditionalFreqDist(genre_word)
# cfd
# <ConditionalFreqDist with 2 conditions>
# cfd.conditions()
# ['news', 'romance']
# 让我们访问这两个条件，它们每一个都只是一个频率分布：
# cfd['news']
# <FreqDist with 100554 outcomes>
# cfd['romance']
# <FreqDist with 70022 outcomes>
# list(cfd['romance'])
# [',', '.', 'the', 'and', 'to', 'a', 'of', '``', "''", 'was', 'I', 'in', 'he', 'had',
# '?', 'her', 'that', 'it', 'his', 'she', 'with', 'you', 'for', 'at', 'He', 'on', 'him',
# 'said', '!', '--', 'be', 'as', ';', 'have', 'but', 'not', 'would', 'She', 'The', ...]
# cfd['romance']['could']
# 193

# import nltk
# from nltk.corpus import udhr
# languages = ['Chickasaw', 'English', 'German_Deutsch',
#     'Greenlandic_Inuktikut', 'Hungarian_Magyar', 'Ibibio_Efik']
# cfd = nltk.ConditionalFreqDist(
#     (lang, len(word))
#     for lang in languages
#     for word in udhr.words(lang + '-Latin1'))
#
# cfd.tabulate(conditions=['English', 'German_Deutsch'],samples = range(10), cumulative = True)
#                   0    1    2    3    4    5    6    7    8    9
#        English    0  185  525  883  997 1166 1283 1440 1558 1638
# German_Deutsch    0  171  263  614  717  894 1013 1110 1213 1275
# ==================================================================================
# 使用双连词生成随机文本
# def generate_model(cfdist, word, num=15):
#     for i in range(num):
#         print word,       #逐个替换并打印每个word的后接频率最大的单词
#         word = cfdist[word].max()
#
# text = nltk.corpus.genesis.words('english-kjv.txt')
# bigrams = nltk.bigrams(text)
# cfd = nltk.ConditionalFreqDist(bigrams)
#
# import nltk
# text = nltk.corpus.genesis.words('english-kjv.txt')
# bigrams = nltk.bigrams(text)
# cfd = nltk.ConditionalFreqDist(bigrams)
# print cfd['living']
# <FreqDist with 6 samples and 16 outcomes>
# generate_model(cfd,'living')
# living creature that he said , and the land of the land of the land
# ============================================================
# NLTK 中的条件频率分布：定义、访问和可视化一个计数的条件频率分布的常用函数：
# cfdist= ConditionalFreqDist(pairs) 从配对链表中创建条件频率分布
# cfdist.conditions() 将条件按字母排序
# cfdist[condition] 此条件下的频率分布
# cfdist[condition][sample] 此条件下给定样本的频率
# cfdist.tabulate() 为条件频率分布制表
# cfdist.tabulate(samples, conditions) 指定样本和条件限制下制表
# cfdist.plot() 为条件频率分布绘图
# cfdist.plot(samples, conditions) 指定样本和条件限制下绘图
# cfdist1 < cfdist2 测试样本在cfdist1 中出现次数是否小于在cfdist2 中出现次数
# =============================================
# 导入其他模块的代码

# 在一个文件中的变量和函数定义的集合被称为一个Python 模块（module）。相关模块的集合称为一个包（package）

# from code.py_test import *
#
# plural("family")

# =====================================
# 另一个词汇列表是名字语料库，包括8000 个按性别分类的名字。男性和女性的名字存
# 储在单独的文件中。让我们找出同时出现在两个文件中的名字即性别暧昧的名字：
# 统计男、女性名字中，最后一个字符的频率分布图：
# import nltk
# names = nltk.corpus.names
# names.fileids()
# # ['female.txt', 'male.txt']
# male_names = names.words('male.txt')
# female_names = names.words('female.txt')
# [w for w in male_names if w in female_names]
# ['Abbey', 'Abbie', 'Abby', 'Addie', 'Adrian', 'Adrien', 'Ajay', 'Alex', 'Alexis',
# 'Alfie', 'Ali', 'Alix', 'Allie', 'Allyn', 'Andie', 'Andrea', 'Andy', 'Angel',
# 'Angie', 'Ariel', 'Ashley', 'Aubrey', 'Augustine', 'Austin', 'Averil', ...]
#
#
# cfd = nltk.ConditionalFreqDist(
#     (fileid, name[-1])
#     for fileid in names.fileids()
#     for name in names.words(fileid))
# cfd.plot()

# 由图显示男性和女性名字的结尾字母；大多数以a，e 或i 结尾的名字是女性；以h 和l 结尾的男性和女性同样多；以k，o，r，s 和t 结尾的更可能是男性。