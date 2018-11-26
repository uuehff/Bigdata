from pykafka import KafkaClient
client = KafkaClient(hosts="cdh-slave2:9092")
topic = client.topics['console_data_in']
#producer = topic.get_producer()
#producer.produce(['testmessage'])
with topic.get_sync_producer() as producer:
    for i in range(4):
        producer.produce(str(i))

