# -*- coding: utf8 -*-
import re
import xlrd
import pandas
import datetime

CN_NUM = {
    u'〇' : 0,
    u'１': 1,
    u'-': 1,
    u'一' : 1,
    u'二' : 2,
    u'三' : 3,
    u'四' : 4,
    u'五' : 5,
    u'六' : 6,
    u'七' : 7,
    u'八' : 8,
    u'九' : 9,

    u'零' : 0,
    u'壹' : 1,
    u'贰' : 2,
    u'叁' : 3,
    u'参' : 3,
    u'肆' : 4,
    u'伍' : 5,
    u'陆' : 6,
    u'柒' : 7,
    u'捌' : 8,
    u'玖' : 9,

    u'貮' : 2,
    u'两' : 2
    }
CN_UNIT = {
    u'十' : 10,
    u'拾' : 10,
    u'百' : 100,
    u'佰' : 100,
    u'千' : 1000,
    u'干' : 1000,
    u'仟' : 1000,
    u'仠' : 1000,
    u'万' : 10000,
    u'萬' : 10000,
    u'亿' : 100000000,
    u'億' : 100000000,
    u'兆' : 1000000000000,
    u'年' : 12,
    u'月' : 1,
    }

def as_text(v):
    if v is None:
        return None
    elif isinstance(v, unicode):
        return v
    elif isinstance(v, str):
        return v.decode('utf-8', errors='ignore')
    else:
        raise ValueError('Invalid type %r' % type(v))

def string_to_digit(money_string):
    if money_string.isdigit() or money_string.count(u'.') == 1:
        return float(money_string)
    elif money_string.count(u'.') == 2:
        return float(money_string.split(u'.')[0])
    else:
        return float(CN_NUM[money_string])

def deal_money(money_string):
    punish_money = None
    money_pattern = re.compile(u'[\d|一二三四五六七八九十|.]+')
    million_money_amount, thousand_money_amount, hundred_money_amount, billion_money_amount = '0', '0', '0', '0'
    if len(money_string) > 0:
        if u'亿' in money_string or u'万' in money_string or u'千' in money_string or u'百' in money_string:
            hundred_money_split = money_string.split(u'百')
            if len(hundred_money_split) > 1:
                money_result = re.findall(money_pattern, hundred_money_split[0])
                hundred_money_amount = money_result[-1]
            money_string = hundred_money_split[0]
            thousand_money_split = money_string.split(u'千')
            if len(thousand_money_split) > 1:
                money_result = re.findall(money_pattern, thousand_money_split[0])
                thousand_money_amount = money_result[-1]
            money_string = thousand_money_split[0]
            million_money_split = money_string.split(u'万')
            if len(million_money_split) > 1:
                money_result = re.findall(money_pattern, million_money_split[0])
                million_money_amount = money_result[-1]
            money_string = million_money_split[0]
            billion_money_split = money_string.split(u'亿')
            if len(billion_money_split) > 1:
                money_result = re.findall(money_pattern, billion_money_split[0])
                billion_money_amount = money_result[-1]
            punish_money = (
                        string_to_digit(billion_money_amount) * 10**8 + \
                        string_to_digit(million_money_amount) * 10000  + \
                        string_to_digit(thousand_money_amount) * 1000  + \
                        string_to_digit(hundred_money_amount) * 100
                    )
            punish_money = string_to_digit(billion_money_amount) * 100000000 + string_to_digit(million_money_amount)  * 10000 + string_to_digit(thousand_money_amount) * 1000  + string_to_digit(hundred_money_amount)  * 100
        else:
            punish_money = (string_to_digit(money_string))
    else:
        punish_money = 0
    return int(punish_money)
def cn2dig(cn):
    lcn = list(cn)
    unit = 0 #当前的单位
    ldig = []#临时数组
    other = []
    while lcn:
        cndig = lcn.pop()
        if CN_UNIT.has_key(cndig):
            unit = CN_UNIT.get(cndig)
            if unit==10000:
                ldig.append('w')    #标示万位
                unit = 1
            elif unit==100000000:
                ldig.append('y')    #标示亿位
                unit = 1
            elif unit==1000000000000:#标示兆位
                ldig.append('z')
                unit = 1
            elif unit==12:
                ldig.append('n')
                unit =1
            continue
        elif CN_NUM.has_key(cndig):
            dig = CN_NUM.get(cndig)
            if unit:
                dig = dig*unit
                unit = 0
            ldig.append(dig)
        else:
            other.append(cndig)
    if unit==10:    #处理10-19的数字
        ldig.append(10)
    #print ldig #uncomment this line to watch the middle var.
    ret = 0
    tmp = 0
    while ldig:
        x = ldig.pop()
        if x=='w':
            tmp *= 10000
            ret += tmp
            tmp=0
        elif x=='y':
            tmp *= 100000000
            ret += tmp
            tmp=0
        elif x=='z':
            tmp *= 1000000000000
            ret += tmp
            tmp=0
        elif x=='n':
            tmp *= 12
            ret += tmp
            tmp=0
        else:
            tmp += x
    ret += tmp
    return ret

def as_money(money_string):
    strip_money_words = [u'计', u'人民币', u'；', u'、72', u'是', u'（已交纳', u'并处', u'并处金人民币',u'并处罚人民币', u'并处罚金', u'金额为', u'罚金', u'金',
                         u'以', u'份', u'（已缴纳一万', u'在', u'位', u'。', u'、00', u'﹒00',u'额', u'×', u'帀', u'某', u'处', u'同', u'大', u'（已缴纳四万',
                         u'?', u'无', u'（￥1000.00）', u'（￥4000.00）', u'（￥2000.00）',u'斌', u'民币', u'+', u'为', u'＊', u'。被告人张', u'元', u'已缴纳',
                         u'.00', u',', u' ', u'　', u'元', u'点', u'余', u'多', u'零', u'，', u'（人民币）', u'＋', u'人民', u'人', u'币', u'￥', u'）', u'（']
    for sw in strip_money_words:
        money_string = as_text(as_text(money_string).replace(sw,''))
    try:
        # money_string = deal_money(money_string)
        if money_string.isdigit():
            money_string = deal_money(money_string)
        elif re.search(r'\d',money_string) and re.search(u'[\u4e00-\u9fa5]',money_string):
            money_string = deal_money(money_string)
        elif re.search(r'\d', money_string) and re.search(u'\.', money_string):
            money_string = deal_money(money_string)
        elif u'《' in money_string:
            money_string = ''
        else:

            money_string = cn2dig(money_string)
    except KeyError:
        money_string = 0
    except IndexError:
        money_string = 0
    except UnicodeEncodeError:
        money_string = 0
    if money_string in [u'0', 0]:
        date_result = u''
    return str(money_string)

class AttrDict(dict):
    """Dict that can get attribute by dot"""
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self
# 有期徒刑期
def as_date_date(date_string):
    date_result = 0
    date_string = as_text(date_string)
    strip_date_words = [u'缓刑一年六个月', u'缓刑一年', u'缓刑二年', u'缓刑三年', u'缓刑四年', u'缓刑五年', u'期限', u'余刑', u'的', u'剩期', u'刑罚', u'刑期', u'仍须执行',
                        u'余期', u'有期徒刑', u'考验期为', u'考验', u'期', u'拘役', u'徒刑', u'个月',
                        u'徒',  u'均', u'是', u'缓',u'刑',u'零']
    for sw in strip_date_words:
        if date_string.count(u'个') > 1:
            date_string = date_string.strip(u'个')
        date_string = as_text(date_string.replace(sw,''))
    try:
        date_result = cn2dig(date_string)
    except UnicodeEncodeError:
        date_result = 0
    except IndexError:
        date_result = 0
    if date_result in [u'0', 0]:
        date_result = u''
    return date_result
# 缓刑
def as_date_delay(date_string):
    date_result = 0
    date_string = as_text(date_string)
    strip_date_words = [u'缓刑', u'期限', u'余刑', u'的', u'剩期', u'刑罚', u'刑期', u'仍须执行',
                        u'余期', u'有期徒刑', u'考验期为', u'考验', u'期', u'拘役', u'徒刑', u'个月',u'个',
                        u'徒',  u'均', u'是', u'缓', u'刑',u'零']
    for sw in strip_date_words:
        if date_string.count(u'个') > 1:
            date_string = date_string.strip(u'个')
        date_string = as_text(date_string.replace(sw,''))
    try:
        date_result = cn2dig(date_string)
    except UnicodeEncodeError:
        date_result = 0
    except IndexError:
        date_result = 0
    if date_result in [u'0', 0]:
        date_result = u''
    return date_result

sentence_delimiters = ['?', '!', ';', '？', '！', '。', '；', '……', '…', '\n']
def sentence_segment(text):
    res = [as_text(text)]
    delimiters = set([as_text(item) for item in sentence_delimiters])
    for sep in delimiters:
        text, res = res, []
        for seq in text:
            res += seq.split(sep)
    res = [s.strip() for s in res if len(s.strip()) > 0]
    return res

def chinese_to_digits(uchars_chinese):
    common_used_numerals ={u'零':0, u'一':1, u'二':2, u'三':3, u'四':4, u'五':5, u'六':6, u'七':7,
                           u'八':8, u'九':9, u'十':10, u'百':100, u'千':1000, u'万':10000, u'亿':100000000}
    if uchars_chinese[0] in [u'十', u'百', u'千', u'万', u'亿']:
        uchars_chinese = u'一' + uchars_chinese
    total = 0
    r = 1
    for i in range(len(uchars_chinese) - 1, -1, -1):
        x = common_used_numerals.get(uchars_chinese[i], 0)
        if x >= 10:
            if x > r:
                r = x
            else:
                r = r * x
        else:
            total += r * x
    return total

def read_location_xcel(excel_path):
    data = xlrd.open_workbook(excel_path)
    table = data.sheet_by_name("sheet")
    result_list = []
    for i in range(1,table.nrows):
        row_content = table.row_values(i, 0, table.ncols)
        result_list.append(row_content)
    return result_list

date_pattern = re.compile(u'[\d|一二三四五六七八九十|.]+')
def judge_bad_date(date_string):
    if date_string and not date_string[0] == ' ':
        day_judge, month_judge, year_judge = False, False, False
        if type(date_string) is str:
            date_string = unicode(date_string)
        date_result = re.findall(date_pattern, date_string)
        day   = date_result[-1]
        month = date_result[1]
        year  = date_result[0]
        date_string = '%s-%s-%s'%(str(year), str(month), str(day))
        try:
            date_format = datetime.datetime.strptime(date_string, '%Y-%m-%d').date()
            now_date = datetime.datetime.now().date()
            if (now_date - date_format).days < 0:
                date_string = ''
        except ValueError:
            date_string = ''
#         if int(day) in range(1,32):
#             day_judge = True
#         if int(month) in range(1,13):
#             month_judge = True
#         if int(year) in range(1900,2200):
#             year_judge = True
#         if day_judge and month_judge and year_judge:
#             date_string = '%s-%s-%s'%(year, month, day)
#         else:
#             date_string = ''
    else:
        date_string = ''
    return date_string

def digit_to_chinese(num):
    result = []
    chiNum=['零','一','二','三','四','五','六','七','八','九']
    chiSerie=['零','十','百','千']
    try:
        num=int(num)
    except ValueError:
        pass
    else:
        zeroFlag=0
        flag=0
        if num==0:
            result.append(chiNum[0])
        elif num>9999 or num<0:
            pass
        else:
            for i in range(4):
                level=num/pow(10,3-i)
                if level==0 and flag==1:
                    zeroFlag=1
                elif level!=0:
                    flag=1
                    num=num%pow(10,3-i)
                    if zeroFlag==1:
                        result.append(chiNum[0])
                    result.append(chiNum[level])
                    if i!=3:
                        result.append(chiSerie[3-i])
                    zeroFlag=0
    return as_text(''.join(result))

