#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
项目描述
"""
import sys
import os
sys.path.append(os.path.join(os.path.split(os.path.realpath(__file__))[0],"../database/"))
from db_mysql import *
from config import DB_CONFIG

__author__ = "风轻清淡"


def select_data():
    sql_helper = MySQL(DB_CONFIG)
    conditions = {'is_format': 0}
    columns = ['id', 'doc_content']
    other = ' LIMIT 2000'
    rows = sql_helper.select(conditions=conditions, columns=columns, other=other, table_name='judgment')
    return rows


def update_data(conditions: dict, value: dict):
    """
    更新数据库记录
    :param conditions: dict
    :param value: dict
    :return:
    """
    sql_helper = MySQL(DB_CONFIG)
    sql_helper.update(conditions=conditions, value=value, table_name='judgment')
