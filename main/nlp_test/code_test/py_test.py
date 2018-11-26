# -*- coding: utf-8 -*-

# 这个函数试图生成任何英语名词的复数形式。例如:如果这个词以y 结尾，删除它们并添加ies。

def plural(word):
    if word.endswith('y'):
        return word[:-1] + 'ies'
    elif word[-1] in 'sx' or word[-2:] in ['sh', 'ch']:
        return word + 'es'
    elif word.endswith('an'):
        return word[:-2] + 'en'
    else:
        return word + 's'

# >>> plural('fairy')
# 'fairies'
# >>> plural('woman')
# 'women'
