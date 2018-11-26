#!/bin/bash
echo "SHUTDOWN SAVE" | /data/redis/redis-4.0.1/src/redis-cli -c -a HHly2017 -h 10.33.51.2
echo "SHUTDOWN SAVE" | /data/redis/redis-4.0.1/src/redis-cli -c -a HHly2017 -h 10.33.52.2
