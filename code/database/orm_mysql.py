#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
数据库操作
"""

from sqlalchemy import create_engine

__author__ = "风轻清淡"


class SqlHelper:
    def __init__(self, connect):
        """
        初始化数据库链接
        :param connect: 数据库连接信息
        """
        self.engine = create_engine(connect, echo=False)

    def insert(self, item_list: list, columns=None, table_name='proxys'):
        """
        增
        :param table_name:
        :param columns:
        :param item_list:
        :return:
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
        sql = "INSERT IGNORE INTO {}{} VALUES {}".format(table_name, columns, sql_str)
        with self.engine.connect() as conn:
            trans = conn.begin()
            try:
                conn.execute(sql)
                trans.commit()
            except Exception as error:
                trans.rollback()
                print(error)
            finally:
                trans.close()

    def delete(self, conditions=None, table_name='proxys'):
        """
        删
        :param table_name:
        :param conditions:
        :return:
        """
        condition_list = []
        for item in conditions.keys():
            item_str = '{}="{}"'.format(item, conditions.get(item))
            condition_list.append(item_str)
        condition_str = " AND ".join(condition_list)
        sql = "DELETE FROM {} WHERE {}".format(table_name, condition_str)
        with self.engine.connect() as conn:
            trans = conn.begin()
            try:
                conn.execute(sql)
                trans.commit()
            except Exception as error:
                trans.rollback()
                print(error)
            finally:
                trans.close()

    def update(self, conditions: dict, value: dict, table_name='proxys'):
        """
        conditions的格式是个字典。类似self.params
        :param table_name:
        :param conditions:
        :param value:也是个字典：{'ip':'192.168.0.1'}
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

        sql = "UPDATE {} SET {} WHERE {}".format(table_name, value_str, condition_str)
        with self.engine.connect() as conn:
            trans = conn.begin()
            try:
                conn.execute(sql)
                trans.commit()
            except Exception as error:
                trans.rollback()
                print(error)
            finally:
                trans.close()

    def select(self, conditions: dict = None, columns=None, other='', table_name='proxys'):
        """
        :param other:
        :param conditions:
        :param columns:
        :param table_name:
        :return:
        """
        condition_list = []
        condition_str = ''
        if conditions:
            for item in conditions.keys():
                item_str = '{}="{}"'.format(item, conditions.get(item))
                condition_list.append(item_str)
            condition_str = "WHERE " + " AND ".join(condition_list)

        if columns is None:
            columns = ['*']

        value_str = ", ".join(columns)

        sql = "SELECT {} FROM {} {} {}".format(value_str, table_name, condition_str, other)
        with self.engine.connect() as conn:
            trans = conn.begin()
            try:
                rows = conn.execute(sql)
            except Exception as error:
                trans.rollback()
                print(error)
            else:
                return rows
            finally:
                trans.close()


if __name__ == '__main__':
    pass
