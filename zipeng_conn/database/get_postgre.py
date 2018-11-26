#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
225 PostgreSQL数据获取示例
"""
import psycopg2
from psycopg2 import extras

__author__ = "风轻清淡"


def art_select():
    conn = psycopg2.connect(database="law_new", user="postgres", password="hhlypost", host="192.168.10.225",
                            port="5432")
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("select * from criminal_case where id<2")
    res = [dict(record) for record in cur]
    cur.close()
    conn.close()
    return res


d = art_select()
