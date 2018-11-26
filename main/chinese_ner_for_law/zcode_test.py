# -*- coding: utf-8 -*-

import re
import labelApi

content = u"没  满   十六  16  周岁  抢劫  学生   七八  78  次  没用  过  凶器  属于  从犯  这种  情况  要  判   几年"

print labelApi.get_X(content)

# t = ['O', 'O', 'B-TIME', 'I-TIME', 'I-TIME', 'I-TIME', 'I-TIME', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O']
#
#
# wl =  re.split("[ ]{1,100}", content)
# tt = []
# start = 0
# end = 0
# for i in wl:
#     end += len(i)
#     tt.append(t[start:end])
#     start += len(i)
# tt2 = []
# for i in range(len(tt)):
#     flag = False
#     for j in tt[i] :
#         if j.startswith('B'):
#             flag = True
#             tt2.append("".join(wl[i]) + "|" + j.split("-")[1])
#             break
#     if not flag:
#         for j in tt[i]:
#             if j.startswith('I'):
#                 flag = True
#                 tt2.append("".join(wl[i]) + "|" + j.split("-")[1])
#                 break
#     if not flag:
#         tt2.append("".join(wl[i]) )
#
# print "   ".join(tt2)
