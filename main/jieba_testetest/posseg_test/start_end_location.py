# encoding=utf-8
import jieba

if __name__ == '__main__':

    # result = jieba.tokenize(u'永和服装饰品有限公司')     #默认模式
    result = jieba.tokenize(u'永和服装饰品有限公司',mode='search')      #搜索模式
    # result = jieba.tokenize(u'永和服装饰品有限公司')
    for tk in result:
        print("word %s\t\t\t start: %d \t\t end:%d" % (tk[0],tk[1],tk[2]))

    jieba.set_dictionary