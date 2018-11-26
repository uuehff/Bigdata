#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
功能描述
"""
import redis

__author__ = "风轻清淡"

pool = redis.ConnectionPool(host='127.0.0.1', port=6379,  db=1)
respond = redis.Redis(connection_pool=pool)

if __name__ == "__main__":
    comment_url = respond.srandmember('detail_list', 1)[0].decode('utf-8')
    print(comment_url)
    if comment_url.find('page') > 0:
        respond.srem('detail_list', comment_url)
