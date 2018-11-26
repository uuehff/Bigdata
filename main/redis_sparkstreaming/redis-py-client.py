#coding=utf-8


from rediscluster import StrictRedisCluster

if __name__ == '__main__':
    # rc = StrictRedisCluster(host="192.168.10.225", port=6379,password="hhly2017")
    startup_nodes = [{"host": "192.168.10.225", "port": 6379},{"host": "192.168.12.34", "port": 6379},{"host": "192.168.12.35", "port": 6379}]
    rc = StrictRedisCluster(startup_nodes=startup_nodes, decode_responses=True,password="hhly2017")
    # rc.connection_pool()
    # rc.rpush("r","2")
    # rc.rpush("r","3")
    # rc.rpush("r","1")
    for i in rc.lrange("redis",0,-1):
        print i
    

