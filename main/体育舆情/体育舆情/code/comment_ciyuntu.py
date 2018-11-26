# encoding:utf-8
import happybase
import json
import jieba
import matplotlib.pyplot as plt
from wordcloud import WordCloud
def stopWord(stopword_file):
    stopwords = []
    for word in open(stopword_file, 'r'):
        stopwords.append(word.strip())
    return stopwords

def fre_word(data,stopwords):
    text = ""
    for line in data:
        text += line.encode("GB18030") + ";"
    words = jieba.cut(text, cut_all=False)
    ww = [w for w in words if w.encode('utf-8') not in stopwords]
    # for w in ww:
    #     print w
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
    # dict111={}
    # for i in freq_word:
        # dict111[i[0]]=i[1]
        # print i[0],i[1]
    # print json.dumps(dict111)

    return freq_word

# 画词云图
def word_cloud(freq_word):
    wc = WordCloud(font_path='D:\Anaconda2\Lib\site-packages\matplotlib\mpl-data\fonts\ttf\simhei.ttf',
                   max_font_size=100, random_state=30).fit_words(freq_word[:100])
    # wordcloud = WordCloud( max_font_size = 50,            # 设置字体最大值
    #             random_state = 30,            # 设置有多少种随机生成状态，即有多少种配色方案
    #             ).fit_words(freq_word[:100])
    plt.imshow(wc)
    plt.axis("off")
    plt.show()

# 读取新闻评论
def new_comment(table):
    xinwen_comment = []
    for k,v in table.scan(row_prefix='嫘祖杯01',columns=['d:comment_list']):
        # print k.decode('utf-8'),v['d:comment_list']
        data = json.loads(v['d:comment_list'])
        for i in data:
            xinwen_comment.append(i['content'])
            # print i['content'].encode("GB18030")
    xinwen_comment = list(set(xinwen_comment))
    # for i in xinwen_comment:
    #     print i.encode("GB18030")
    return xinwen_comment

# 读取微博评论
def weibo_comment(table):
    weibo_comment = []
    for k,v in table.scan(row_prefix="嫘祖杯02",columns=["d:comment"]):
        for k2 in v.values():
            if k2:
                s = k2.decode("utf-8")
                s3 = json.loads(s)
                for j in s3.values():
                    # print type(j)
                    j2 = json.loads(j)
                    if u'[热门]' not in j2["pinglun_content"]:
                        # print j2["pinglun_content"]
                        if u'回复' in j2["pinglun_content"]:
                            comment = j2["pinglun_content"].split(':')[-1]
                            # print comment
                            weibo_comment.append(comment)
                        else:
                            weibo_comment.append(j2["pinglun_content"])
    weibo_comment = list(set(weibo_comment))
    # for i in weibo_comment:
    #     print i
    return weibo_comment
if __name__ == '__main__':
    conn = happybase.Connection('192.168.10.24', timeout=300000)
    table = conn.table('public_sentiment')

    # for i in new_comment:
    #     print i.encode('GB18030')
    stopword_file = '../data/stopword.txt'
    stopwords = stopWord(stopword_file)
    # freq_word = fre_word(new_comment, stopwords)
    # word_cloud(freq_word)

    weibo_comment = weibo_comment(table)
    weibo_freq_word = fre_word(weibo_comment, stopwords)
    weibo_comment_dict = {}
    xinwen_comment = new_comment(table)
    xinwen_freq_word = fre_word(xinwen_comment, stopwords)
    xinwen_comment_dict = {}
    for i in weibo_freq_word[:201]:
        if i[0]:
            weibo_comment_dict[i[0]] = i[1]
    print json.dumps(weibo_comment_dict)
    # word_cloud(weibo_freq_word)