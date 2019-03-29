from kafka import KafkaConsumer

KAFKA_SERVER_IP = '127.0.0.1'
KAFKA_TOPIC = 'mytopic'


consumer = KafkaConsumer(KAFKA_TOPIC, auto_offset_reset='earliest', bootstrap_servers=KAFKA_SERVER_IP)

#一个消费者可以订阅多个topic, 传入元组
# consumer.subscribe(topics=('test','test0'))


# 指定group
# consumer = KafkaConsumer('test',group_id='my-group',bootstrap_servers=['127.0.0.1:9092'])
print('start read message')
for message in consumer:    # 会是个迭代器，如果没有消息会阻塞
    print("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition, message.offset, message.key, message.value))


# msg = consumer.poll(timeout_ms=5)   #主动从kafka拉取消息

