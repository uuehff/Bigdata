#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
修正抽取判决文书底部数据
"""
import re
import time

from multiprocessing import Pool

from database.db_mysql import MySQL


__author__ = "风轻清淡"

DB_CONFIG = {
    'host': '192.168.12.34',
    'port': 3306,
    'user': 'tzp',
    'passwd': '123456',
    'db_name': 'laws_doc',
    'charset': 'utf8'
}

reg_footer = re.compile(r'\n(?:\S{0,2}审判).*(?:书记员|\S+年\S+月)\S+', re.S)
reg_replace = re.compile(r'附\S+$')


def doc_items(items):
    item_id = items.get('id')
    doc_footer = items.get('doc_footer')
    footer_result = re.findall(reg_footer, doc_footer)
    if footer_result:
        doc_footer = footer_result[0].strip()
    doc_footer = re.sub(reg_replace, '', doc_footer)
    items_dict = dict(doc_footer=doc_footer, mark=1)
    return item_id, items_dict


def select_data():
    sql_helper = MySQL(DB_CONFIG)
    conditions = {'mark': 0}
    columns = ['id', 'doc_footer']
    other = ' LIMIT 20000'
    rows = sql_helper.select(conditions=conditions, columns=columns, other=other, table_name='tmp_footer')
    return rows


def update_data(conditions: dict, value: dict):
    """
    更新数据库记录
    :param conditions: dict
    :param value: dict
    :return:
    """
    sql_helper = MySQL(DB_CONFIG)
    sql_helper.update(conditions=conditions, value=value, table_name='tmp_footer')


def worker(items):
    try:
        items_dict = doc_items(items)
    except Exception as error:
        print(error)
    else:
        if isinstance(items_dict, tuple):
            item_id = items_dict[0]
            conditions = {'id': item_id}
            print(items_dict)
            update_data(conditions=conditions, value=items_dict[1])


def footer_main():
    while 1:
        pool = Pool(24)
        rows = select_data()
        if not rows:
            break
        pool.map(worker, rows)
        pool.close()
        pool.join()


if __name__ == "__main__":
    footer_main()
