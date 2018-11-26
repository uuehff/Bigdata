#!/usr/bin/env python
import pymysql
from pymysql import escape_string


class MysqlDB(object):
    """
    接收数据库参数
    """
    def __init__(self, host="127.0.0.1", user="root", password="", port=3306, db="", charset="utf8"):
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.db = db
        self.charset = charset

        self.conn = self.connect()
        if self.conn:
            self.cursor = self.conn.cursor()


    def connect(self):
        try:
            conn = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                port=self.port,
                db=self.db,
                charset=self.charset
            )
        except pymysql.Error as e:
            return e
        return conn

    def select_all(self, sql):
        try:
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except pymysql.Error as e:
            return e

    def select_one(self, sql):
        try:
            self.cursor.execute(sql)
            return self.cursor.fetchone()
        except pymysql.Error as e:
            return e
        # finally:
        #     self.close()

    def insert_data(self, sql):
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(sql, "insert Error")
            return e
        # finally:
        #     self.close()

    def delete_data(self, sql):
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except pymysql.Error as e:
            return e
        # finally:
        #     self.close()

    def update_data(self, sql):
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(e)
            return e
        # finally:
        #     self.close()

    def trans_data(self, ret):
        r = pymysql.escape_string(ret)
        return r

    def close(self):
        self.cursor.close()
        self.conn.close()

    def __del__(self):
        self.close()


if __name__ == '__main__':
    db = MysqlDB()
