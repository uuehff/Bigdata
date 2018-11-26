#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
PostgreSQL数据库操作相关
"""
import contextlib
import psycopg2
import psycopg2.extras

__author__ = "风轻清淡"

HOST = 'localhost'
DB_NAME = 'legal_doc'
USER_NAME = 'postgres'
USER_PWD = 'postgres'
PORT = 5432


@contextlib.contextmanager
def connect_postgre(host=HOST, port=PORT, user=USER_NAME, password=USER_PWD, database=DB_NAME):
    conn = psycopg2.connect(host=host, port=port, user=user, password=password, database=database)
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
        yield cursor
    except psycopg2.IntegrityError as error:
        print(error)
    except psycopg2.Error as error:
        print(error)
    finally:
        conn.commit()
        cursor.close()
        conn.close()


def select_doc(limit=1, offset=0):
    with connect_postgre() as cursor:
        sql = "SELECT * FROM tb_case ORDER BY id ASC LIMIT {} OFFSET {}".format(limit, offset)
        cursor.execute(sql)
        rows = cursor.fetchall()
        return rows


if __name__ == "__main__":
    print(select_doc())
