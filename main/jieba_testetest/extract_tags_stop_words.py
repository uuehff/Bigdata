# encoding=utf-8
import sys
import jieba
import jieba.analyse
from optparse import OptionParser

# USAGE = "usage:    python extract_tags_stop_words.py [file name] -k [top k]"
#
# parser = OptionParser(USAGE)
# parser.add_option("-k", dest="topK")
# opt, args = parser.parse_args()
#
#
# if len(args) < 1:
#     print(USAGE)
#     sys.exit(1)
#
# file_name = args[0]
#
# if opt.topK is None:
#     topK = 10
# else:
#     topK = int(opt.topK)

# content = open(file_name, 'rb').read()
content = open("E:\\PycharmProjects\\data_etl\\main\\jieba_testetest\\water.txt", 'rb').read()

jieba.analyse.set_stop_words("E:\\PycharmProjects\\data_etl\\main\\jieba_testetest\\stop_words.txt")
jieba.analyse.set_idf_path("E:\\PycharmProjects\\data_etl\\main\\jieba_testetest\\idf.txt.big");

# textrank  进行关键词抽取
tags2 = jieba.analyse.textrank(content, topK=10, withWeight=True, allowPOS=('ns', 'n', 'vn', 'v'))

# tags2 = jieba.analyse.extract_tags(content, topK=10, withWeight=True) #withWeight=True返回权重值


for i in tags2:
    print i[0],i[1]