#coding=utf-8

# pykafka API:http://pykafka.readthedocs.io/en/latest/api/producer.html


from pykafka import KafkaClient,Topic,Producer,BalancedConsumer,SimpleConsumer  #方便看源码！
from pykafka.partitioners import BasePartitioner

# partitioner=partitioner,是topic.get_producer()的参数！默认:random_partitioner
# partition_key=key，是producer.produce()的参数！类型：bytes

def producer(topic,message):
    producer = topic.get_producer()

    producer.produce(message)

    producer.stop()


def sync_producer(topic,message):
    with topic.get_sync_producer() as producer:
        # for j in range(100):
        #     #time.sleep(0.1)
        #     for i in range(1):
        #         producer.produce('test message>>' + str(i ** 2))
        producer.produce(message)


client = KafkaClient(hosts="cdh-slave2:9092,cdh-slave1:9092",zookeeper_hosts="cdh-master:2181")
topic = client.topics['test_in21']

message = "input"
# p = '5'
producer(topic,message)