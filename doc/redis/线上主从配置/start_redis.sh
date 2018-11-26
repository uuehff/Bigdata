#!/bin/bash
sudo /data/redis/redis-4.0.1/src/redis-server /data/redis/redis-4.0.1/redis.conf
ssh cdh-slave1 -p 2222 "sudo /data/redis/redis-4.0.1/src/redis-server /data/redis/redis-4.0.1/redis.conf "
