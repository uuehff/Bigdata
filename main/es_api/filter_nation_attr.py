# -*- coding: utf-8 -*-

from DB import MysqlDB
from bs4 import BeautifulSoup
import redis
from multiprocessing import Process


def send_law_id_redis():    # 将law_id放到redis
    # 如果redis没有数据，将数据库的内容插入到redis
    if not rd.exists("wait_filter_url"):
        if not rd.exists("wait_filter_lock"):
            rd.rpush("wait_filter_lock", 1)
        else:
            return "push redis ing"
        total_sql = "select law_id from law_link where filter_state=0 and state =1 limit 0, 10000"
        total_url = db.select_all(total_sql)
        # 这里是没有连接了
        if len(total_url) == 0:
            rd.lpop("wait_filter_lock")
            return "have no data"
        for url in total_url:
            rd.rpush("wait_filter_url", url[0])
        if rd.exists("wait_filter_lock"):
            rd.lpop("wait_filter_lock")

    return str(rd.lpop("wait_filter_url"), encoding='utf-8')


def clean_chars(txt):
    if txt is None:
        return ""
    if isinstance(txt, str):
        if txt != "":
            return txt.strip()
        else:
            return ""
    else:
        return txt


def filter_attr(attr_body):  # 清洗属性标签
    l_key = ["制定机关", "文号", "效力等级", "主题分类", "公布日期", "施行日期", "时效性"]
    l_var = ["enact_org", "law_doc_num", "eff_gra", "sub_cla", "page_pub_date", "page_imp_date", "timeliness"]
    soup_attr = attr_body.findAll("li")
    r_dict = {}
    for attr in soup_attr:
        attr_name = attr.find("div", class_="nop-t1").get_text().strip()
        attr_var = attr.find("div", class_="nop-t2").get_text().strip()
        r_dict[l_var[l_key.index(attr_name)]] = clean_chars(attr_var)
    return r_dict


def body_id():      # 提取内容里的id
    pass


def legal_evolution():  # 提取法律沿革
    pass


def main_body():     # 分析内容
    law_id = send_law_id_redis()
    # 正在插入redis
    if law_id == "push redis ing":
        return
    # 弄完了没数据了
    if law_id == "have no data":
        return "have no data"
    sql = "select " \
          "law_doc_url,cas_tit,lib_id,lib_name,law_title,law_doc_num,pub_date,imp_date,html_resouce " \
          "from law_link where state=1 and law_id='{}'".format(law_id)
    # sql = "select " \
    #       "law_doc_url,cas_tit,lib_id,lib_name,law_key_word,law_title,law_doc_num,pub_date,imp_date,html_resouce " \
    #       "from law_link where state=1 and law_id='{}'".format("A100004")
    rest = db.select_one(sql)
    if rest[-1] is None:
        return
    # 这里要筛选频率过快的
    if "您的访问频率过快，请稍后刷新" in str(rest[-1]) or "你的访问篇数已超过最大限制数" in str(rest[-1]):
        return
    # 这里要筛选下只爬了一半的
    if "footerMod bt_none" not in str(rest[-1]):
        return
    html = BeautifulSoup(rest[-1], "lxml")
    attr_body = html.findAll("div", class_="naturePop clearfix js_pop")[0]
    attr_dict = filter_attr(attr_body)
    rest_dict = {
        "law_id": law_id,
        "law_doc_url":  clean_chars(rest[0]),
        "cas_tit": clean_chars(rest[1]),
        "lib_id": clean_chars(rest[2]),
        "lib_name": clean_chars(rest[3]),
        "law_title": clean_chars(rest[4]),
        "law_doc_num": clean_chars(rest[5]),
        "pub_date": clean_chars(rest[6]),
        "imp_date": clean_chars(rest[7])
    }
    try:
        r_dict = dict(attr_dict, **rest_dict)
        column_key = str(tuple(r_dict)).replace("'", "")
        column_var = tuple(r_dict.values())
        in_sql = "insert into law_link_filter {} values {}".format(column_key, column_var)
        print(law_id)
        db.insert_data(in_sql)
        up_sql = "update law_link set filter_state=1 where law_id='{}'".format(law_id)
        db.update_data(up_sql)
    except:
        return "insert err"


db = MysqlDB(host="192.168.74.100", user="huanght", password="Huanght@123456", db="hht_laws_faxin")
pool = redis.ConnectionPool(host="192.168.74.100", port=6379, db=14)
rd = redis.Redis(connection_pool=pool)


def main():
    while True:
        main_rest = main_body()
        # main_rest = "123"
        if main_rest == "have no data":
            return


if __name__ == "__main__":

    processes = list()
    for i in range(3):
        p = Process(target=main, args=())
        print('Process will start.')
        p.start()
        processes.append(p)
    for p in processes:
        p.join()
