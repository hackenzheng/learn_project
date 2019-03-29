

服务器部署kafka的修改

首先要修改zk的端口号，因为服务器可能有许多zk在运行。

在kafka目录config文件夹下zookeeper.properties文件中修改为

clientPort=2185


server.properties文件中修改为，因为zk和kafka是合并在一起运行的，所以可以使用localhost

zookeeper.connect=localhost:2185


修改server.properties文件中kafka监听的端口号，并保障服务器端口号是打开的。不修改的话kafka只能监听本地端口号。

listeners=PLAINTEXT://192.168.180.128:9092



生产者：

1. k8s在部署kafka之后，必须保证pod对应的service的NodePort 和port 是一样的，即docker内部端口和外部暴露端口保持一致。

例如：

 

2. 将pod所在物理主机IP 和sercieName（podName和serviceName一样） 绑定到，使用API的客户端主机的hosts上

例如：

 

消费者：

1. 消费者的group.id，必须保持和pod中的consumer.properties文件里的group.id=test-consumer-group需要改成一致，不然无法消费

 

整体注意点：

1. 不同版本引用的jar包是不一样的，必须一一对应



创建主题
bin/kafka-topics.sh --create --zookeeper 10.233.61.237:2181 --replication-factor 1 --partitions 1 --topic device     这里面使用的是集群ip，容器间访问
创建消费者
bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic device --from-beginning   
创建生产者
bin/kafka-console-producer.sh --broker-list localhost:9092 --topic device     使用本地ip
bin/kafka-console-producer.sh --broker-list 10.233.9.150:9092 --topic device     使用clusterip
bin/kafka-console-producer.sh --broker-list 192.168.2.177:30946 --topic device    使用外网ip和nodeport