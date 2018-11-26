# encoding:utf-8
import MySQLdb
import multiprocessing

area={u'北京':u'北京市',u'重庆':u'重庆市',u'上海':u'上海市',u'天津':u'天津市',u'潼南县':u'重庆市',
    u'威宁':u'贵州省',u'六盘水':u'贵州省',u'凤岗县':u'贵州省',u'平坝县':u'贵州省',u'贵阳':u'贵州省',
    u'大连':u'辽宁省',u'沈阳':u'辽宁省',u'锦州':u'辽宁省',u'丹东':u'辽宁省',u'德州':u'山东省',u'滨州':u'山东省',u'青岛':u'山东省',u'济宁':u'山东省',
    u'烟台':u'山东省',u'临沂':u'山东省',u'威海':u'山东省',u'日照':u'山东省',u'菏泽':u'山东省',u'泰安':u'山东省',u'潍坊':u'山东省',u'济南':u'山东省',
    u'红石林区':u'湖南省',u'大通湖':u'湖南省',u'屈原管理区':u'湖南省',u'长沙':u'湖南省',u'洪江':u'湖南省',u'ＸＸ瑶族自治县':u'湖南省',u'衡阳':u'湖南省',u'怀化':u'湖南省',
    u'荆州市':u'湖北省',u'武汉':u'湖北省',u'芜湖':u'湖北省',u'宜昌':u'湖北省',u'葛洲坝':u'湖北省',u'襄阳':u'湖北省',u'沙洋':u'湖北省',
    u'福州':u'福建省',u'铜陵市':u'安徽省',u'合肥':u'安徽省',u'杭州':u'浙江省',u'洞头县':u'浙江省',
    u'泰州':u'江苏省',u'扬州':u'江苏省',u'苏州':u'江苏省',u'南京':u'江苏省',u'淮安':u'江苏省',u'南通':u'江苏省',u'常州市':u'江苏省',
    u'积石山保安族':u'甘肃省',u'兰州':u'甘肃省',u'庆阳林区':u'甘肃省',u'武威':u'甘肃省',u'卓尼林区':u'甘肃省',u'迭部林区':u'甘肃省',u'舟曲林区':u'甘肃省',u'甘肃':u'甘肃省',
    u'白石山林区':u'吉林省',u'图们':u'吉林省',u'长春':u'吉林省',u'和龙林区':u'吉林省',u'敦化林区':u'吉林省',u'汪清林区':u'吉林省',
    u'抚松林区':u'吉林省',u'珲春林区':u'吉林省',u'南昌':u'江西省',u'新建县':u'江西省',u'赣州':u'江西省',u'庐山':u'江西省',
    u'珠海':u'广东省',u'梅州市':u'广东省' ,u'从化市':u'广东省',u'湛江':u'广东省',u'增城市':u'广东省',u'高要市':u'广东省',u'广州':u'广东省',u'增城':u'广东省',
    u'九三农垦':u'黑龙江省',u'建三江农垦':u'黑龙江省',u'哈尔滨':u'黑龙江省',u'牡丹江':u'黑龙江省',u'铁力林区':u'黑龙江省',u'迎春林区':u'黑龙江省',
    u'通北林区':u'黑龙江省',u'绥化农垦':u'黑龙江省',u'方正林区':u'黑龙江省',u'双丰林区':u'黑龙江省',u'苇河林区':u'黑龙江省',u'齐齐哈尔':u'黑龙江省',
    u'红兴隆农垦':u'黑龙江省',u'兴隆林区':u'黑龙江省',u'东方红林区':u'黑龙江省',u'绥棱林区':u'黑龙江省',u'大庆':u'黑龙江省',u'东京城林区':u'黑龙江省',
    u'北安农垦':u'黑龙江省',u'大兴安岭':u'黑龙江省',u'穆棱林区':u'黑龙江省',u'佳木斯':u'黑龙江省',u'林口林区':u'黑龙江省',u'桃山林区':u'黑龙江省',
    u'绥阳林区':u'黑龙江省',u'大海林林区':u'黑龙江省',u'柴河林区':u'黑龙江省',u'鹤北林区':u'黑龙江省',u'海林林区':u'黑龙江省',u'宝泉岭':u'黑龙江省',
    u'双鸭山林区': u'黑龙江省', u'桦南林区': u'黑龙江省', u'图强林区': u'黑龙江省', u'亚布力林区':u'黑龙江省',u'阿木尔林区':u'黑龙江省',u'十八站林区':u'黑龙江省',
    u'沾河林区':u'黑龙江省',u'清河林区':u'黑龙江省',u'鹤立林区':u'黑龙江省', u'山河屯林区':u'黑龙江省', u'八面通林区': u'黑龙江省',u'朗乡林区':u'黑龙江省',
    u'金平苗族瑶族傣族':u'云南省',u'玉溪':u'云南省',u'元江哈尼族':u'云南省',u'曲靖':u'云南省',u'成都':u'四川省',
    u'临汾':u'山西省',u'太原':u'山西省',u'大同':u'山西省', u'郑州':u'河南省',u'洛阳':u'河南省',u'三门峡':u'河南省',u'陕州区':u'河南省',
    u'安康':u'陕西省',u'西安':u'陕西省',u'歧山县':u'陕西省', u'高陵县':u'陕西省',u'渭南市华州区':u'陕西省',
    u'石家庄':u'河北省',u'秦皇岛':u'河北省',u'邢台':u'河北省',u'保定':u'河北省',u'营口市':u'辽宁省', u'辽河人民法院': u'辽宁省',
    u'乃东区':u'西藏自治区',u'乌鲁木齐':u'新疆维吾尔自治区',u'新疆':u'新疆维吾尔自治区',u'靖西县':u'广西壮族自治区',u'柳州':u'广西壮族自治区',u'南宁':u'广西壮族自治区',
    u'冷湖矿区':u'青海省',u'茫崖矿区':u'青海省',u'西宁':u'青海省',u'大柴旦矿区':u'青海省',u'无锡':u'江苏省',u'常州':u'江苏省',u'徐州':u'江苏省',u'盐城':u'江苏省',u'镇江':u'江苏省',
    u'荣昌县':u'重庆市',u'彭山县':u'四川省',u'马尔康市':u'四川省',u'西昌':u'四川省',u'绵阳':u'四川省',
    u'腾冲县':u'云南省',u'镇沅彝族哈尼族拉祜族':u'云南省',u'孟连傣族拉祜族佤族':u'云南省',u'双江拉祜族佤族布朗族傣族':u'云南省',u'昆明':u'云南省',u'开远':u'云南省',
    u'香格里拉':u'云南省',u'土默特':u'内蒙古自治区',u'阿拉善':u'内蒙古自治区',u'旗':u'内蒙古自治区',u'包头':u'内蒙古自治区',u'呼和浩特':u'内蒙古自治区',
    u'库尔勒':u'新疆维吾尔自治区',u'哈密':u'新疆维吾尔自治区',u'北屯市':u'新疆维吾尔自治区',u'塔什库尔干塔吉克自治县':u'新疆维吾尔自治区',
    u'银川':u'宁夏回族自治区',u'吴忠市红寺堡开发区':u'宁夏回族自治区',u'武鸣县':u'广西壮族自治区',
    u'宁河县':u'河北省',u'抚宁县':u'河北省',u'清苑县':u'河北省',u'张家口':u'河北省',u'廊坊市':u'河北省',u'徐水县':u'河北省',u'唐山':u'河北省',
    u'海拉尔':u'内蒙古自治区',u'喀喇沁左翼':u'内蒙古自治区',u'喀喇沁':u'内蒙古自治区',u'前郭尔罗斯':u'内蒙古自治区',u'堆龙德庆区':u'西藏自治区',
    u'白城铁路运输法院':u'吉林省',u'白河林区':u'吉林省',u'临江林区':u'吉林省',u'江源林区':u'吉林省',u'吉林':u'吉林省',u'通化':u'吉林省',
 }

# for k in area.keys():
#     print k,area[k]
# con = MySQLdb.connect(host='192.168.12.34', user='liuf', passwd='123456', db='laws_doc', charset='utf8')
# cursor = con.cursor()
# sql = "select id, province,court from tmp_raolu where province ='None'"
# #
# cursor.execute(sql)
# row = cursor.fetchall()
# for i in row:
#     print i[1],i[2]
# # print p.keys()
# def update(int_num):
#     con = MySQLdb.connect(host='192.168.12.34', user='liuf', passwd='123456', db='laws_doc', charset='utf8')
#     cursor = con.cursor()
#     sql = "select id, province,court from tmp_raolu"
#     cursor.execute(sql)
#     row = cursor.fetchall()
#     p = {}
#     for i in row:
#         if u'北京' == i[1]:
#             province1 = u'北京市'
#             p[int(i[0])] = province1
#         elif u'天津' == i[1]:
#             province1 = u'天津市'
#             p[int(i[0])] = province1
#         elif u'上海' == i[1]:
#             province1 = u'上海市'
#             p[int(i[0])] = province1
#         elif u'重庆' == i[1]:
#             province1 = u'重庆市'
#             p[int(i[0])] = province1
#     a_list = []
#     for k in p.keys():
#         a_list.append(int(k))
#     print len(a_list)
#     for n in int_num:
#         if n in a_list:
#             print n,p[n]
#             sql = "update tmp_raolu set province= '%s' where id='%s'" % (p[n], n)
#             cursor.execute(sql)
#     con.commit()
#     cursor.close()
#     con.close()
# if __name__ == '__main__':
#     pool = multiprocessing.Pool(processes=5)
#     pool.apply_async(update, (xrange(40 * 10000),))
#     pool.apply_async(update, (xrange(40 * 10000, 80 * 10000),))
#     pool.apply_async(update, (xrange(80*10000, 120*10000), ))
#     pool.apply_async(update, (xrange(120*10000, 160*10000), ))
#     pool.apply_async(update, (xrange(160*10000, 190*10000), ))
#     pool.close()
#     pool.join()
# con = MySQLdb.connect(host='192.168.12.34', user='liuf', passwd='123456', db='laws_doc', charset='utf8')
# cursor = con.cursor()
# sql = "select id, province,court from tmp_raolu where province is Null "
# cursor.execute(sql)
# row = cursor.fetchall()
# #
# for i in row:
#     province = i[1]
#     for a in area.keys():
#         if a in i[2]:
#             province = area[a]
#     if province is Null:
#         print province
    # print i[2],province
#     sql = "update tmp_raolu set province= '%s' where id='%s'" % (province, i[0])
#     cursor.execute(sql)
# con.commit()
con = MySQLdb.connect(host='192.168.12.34', user='liuf', passwd='123456', db='laws_doc', charset='utf8')
cursor = con.cursor()
sql = "select uuid, province,court from tmp_raolu where province is Null"
cursor.execute(sql)
row = cursor.fetchall()
def update(int_num):
    for n in int_num:
        province = row[n][1]
        for a in area.keys():
            if a in row[n][2]:
                province = area[a]
        print row[n][2],province
        sql = "update tmp_raolu set province= '%s' where uuid='%s'" % (province, row[n][0])
        cursor.execute(sql)
    con.commit()
    cursor.close()
    con.close()
if __name__ == '__main__':
    pool = multiprocessing.Pool(processes=5)
    pool.apply_async(update, (xrange(2 * 1000),))
    pool.apply_async(update, (xrange(2 * 1000, 4 * 1000),))
    pool.apply_async(update, (xrange(4 * 1000, 6 * 1000),))
    pool.apply_async(update, (xrange(6 * 1000, 8 * 1000),))
    pool.apply_async(update, (xrange(8 * 1000, 11 * 1000),))
    pool.close()
    pool.join()
