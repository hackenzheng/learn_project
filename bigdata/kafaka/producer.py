# kafka包的安装：  pip install kafka-python

from kafka import KafkaProducer
import time, json


#要带端口，没有端口使用默认的9092， 若是集群IP可以是多个['0.0.0.1:9092','0.0.0.2:9092','0.0.0.3:9092' ]
KAFKA_SERVER_IP = '127.0.0.1:9092'
KAFKA_TOPIC = 'mytopic'

# 在这里就会尝试连接borker,若服务没起来会抛异常
producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER_IP)
i=0
while i<1000000:
    i+=1
    msg = {'userid':i, 'name':'test'+str(i), 'age':i}
    print(msg)
    # 消息为bytes类型的数据，topic不存在会主动创建一个,有可能发送超时
    producer.send(KAFKA_TOPIC,  json.dumps(msg).encode('utf-8'))
    # time.sleep()

producer.close()