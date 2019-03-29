## docker部署

拉取镜像:  
docker pull wurstmeister/zookeeper

docker pull wurstmeister/kafka

启动zookeeper，注意端口号，因为以后还有有其他的zookeeper

docker run -d --name kafka-zookeeper -p 2181:2181 --volume /etc/localtime:/etc/localtime wurstmeister/zookeeper:latest   

后台启动kafka:  
docker run -d --name kafka -p 9092:9092 --link kafka-zookeeper --env KAFKA_ZOOKEEPER_CONNECT=kafka-zookeeper:2181 --env KAFKA_ADVERTISED_HOST_NAME=localhost --env KAFKA_ADVERTISED_PORT=9092 --volume /etc/localtime:/etc/localtime wurstmeister/kafka:latest 


进入kafka容器内部测试发送消息:  
docker exec -it ${CONTAINER ID} /bin/bash 

kafka默认目录:  
cd /opt/kafka_2.11-2.0.0/


创建一个topic：topic是由zk保管的
./bin/kafka-topics.sh --create --zookeeper kafka-zookeeper:2181 --replication-factor 1 --partitions 1 --topic mykafka

运行一个消息生产者，使用刚刚创建的topic
./bin/kafka-console-producer.sh --broker-list localhost:9092 --topic mykafka


另起一个端口进入容器，启动消费者
cd /opt/kafka_2.11-2.0.0/

查看所有的topic列表
./bin/kafka-topics.sh --list --zookeeper kafka-zookeeper:2181

运行一个消费者，指定同样的主题，也是进入交互模式，会从头开始读取所有的消息，如果producer有消息输入，这边会立即显示
./bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic mykafka --from-beginning



