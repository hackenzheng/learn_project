
# 单机调试使用前要先启动zookeeper和kafka服务
# 启动zookeeper要cd /home/lp/soft/kafka_2.11-1.1.0,然后 bin/zookeeper-server-start.sh config/zookeeper.properties
# 启动kafka要cd /home/lp/soft/kafka_2.11-1.1.0,然后bin/kafka-server-start.sh config/server.properties

from kafka import KafkaConsumer
from kafka.structs import TopicPartition


KAFKA_SERVER_IP = '127.0.0.1'


class kafka_consumer():

    def __init__(self,kafka_server=KAFKA_SERVER_IP):
        self.kafka_servers=kafka_server    # kafka服务器的消费者接口
        self.consumer=None
        self.topic=None

    # 设置消费者.使用group,对于同一个group的成员只有一个消费者实例可以读取数据。
    def set_consumer(self,topic='device',group_id=None,auto_offset_reset='latest'):
        self.topic=topic
        if (group_id):
            self.consumer = KafkaConsumer(topic, group_id=group_id, auto_offset_reset=auto_offset_reset,bootstrap_servers=self.kafka_servers)
        else:
            self.consumer = KafkaConsumer(topic, auto_offset_reset=auto_offset_reset,bootstrap_servers=self.kafka_servers)


    # callback为回调函数，这是一个堵塞进行
    def read_data(self,callback):
        if(self.consumer):
            for message in self.consumer:
                callback(message)
                # print("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,message.offset, message.key,message.value))


    # 获取当前消费者信息
    def get_consumer_info(self):
        cousumer_info={}
        cousumer_info['partitions_for_topic'] =self.consumer.partitions_for_topic(self.topic)  #获取test主题的分区信息
        cousumer_info['topic']=self.consumer.topics()  #获取主题列表
        cousumer_info['subscription'] = self.consumer.subscription()  #获取当前消费者订阅的主题
        cousumer_info['assignment'] = self.consumer.assignment()  #获取当前消费者topic、分区信息
        cousumer_info['beginning_offsets'] = self.consumer.beginning_offsets(self.consumer.assignment()) #获取当前消费者可消费的偏移量
        return cousumer_info


    # 设置偏移
    def set_offset(self,partition=0,offset=0):
        self.consumer.seek(TopicPartition(topic=self.topic, partition=partition), offset)  # 重置偏移量，从第offset个偏移量消费
        return self.consumer.position(TopicPartition(topic=self.topic, partition=partition)) #获取当前主题的最新偏移量

    # 手动拉取消息
    def pull_data(self,callback):
        msg = self.consumer.poll(timeout_ms=5)  # 从kafka获取消息
        callback(msg)


    # ======读取当前数据==========
    # 使用group,对于同一个group的成员只有一个消费者实例可以读取数据。callback为回调函数，这是一个堵塞进行
    def read_data_now(self,callback,topic='device',group_id=None,auto_offset_reset='latest'):
        if(group_id):
            consumer = KafkaConsumer(topic,group_id=group_id,auto_offset_reset=auto_offset_reset,bootstrap_servers=self.kafka_servers)
            for message in consumer:
                callback(message)
                # print("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,message.offset, message.key,message.value))
        else:
            consumer = KafkaConsumer(topic,auto_offset_reset=auto_offset_reset,bootstrap_servers=self.kafka_servers)
            for message in consumer:
                callback(message)
                # print("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition, message.offset, message.key, message.value))


# ==============消息恢复和挂起===========

# from kafka import KafkaConsumer
# from kafka.structs import TopicPartition
# import time
#
# consumer = KafkaConsumer(bootstrap_servers=['127.0.0.1:9092'])
# consumer.subscribe(topics=('test'))
# consumer.topics()
# consumer.pause(TopicPartition(topic=u'test', partition=0))  # pause执行后，consumer不能读取，直到调用resume后恢复。
# num = 0
# while True:
#     print(num)
#     print(consumer.paused())   #获取当前挂起的消费者
#     msg = consumer.poll(timeout_ms=5)
#     print(msg)
#     time.sleep(2)
#     num = num + 1
#     if num == 10:
#         print("resume...")
#         consumer.resume(TopicPartition(topic='test', partition=0))
#         print("resume......")


# ======消费者分组==========
# from kafka import KafkaConsumer
# # 使用group,对于同一个group的成员只有一个消费者实例可以读取数据
# consumer = KafkaConsumer('test',group_id='my-group',bootstrap_servers=['127.0.0.1:9092'])
# for message in consumer:
#     print("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,message.offset, message.key,message.value))



# =====读取消息队列最早或最新的消息========
# from kafka import KafkaConsumer
# consumer = KafkaConsumer('test',auto_offset_reset='earliest',bootstrap_servers=['127.0.0.1:9092'])
# for message in consumer:
#     print("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,message.offset, message.key,message.value))
#


# # ==========读取指定位置消息===============
# from kafka import KafkaConsumer
# from kafka.structs import TopicPartition
#
# consumer = KafkaConsumer('test',bootstrap_servers=['127.0.0.1:9092'])
#
# print(consumer.partitions_for_topic("test"))  #获取test主题的分区信息
# print(consumer.topics())  #获取主题列表
# print(consumer.subscription())  #获取当前消费者订阅的主题
# print(consumer.assignment())  #获取当前消费者topic、分区信息
# print(consumer.beginning_offsets(consumer.assignment())) #获取当前消费者可消费的偏移量
# consumer.seek(TopicPartition(topic='test', partition=0), 5)  #重置偏移量，从第5个偏移量消费
# for message in consumer:
#     print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,message.offset, message.key,message.value))



# =======订阅多个消费者==========

# from kafka import KafkaConsumer
# from kafka.structs import TopicPartition
#
# consumer = KafkaConsumer(bootstrap_servers=['127.0.0.1:9092'])
# consumer.subscribe(topics=('test','test0'))  #订阅要消费的主题
# print(consumer.topics())
# print(consumer.position(TopicPartition(topic='test', partition=0))) #获取当前主题的最新偏移量
# for message in consumer:
#     print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,message.offset, message.key,message.value))


# ==========消费者(手动拉取消息)============
#
# from kafka import KafkaConsumer
# import time
#
# consumer = KafkaConsumer(bootstrap_servers=['127.0.0.1:9092'])
# consumer.subscribe(topics=('test','test0'))
# while True:
#     msg = consumer.poll(timeout_ms=5)   #从kafka获取消息
#     print(msg)
#     time.sleep(2)