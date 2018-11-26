#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
MYSQL数据库操作相关
"""

import contextlib
from random import choice
from warnings import filterwarnings

import pymysql

__author__ = "风轻清淡"

proxy_list = []

HOST = '127.0.0.1'
DB_NAME = 'wenshu'
YEAR_DB_NAME = 'doc_year'
USER_NAME = 'root'
USER_PWD = 'Mc0xBPMtxHTE'
PORT = 3306

filterwarnings('ignore', category=pymysql.Warning)


@contextlib.contextmanager
def mysql_connect(host=HOST, user=USER_NAME, password=USER_PWD, database='wenshu'):
    """
    定义上下文管理器，连接后自动关闭连接
    """
    conn = pymysql.connect(
        host=host,
        port=PORT,
        user=user,
        passwd=password,
        db=database,
        charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    try:
        yield cursor
    except pymysql.err.IntegrityError:
        pass
    except pymysql.Error as error:
        print(error)
    finally:
        conn.commit()
        cursor.close()
        conn.close()


def insert_data(item_list: list, columns=None, table_name='article', db_name='law_64365'):
    """
    数据库插入内容，支持多条插入
    插入格式如下：
    [('1', '1', '1'), ('1', '1', '1')]
    """
    if columns is None:
        columns = ''
    else:
        columns = '(' + ','.join(columns) + ')'

    sql_list = []
    for item in item_list:
        sql_str = str(item)
        sql_list.append(sql_str)
    sql_str = ','.join(sql_list).lstrip(',').replace('%', '%%')
    with mysql_connect(database=db_name) as cursor:
        sql = "INSERT IGNORE INTO {}{} VALUES {}".format(table_name, columns, sql_str)
        cursor.execute(sql)


def update_data(conditions: dict, value: dict, table_name='article', db_name='law_64365'):
    """
    更新数据库记录
    :param db_name:
    :param conditions: dict
    :param value: dict
    :param table_name:
    :return:
    """
    condition_list = []
    for item in conditions.keys():
        item_str = '{}="{}"'.format(item, conditions.get(item))
        condition_list.append(item_str)
    condition_str = " AND ".join(condition_list)

    value_list = []
    for item in value.keys():
        item_str = "{}='{}'".format(item, value.get(item))
        value_list.append(item_str)
    value_str = ", ".join(value_list)

    with mysql_connect(database=db_name) as cursor:
        sql = "UPDATE {} SET {} WHERE {}".format(table_name, value_str, condition_str)
        cursor.execute(sql)


def select_data(conditions: dict, columns=None, table_name='article', db_name='law_64365'):
    """

    :param db_name:
    :param conditions:
    :param columns:
    :param table_name:
    :return:
    """
    condition_list = []
    for item in conditions.keys():
        item_str = '{}="{}"'.format(item, conditions.get(item))
        condition_list.append(item_str)
    condition_str = " AND ".join(condition_list)

    if columns is None:
        columns = ['*']

    value_str = ", ".join(columns)

    with mysql_connect(database=db_name) as cursor:
        sql = "SELECT {} FROM {} WHERE {}".format(value_str, table_name, condition_str)
        print(sql)
        cursor.execute(sql)
        rows = cursor.fetchone()
        return rows


def insert_proxy(proxy_item):
    with mysql_connect(host='192.168.10.22', user='tzp', password='123456', database='proxy') as cursor:
        sql = "INSERT IGNORE INTO proxys(ip,port,speed) VALUES {}".format(proxy_item)
        cursor.execute(sql)


if __name__ == "__main__":
    update_data(dict(id='123', key='Hello'), dict(id='456'))
    insert_data([('1', '1', '1', '1', '1', '1'), ('1', '1', '1', '1', '1', '1')])
