
# 使用前需要启动hbase和thrift服务器
# 启动hbase在cd /usr/local/hbase下bin/start-hbase.sh   默认端口为 60000
# 启动thrift服务器cd /usr/local/hbase/bin执行./hbase-daemon.sh start thrift   默认端口为9090


from py_rabbit import Rabbit_Consumer


def receive_message(ch, method, properties, body):
    print(" receive %r" % body)


consumer = Rabbit_Consumer()
consumer.set_queue()
consumer.set_receive_config(receive_message)
consumer.start_receive()

