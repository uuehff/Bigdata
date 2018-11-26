#encoding=utf-8

import jieba.posseg as pseg


if __name__ == '__main__':
    words = pseg.cut("我爱北京天安门")
    for word, flag in words:
        print('%s %s' % (word, flag))

