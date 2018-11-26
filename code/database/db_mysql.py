#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
MYSQL数据库操作相关
"""
import contextlib
import traceback

from warnings import filterwarnings

import pymysql

__author__ = "风轻清淡"

filterwarnings('ignore', category=pymysql.Warning)


class MySQL(object):
    """
    MySQL数据库操作类
    """

    def __init__(self, db_config):
        self.host = db_config['host']
        self.port = db_config['port']
        self.user = db_config['user']
        self.passwd = db_config['passwd']
        self.db_name = db_config['db_name']
        self.charset = db_config['charset']

    @contextlib.contextmanager
    def _connect(self):
        self._conn = pymysql.connect(host=self.host,
                                     port=self.port,
                                     user=self.user,
                                     passwd=self.passwd,
                                     db=self.db_name,
                                     charset=self.charset)
        cursor = self._conn.cursor(cursor=pymysql.cursors.DictCursor)
        try:
            yield cursor
        except pymysql.err.IntegrityError:
            pass
        except pymysql.Error:
            self._conn.rollback()
            traceback.print_exc()
        finally:
            self._conn.commit()
            cursor.close()
            self._conn.close()

    def insert(self, item_list: list, columns, table_name='proxy'):
        """
        数据库插入内容，支持多条插入
        插入格式如下：
        [('1', '1', '1'), ('1', '1', '1')]
        """
        columns_str = '(' + ','.join(columns) + ')'
        value_str = '(' + ('%s,' * len(columns)).rstrip(',') + ')'

        with self._connect() as cursor:
            sql = "INSERT IGNORE INTO {}{} VALUES {}".format(table_name, columns_str, value_str)
            cursor.executemany(sql, item_list)

    def delete(self, conditions=None, table_name='proxy'):
        """
        从数据表中删除记录
        :param table_name:
        :param conditions:
        :return:
        """
        item_list = []
        condition_str = ''
        if conditions:
            condition_list = []
            for item in conditions.keys():
                item_str = '{}=%s'.format(item)
                item_list.append(conditions.get(item))
                condition_list.append(item_str)
            condition_str = "WHERE " + " AND ".join(condition_list)

        with self._connect() as cursor:
            sql = "DELETE FROM {} {}".format(table_name, condition_str)
            cursor.execute(sql, tuple(item_list))
            return cursor.rowcount

    def update(self, conditions: dict, value: dict, table_name='proxy'):
        """
        conditions的格式是个字典。
        :param table_name:
        :param conditions:
        :param value:也是个字典：{'ip':'192.168.0.1'}
        :return:
        """
        value_list = []
        item_list = []
        for item in value.keys():
            item_str = "{}=%s".format(item)
            item_list.append(value.get(item))
            value_list.append(item_str)
        value_str = ", ".join(value_list)

        condition_str = ''
        if conditions:
            condition_list = []
            for item in conditions.keys():
                item_str = '{}=%s'.format(item)
                item_list.append(conditions.get(item))
                condition_list.append(item_str)
            condition_str = "WHERE " + " AND ".join(condition_list)

        with self._connect() as cursor:
            sql = "UPDATE {} SET {} {}".format(table_name, value_str, condition_str)
            cursor.execute(sql, tuple(item_list))
            return cursor.rowcount

    def select(self, conditions: dict = None, columns=None, other='', table_name='proxy'):
        """
        :param other:
        :param conditions:
        :param columns:
        :param table_name:
        :return:
        """
        item_list = []
        condition_str = ''
        if conditions:
            condition_list = []
            for item in conditions.keys():
                item_str = '{}=%s'.format(item)
                item_list.append(conditions.get(item))
                condition_list.append(item_str)
            condition_str = "WHERE " + " AND ".join(condition_list)

        if columns is None:
            columns = ['*']

        value_str = ", ".join(columns)
        with self._connect() as cursor:
            sql = "SELECT {} FROM {} {} {}".format(value_str, table_name, condition_str, other)
            cursor.execute(sql, tuple(item_list))
            rows = cursor.fetchall()
            return rows


if __name__ == '__main__':
    config = {
        'host': '192.168.188.134',
        'port': 3306,
        'user': 'python',
        'passwd': '123456',
        'db_name': 'python',
        'charset': 'utf8'
    }
    db = MySQL(config)
    db.update(dict(id='123', key='Hello'), dict(id='456'), 'news')
    db.insert([('1', '1', '1', '1', '1', '1'), ('1', '1', '1', '1', '1', '1')], 'news')
