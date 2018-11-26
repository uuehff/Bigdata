# -*- coding: utf-8 -*-
import re

# ["《中华人民共和国刑法》第一百三十三条", "《中华人民共和国刑法》第五十二条"]
#p1 = ur'^[\w,.:;!，。：；！]?$'
# p1 = ur'^[\d,.:;!、，。：；！？?_]*[a-zA-Z]?[\d,.:;!、，。：；！？?_]*$'
#过滤掉类似：，,.。和 a12,.、和 ？1 ，a 等
# pattern1 = re.compile(p1)



# p1 = ur'^[\d,.:;!、，。：；！？?_]*[a-zA-Z]?[\d,.:;!、，。：；！？?_]*$'
# [\u4e00,\u4e8c,\u4e09,\u56db,\u4e94,\u516d,\u4e03,\u516b,\u4e5d,\u5341
# p1 = ur'\u7b2c[\u4e00\u4e8c\u4e09\u56db\u4e94\u516d\u4e03\u516b\u4e5d\u5341\u767e\u5343]{1,10}\u6761'
p1 = ur'[\u4e00-\u9fa5]{1,100}事务所'
# 第[一二三四五六七八九十百千]{1,10}条
# p1 = ur'\u7b2c[\u4e00\u4e8c\u4e09\u56db\u4e94\u516d\u4e03\u516b\u4e5d\u5341\u767e\u5343]{1,10}\u6761'  search,pattern1.group(0)
# p2 = ur'[\u300a\u300b]'
p2 = ur"："
# [\u4e00-\u9fa5]
# ^[\u4E00-\u9FFF]+$
# \u300a - \u300b   ==>  《 - 》
q = ["qwe1234ddd", "bbccxxzz123mmnnn"]
# q2 = ["《中华人民共和国刑法》第一百三十三条", "《中华人民共和国刑法》第五十二条"]
q2 = ["《中华人民共和国刑法》第三百四十七条第一款、第四款", "《中华人民共和国刑法》第六十五条第一款", "《中华人民共和国刑法》第六十七条第三款", "《中华人民共和国刑法》第五十三条"]
# pattern1 = re.findall(p1,q2[0].decode("utf-8"))
# pattern1 = re.search(p1,q2[0].decode("utf-8"))
s = u"1996-04-18开始首次执业2002-05-21市内转所：广东立国律师事务所2004-08-18市内转所：广东正大元律师事务所2005-04-28市内转所：广东劳维律师事务所2007-07-18市内转所：广东卓建律师事务所2009-08-05市内转所：广东立国律师事务所2012-08-15市内转所：广东赵卢律师事务所2013-08-05跨市转所：广东创晖律师事务所"

pattern1 = re.split(p2,s)
for i in pattern1:
    pattern2 = re.search(p1, i)
    if pattern2:
        print pattern2.group(0)
# for i in q2:
#
#     pattern1 = re.split(p2,i.decode("utf-8"))
#     pattern2 = re.search(p1, pattern1[2])
#     print pattern1[1],pattern2.group(0)