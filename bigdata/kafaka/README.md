## 整体介绍

kafka中的message以topic的形式存在，topic在物理上又分为很多的partition，每个partion就是一个目录，
partition物理上由很多segment(具体的文件)组成，segment是存放message的真正载体。segment file组成：由2大部分组成，
分别为index file和data file，此2个文件一一对应，成对出现，后缀”.index”和“.log”分别表示为segment索引文件、数据文件.

对于传统的mq而言，一般会删除已经被消费的消息，而Kafka会保留所有的消息，无论其被消费与否。当然，因为磁盘限制，不可能永久保留所有数据（实际上也没必要），
因此Kafka提供两种策略删除旧数据。一是基于时间，二是基于Partition文件大小，在server.properties中设置

一个消费者可以订阅多个topic

整体架构

![](./KafkaStructure.png)

Kafka的设计理念之一就是同时提供离线处理和实时处理。根据这一特性，可以使用Storm这种实时流处理系统对消息进行实时在线处理，
同时使用Hadoop这种批处理系统进行离线处理，还可以同时将数据实时备份到另一个数据中心，只需要保证这三个操作所使用的Consumer属于不同的Consumer Group即可

### 主要概念

Broker：Kafka 集群包含一个或多个服务器，一个服务器被称为broker，解压之后默认启动是单机即单个broker.

Topic：每条发布到 Kafka 集群的消息都有一个类别，这个类别被称为 Topic。（物理上不同 Topic 的消息分开存储，
逻辑上一个 Topic 的消息虽然保存于一个或多个 broker 上，但用户只需指定消息的 Topic 即可生产或消费数据而不必关心数据存于何处）。
每个Topic分为多个分区，这样的设计有利于管理数据和负载均衡。

Partition：Partition 是物理上的概念，每个partition是一个有序的队列,每个 Topic 包含一个或多个 Partition，partion可以在不同的服务器上
创建一个topic时，同时可以指定分区数目，分区数越多，其吞吐量也越大，但是需要的资源也越多，
同时也会导致更高的不可用性，kafka在接收到生产者发送的消息之后，会根据均衡策略将消息存储到不同的分区中。消费者读取消息不会区分partion,只要topic
生产者在向kafka集群发送消息的时候，可以通过指定分区来发送到指定的分区中，也可以通过指定均衡策略来将消息发送到不同的分区中，如果不指定，
就会采用默认的随机均衡策略，将消息随机的存储到不同的分区中。所有消息可以均匀分布到不同的Partition里，这样就实现了负载均衡。如果一个Topic对应一个文件，
那这个文件所在的机器I/O将会成为这个Topic的性能瓶颈，而有了Partition后，不同的消息可以并行写入不同broker的不同Partition里，极大的提高了吞吐率。
在发送一条消息时，可以指定这条消息的key，Producer根据这个key和Partition机制来判断应该将这条消息发送到哪个Parition，Paritition机制可以设置

Segment：如果就以partition为最小存储单位，我们可以想象当Kafka producer不断发送消息，必然会引起partition文件的无限扩张，
这样对于消息文件的维护以及已经被消费的消息的清理带来严重的影响，所以这里以segment为单位又将partition细分。
每个partition(目录)相当于一个巨型文件被平均分配到多个大小相等的segment(段)数据文件中（每个segment
文件中消息数量不一定相等）这种特性也方便old segment的删除，即方便已被消费的消息的清理，提高磁盘的利用率。
每个partition只需要支持顺序读写就行，segment的文件生命周期由服务端配置参数（log.segment.bytes，log.roll.{ms,hours}等若干参数）决定。

offset：每个partition都由一系列有序的、不可变的消息组成，这些消息被连续的追加到partition中.
partition中的每个消息都有一个连续的序列号叫做offset,用于partition唯一标识一条消息.

Producer：负责发布消息到 Kafka broker。

Consumer：消息消费者，向 Kafka broker读取消息的客户端。

Consumer Group：多个consumer可以组成一个group，每个Consumer只能属于一个特定的Consumer Group，默认是不同的group，也可指定group name。
可以有多个不同的group来同时消费同一个topic下的消息，他们的的消费的offset各不项目，不互相干扰。
对于一个group而言，消费者的数量不应该多余分区的数量，因为在一个group中，每个分区至多只能绑定到一个消费者上，即一个消费者可以消费多个分区，一个分区只能给一个消费者消费。
那这样一个组下面的不同consumer只能读到一部分message，加起来才是整个的，即同一Topic的一条消息只能被同一个Consumer Group内的一个Consumer消费，但多个Consumer Group可同时消费这一消息。
若一个group中的消费者数量大于分区数量的话，多余的消费者将不会收到任何消息。用于那种能够水平扩容且只要消费一次的场景。

主要有3种发送消息的方法：

    立即发送：只管发送消息到server端，不care消息是否成功发送。大部分情况下，这种发送方式会成功，因为Kafka自身具有高可用性，producer会自动重试；但有时也会丢失消息；

    同步发送：通过send()方法发送消息，并返回Future对象。get()方法会等待Future对象，看send()方法是否成功；

    异步发送：通过带有回调函数的send()方法发送消息，当producer收到Kafka broker的response会触发回调函数


通常一个producer起一个线程开始发送消息。为了优化producer的性能，一般会有下面几种方式：
单个producer起多个线程发送消息；使用多个producer。


kafka的消费模式总共有3种：最多一次，最少一次，正好一次。为什么会有这3种模式，是因为consumer处理消息，提交反馈这两个动作不是原子性。
消费模式在服务端的配置文件中配置。 producer发送数据也有这三种模式

    1.最多一次：客户端收到消息后，在处理消息前自动提交，这样kafka就认为consumer已经消费过了，偏移量增加。 
    2.最少一次：客户端收到消息，处理消息，再提交反馈。这样就可能出现消息处理完了，在提交反馈前，网络中断或者程序挂了，那么kafka认为这个消息还没有被consumer消费，产生重复消息推送。
    3.正好一次：保证消息处理和提交反馈在同一个事务中，即有原子性。

Kafka的高可靠性通过副本（replication）策略实现。Kafka从0.8.x版本开始提供partition级别的复制,replication的数量可以在server.properties中配置
Kafka给多个Replication设置了一个Leader，其他副本叫做follower，Producer发送消息时，只发送给Leader，follower再从leader复制消息，
既不是同步复制，也不是完全的异步复制，Kafka的Leader会看哪些follower的数据与自己是同步的，将其视为好同志，重点培养，放入一个列表，称为ISR，
所以Kafka是采用了同步和完全异步的折中方式，让一部分高效的follower同步，让其他follower异步

但如果不幸ISR列表中的follower都不行了，就只能从其他follower中选取，这时就有数据丢失的可能了，因为不确定这个follower是否已经把leader的数据都复制完成了

基本使用：https://blog.csdn.net/luanpeng825485697/article/details/81036028

kafka数据可靠性深度解读 ：https://mp.weixin.qq.com/s?__biz=MzU1NDA4NjU2MA==&mid=2247486245&amp;idx=1&amp;sn=a6ecb1026b6ef24cabe10ef9a4b7570d&source=41#wechat_redirect


### 消息重复和丢失
   重复的原因：
      (1) 重复发送：生产发送的消息没有收到正确的broker响应，导致producer重试。
      (2) 重复消费：数据消费完没有及时提交offset到broker。
   丢失的原因： 
      (1) producer发送消息完，不管结果了，如果发送失败也就丢失了。
      (2) producer发送消息完，只等待lead写入成功就返回了，leader crash了，这时follower没来及同步，消息丢失。
      
      
参考： https://www.cnblogs.com/wangzhuxing/p/10124308.html

消息队列应用场景
https://blog.csdn.net/dj2008/article/details/78872889