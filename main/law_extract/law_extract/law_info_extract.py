# -*- coding: utf-8 -*-

import pandas as  pd
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import time
from pyltp import Segmentor
from pyltp import Postagger
from pyltp import NamedEntityRecognizer
import re
from collections import Counter

segmentor = Segmentor()  # 初始化实例
segmentor.load('/home/sherlock/Documents/ltp_data/cws.model')
#实例化词性工具
# postagger = Postagger() # 初始化实例
# postagger.load('/home/sherlock/Documents/ltp_data/pos.model')  # 加载模型
# recognizer = NamedEntityRecognizer()
# recognizer.load('/home/sherlock/Documents/ltp_data/ner.model')

def wdseg(inputstr,ret_type):


    words = segmentor.segment(inputstr)  # 分词
    if ret_type == 'str':
        seg_word = ' '.join(words)
    if ret_type == 'lst':
        seg_word = ' '.join(words)
        seg_word = seg_word.split()

    #segmentor.release()  # 释放模型
    return seg_word

def deleCnbiaodian(line):
    #替换中文标点
    line = line.decode('utf8')
    string = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+".decode("utf8"), "".decode("utf8"),line)
    #regex = re.compile(ur"[，, 。、；！：（）“”《》？_]")
    return string



nation = u'汉族、蒙古族、回族、藏族、维吾尔族、苗族、彝族、壮族、布依族、朝鲜族、满族、侗族、瑶族、白族、土家族、哈尼族、哈萨克族、傣族、黎族、僳僳族、佤族、畲族、高山族、拉祜族、水族、东乡族、纳西族、景颇族、柯尔克孜族、土族、达斡尔族、仫佬族、羌族、布朗族、撒拉族、毛南族、仡佬族、锡伯族、阿昌族、普米族、塔吉克族、怒族、乌孜别克族、俄罗斯族、鄂温克族、德昂族、保安族、裕固族、京族、塔塔尔族、独龙族、鄂伦春族、赫哲族、门巴族、珞巴族、基诺族'
nation_list = nation.split('、')

agenda_list = [u'男',u'女']
xueli_list = [u'文盲',u'小学',u'中学',u'初中',u'高中',u'大学',u'本科',u'硕士',u'研究生',u'博士',u'博士后']

#多人犯罪的性别
def get_gender_edu_nation(t_item_list,info_seg_lislt):
#This function could match gender,edu,nation in the orging party_info
    for ii  in info_seg_lislt:
        ii = ii.decode('utf8')
        if ii in t_item_list:
            return ii


def get_birth(info_seg_list):
    for i in info_seg_list:
        if '被告' in i:

            dft_idx = int(info_seg_list.index(i))
            print '***' + i +str(info_seg_list.index(i))
        if '年' in i:
            yr_idx = int(info_seg_list.index(i))
        if '生' in i:
            born_str = int(info_seg_list.index(i))
            try:
                if yr_idx - dft_idx <10 or born_str - yr_idx <5:
                    birth = ''
                    for bt_i in  range(yr_idx,yr_idx+3):
                        bt = info_seg_list[bt_i]
                        birth = birth + bt

                    print birth
                    return birth
            except:
                pass


def judge_suspect_number(info_seg_list):

    seg_word_count = Counter(info_seg_list)
    suspect_number = seg_word_count['被告人']
    suspect_number2 = seg_word_count['被告']
    if suspect_number>0:
        return suspect_number
    elif suspect_number2 >0:
        return suspect_number2





law_path = '/media/sherlock/new30/law/jun28InfoExtractor/tb_doc.csv'
law_df = pd.read_csv(law_path)

for i in range(len(law_df)):
    info_words = wdseg((law_df.loc[i,'party_info']).encode('utf8'),'lst')
    law_df.loc[i,'gender'] = get_gender_edu_nation(agenda_list, info_words)
    law_df.loc[i,'edu'] = get_gender_edu_nation(xueli_list, info_words)
    law_df.loc[i,'nation'] = get_gender_edu_nation(nation_list, info_words)
    law_df.loc[i,'birth'] = get_birth(info_words)
    law_df.loc[i,'suspect_num'] = judge_suspect_number(info_words)
    print i

law_df.to_csv('/media/sherlock/new30/law/jun28InfoExtractor/tb_doc_add3.csv',header=True,index=False,encoding='utf8')
