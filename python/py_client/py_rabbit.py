
import logging
from common.config import *
import time,json,datetime
import pika



class Rabbit_Producer():

    def __init__(self,host=RABBITMQ_SERVER_IP,port=RABBITMQ_SERVER_PORT,user=RABBITMQ_SERVER_USER,password=RABBITMQ_SERVER_PASSWORD,virtual_host='/'):    # 默认端口5672，可不写
        credentials = pika.PlainCredentials(user,password)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=port, credentials=credentials,virtual_host=virtual_host))   # virtual_host='/'
        self.channel = self.connection.channel()   #声明一个管道
        self.properties = pika.BasicProperties(    # 需要将消息发送到exchange，exchange会把消息分发给queue。queue会把消息分发给消费者
            delivery_mode=2,  # 消息持久化
            # content_type='application/json',
            # content_encoding='UTF-8',
            # priority=0,
            expiration = '60000'    # 有效时间，毫秒为单位
        )
        self.exchange_name=""
        self.exchange_type=""
        self.queue_name=""

    # 设置广播通道
    def set_exchange(self,exchange='intellif',exchange_type='topic'):
        self.exchange_name=exchange
        self.exchange_type=exchange_type
        # 注意：这里是广播，不需要声明queue
        self.channel.exchange_declare(exchange=exchange, exchange_type=exchange_type,durable=True)  # 声明广播管道
        logging.info('set rabbit exchange %s, type %s'%(exchange,exchange_type))

    # 设置队列，在直连模式下，需要设置队列，此时不启动广播器exchange
    def set_queue(self,queue_name='camera_queue'):
        self.queue_name=queue_name
        self.channel.queue_declare(queue=queue_name, durable=True)

    # 发送消息，传递字节流
    def send_message(self,message,rout_key = "recom"):
        # logging.info('send to rabbit: time is %s' % datetime.datetime.now())
        self.channel.basic_publish(exchange=self.exchange_name,routing_key=rout_key,body=message,properties=self.properties)  # body消息内容

    #删除exchange,  因为有时exchange会弄错
    def delete_exchange(self,exchange_name=None):
        if not exchange_name:
            exchange_name = self.exchange_name
        self.channel.exchange_delete(exchange_name)

    # 关闭，要记得关闭信道
    def close(self):
        self.channel.close()
        self.connection.close()


class Rabbit_Consumer():

    def __init__(self,host=RABBITMQ_SERVER_IP,port=RABBITMQ_SERVER_PORT,user=RABBITMQ_SERVER_USER,password=RABBITMQ_SERVER_PASSWORD,virtual_host='/'):    # 默认端口5672，可不写
        credentials = pika.PlainCredentials(user,password)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host,port=port,credentials=credentials,virtual_host=virtual_host))
        self.channel = self.connection.channel()   #声明一个管道
        self.exchange_name=""
        self.exchange_type=""
        self.queue_name=""


    # 设置广播接收队列.  exchange通过路由规则发送到符合路由规则的队列。用户订阅队列，就能收到该队列的消息。
    def set_queue(self,exchange='intellif',exchange_type='topic',queue_name='camera_queue',rout_key = "recom"):
        self.exchange_name=exchange
        self.exchange_type=exchange_type
        self.queue_name=queue_name
        if(exchange):
            # 声明转发器
            self.channel.exchange_declare(exchange=exchange, exchange_type=exchange_type,durable=True)
            # 发送方和接收方不知道谁首先连接到RabbitMQ，双方连接上来都先声明一个队列
            self.channel.queue_declare(queue=queue_name, durable=True)
            # queue绑定到转发器上
            self.channel.queue_bind(exchange=exchange, queue=queue_name,routing_key=rout_key)   # 如果是fanout，rout_key要设置成""
            logging.info('set rabbit queue %s bing to exchange %s'%(queue_name,exchange))
        else:
            print('====',exchange)
            self.channel.queue_declare(queue=queue_name, durable=True)

    # 设置消息接收配置
    def set_receive_config(self,callback,no_ack=True):
        # 声明接收收消息变量。#callback收到消息后执行的回调函数。no_ack默认不执行回复ack，以便服务器宕机，能被其他消费者接收
        self.channel.basic_consume(callback, queue=self.queue_name,no_ack=no_ack)

    # 开始接收消息，不停循环接收，没有消息挂起等待
    def start_receive(self):
        logging.info('start listening')
        self.channel.start_consuming()

    def close(self):
        self.channel.close()
        self.connection.close()