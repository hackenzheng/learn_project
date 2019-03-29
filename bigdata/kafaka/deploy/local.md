## ubuntu本地安装
   Kafka是使用scala编写的运行与jvm虚拟机上的程序，运行时需要java运行环境(jdk)，github上的kafka说还需要安装gradle，实际不用
   以前的kafka还需要zookeeper，新版的kafka已经内置了一个zookeeper环境，可以直接使用.   
   在kafka官网 http://kafka.apache.org/downloads下载编译好的二进制版tgz文件，
   版本kafka_2.12-2.2.0下载链接https://www.apache.org/dyn/closer.cgi?path=/kafka/2.2.0/kafka_2.12-2.2.0.tgz
   解压到/usr/bin或~/bin目录下即可
### java运行环境(jdk)安装
   jdk包含jre，Ubuntu自带了java环境，如果没有
   从oracle官网https://www.oracle.com/technetwork/java/javase/downloads/index.html下载Ubuntu适用的deb包，然后按安装即可

## 配置
启动参考： http://kafka.apache.org/quickstart

在kafka解压目录下config文件夹放置配置文件
consumer.properites 消费者配置
producer.properties 生产者配置
server.properties kafka服务器的配置，此配置文件用来配置kafka服务器，
broker.id 申明当前kafka服务器在集群中的唯一ID，需配置为integer,并且集群中的每一个kafka服务器的id都应是唯一的，
listeners 申明此kafka服务器需要监听的端口号，如果是在本机上跑虚拟机运行可以不用配置本项，默认会使用localhost的地址，
如果是在远程服务器上运行则必须配置，例如：listeners=PLAINTEXT:// 192.168.180.128:9092。并确保服务器的9092端口能够访问
zookeeper.connect 申明kafka所连接的zookeeper的地址 ，需配置为zookeeper的地址，由于本次使用的是kafka高版本中自带zookeeper，
使用默认配置即可 zookeeper.connect=localhost:2181
当我们有多个应用,在不同的应用中都使用zookeer,都使用默认的zk端口的话就会2181端口冲突,
我们可以设置自己的端口号,在config文件夹下zookeeper.properties文件中修改为clientPort=2185，也就是zk开放接口为2185.
同时修改kafka的接入端口,server.properties文件中修改为zookeeper.connect=localhost:2185，这样我们就成功修改了kafka里面的端口号



## 启动kafka:

启动zookeeper，zk默认端口是2181，启动是否成功可以通过打印出来的日志查看，默认是前台工作方式启动
sudo bin/zookeeper-server-start.sh config/zookeeper.properties

启动kafka
cd /home/lp/soft/kafka_2.11-1.1.0
sudo bin/kafka-server-start.sh config/server.properties


创建topic，有两种方式 如果用--zookeeper选项用的是locahost:2181，若是bootstrap-server则是localhost:9092
0.8 以前，消费进度是直接写到 zookeeper 的，consumer 必须知道 zookeeper 的地址。这个方案有性能问题，
0.9 的时候整体大改了一次，brokers 接管了消费进度，consumer 不再需要和 zookeeper 通信了。
一个topic可以支持多个consumer也支持多个producer，即一个producer多个consumer，多个producer一个consumer，
多个producer多个consumer。 replication-factor就是副本数，副本数要小于broker，如果单机部署那么设置replication-factor为3会启动失败。
若kafka没有启动运行命令会有提示
(1)bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic test
(2)bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic test

启动producer往指定的topic发送消息，对应的也有两种方式
(1)bin/kafka-console-producer.sh --broker-list localhost:9092 --topic test
(2)bin/kafka-console-producer.sh --bootstrap-server localhost:9092 --topic test

启动consumer接收指定topic的消息，可以有多个消费者消费同一个topic,数据被一个消费者消费之后并不会被清除，后面接进来的消费者可以接着从头消费，
当然也可以不从头而从接入的时间开始。而redis实现的pub/sub功能消费了就没了。 消费者中间退出没有任何影响,空行也是消息

bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test --from-beginning


清除kafka的数据是删除/tmp/kafka-logs目录下topic文件


