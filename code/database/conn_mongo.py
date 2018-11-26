#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Mongo Conn连接类
"""
import pymongo

__author__ = "风轻清淡"

server_name = "mongodb://192.168.10.22:27017"
local_server = "mongodb://127.0.0.1:27017"


def get_conn(server=server_name, db_name='spider', connection='comment_list'):
    client = pymongo.MongoClient(server)
    db_conn = client.get_database(db_name)
    connections = db_conn[connection]
    return connections


if __name__ == "__main__":
    print(get_conn())
