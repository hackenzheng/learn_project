## 安装
   1. 在kafka中集成了zk,下载安装包之后直接启动
   2. 单独安装

## 使用
   连接zk: bin/zookeeper-shell.sh 127.0.0.1:2181，不支持命令补全，不支持上下历史命令查找.
   连接后的情况：比如在kafka中创建了topic: mytopic,test，可以在zk里面通过命令ls /brokers/topics列出来.
   操作类似于文件系统中的操作，每个path都是一个节点，都可通过get指令查看里面存储的信息，
   可通过create创建新节点比如create -s /config "001"。
   
   kafka在zk中保存的信息如下
   ![](./kafka-zk-level.png)
   
   zk上的操作
   ![](./zk_shell.bmp)
   

## 常用命令

    connect host:port
    get path [watch]
    ls path [watch]
    set path data [version]
    rmr path
    delquota [-n|-b] path
    quit 
    printwatches on|off
    create [-s] [-e] path data acl
    stat path [watch]
    close 
    ls2 path [watch]
    history 
    listquota path
    setAcl path acl
    getAcl path
    sync path
    redo cmdno
    addauth scheme auth
    delete path [version]
    setquota -n|-b val path
    
## zk功能与原理
zk本身使用副本模式解决了单点问题，并且解决主从架构下的分布式一致性问题，可以认为zk集群是可靠的，只要对外提供服务，那么就是可靠的。
client可以直接连接到zk集群的follower节点，也能连到leader节点，所看到的数据，执行的操作都是一样的。
主从节点的数据就是一致的。zk对外提供的服务是kv存储，类似于文件系统的存储，key是路径path，value是znode,文件节点，每个znode本身兼具文件和目录两种特点。
在这基础之上，还提供了自动编号节点，watcher机制. zk提供这些基本的服务，在具体的应用中，结合自己的业务，使用zk可以实现选主，服务发现，配置共享，分布式锁等功能。

1. 出现的原因及目标：

在分布式环境中，由于网络的不可靠，你对一个服务的调用失败了并不表示一定是失败的，可能是执行成功了，但是响应返回的时候失败了。
还有，A和B都去调用C服务，在时间上A还先调用一些，B后调用，那么最后的结果不一定A的请求就先于B到达。
分布式协调远比多个进程通信同步的调度要难，而且如果每一个分布式应用都开发一个独立的协调程序。
会出现反复编写浪费，且难以形成通用、伸缩性好的协调器。另一方面，协调程序开销比较大，会影响系统原有的性能。
所以，急需一种高可靠、高可用的通用协调机制来用以协调分布式应用。

2. 分布式锁的实现者：
分布式协调技术方面做得比较好的就是Google的Chubby还有Apache的ZooKeeper他们都是分布式锁的实现者。
既然有了Chubby为什么还要弄一个ZooKeeper，主要是Chbby是非开源的，Google自家用。
后来雅虎模仿Chubby开发出了ZooKeeper，也实现了类似的分布式锁的功能，并且将ZooKeeper作为一种开源的程序捐献给了Apache，
那么这样就可以使用ZooKeeper所提供锁服务。而且在分布式领域久经考验，它的可靠性，可用性都是经过理论和实践的验证的。

3. zk概述
它提供了一项基本服务：分布式锁服务。由于ZooKeeper的开源特性，后来在分布式锁的基础上，
摸索了出了其他的使用方法：配置维护、组服务、分布式消息队列、分布式通知/协调等。

zk使用zab协议,在实现这些服务时，首先它设计一种新的数据结构——Znode，然后在该数据结构的基础上定义了一些原语。
因为zk是工作在分布式的环境下，服务是通过消息以网络的形式发送给分布式应用程序，所以还需要一个通知机制——Watcher机制.

znode，兼具文件和目录两种特点。既像文件一样维护着数据、元信息、ACL、时间戳等数据结构，又像目录一样可以作为路径标识的一部分。每个Znode由3部分组成:
zk的服务器和客户端都被设计为严格检查并限制每个Znode的数据大小至多1M,因为配置文件信息、状态信息都是很小的数据。

    stat：此为状态信息, 描述该Znode的版本, 权限等信息
    
    data：与该Znode关联的数据
    
    children：该Znode下的子节点

节点分为临时节点和持久节点，该节点的生命周期依赖于创建它们的会话。一旦会话(Session)结束，临时节点将被自动删除，当然可以也可以手动删除。
另外又有顺序自动编号节点PERSISTENT_SEQUENTIAL，EPHEMERAL_SEQUENTIAL，这种目录节点会根据当前已近存在的节点数自动加 1

zk选主功能代替双机主备 https://www.cnblogs.com/wuxl360/p/5817471.html


配置管理：
一个应用系统有多台server，但某些配置项是相同的，如果要修改这些相同的配置项，那么就必须同时修改每台运行这个应用系统的Server，
这样非常麻烦而且容易出错。可用使用zk解决，将配置信息保存在 Zookeeper 的某个目录节点中，然后将所有共享这个配置的server监控配置信息的状态，
一旦配置信息发生变化，每台应用机器就会收到Zookeeper的通知，然后从 Zookeeper 获取新的配置信息应用到系统中。


分布式锁：
创建一个 EPHEMERAL_SEQUENTIAL(自动编号)目录节点，然后调用 getChildren方法获取当前的目录节点列表中最小的目录节点是不是就是自己创建的目录节点，
zk的每个操作都是原子的，但是有两步操作，那么就存在failed的情况。
如果正是自己创建的，那么它就获得了这个锁，如果不是那么它就调用 exists(String path, boolean watch) 方法并监控 Zookeeper 
上目录节点列表的变化，一直到自己创建的节点是列表中最小编号的目录节点，从而获得锁，释放锁很简单，只要删除前面它自己所创建的目录节点就行了。

集群管理leader election： 通过EPHEMERAL_SEQUENTIAL 目录节点

## zk数据存储
Zookeeper的数据模型是树结构，在内存数据库中，存储了整棵树的内容，包括所有的节点路径、节点数据、ACL信息，Zookeeper会定时将这个数据存储到磁盘上。
集群中的每个节点上的数据都是一样的，所以不能线性扩展，存储容量有限。但每个节点都能对外提供服务，所以并发性能是比较高的。

多个客户端同时创建同一个节点，会只有一个客户端创建成功。 这一特性可以用来实现分布式锁，选主等功能。
在zk中，事务是指能够改变zk服务器状态的操作。对每个事务请求，zk都会为其分配一个全局唯一的事务id,是顺序递增的。
所有的事务操作都会转到leader进行处理，从而保证事务处理的顺序性。 每个事务操作都会记录一条日志到事务日志文件中。

## zk集群状态
在服务启动阶段，会进行数据磁盘的恢复，然后进行leader选举。leader选举成功后进行集群间的数据同步(follower与leader进行同步)。整个启动过程中zk都处于不可用的状态。
    
    第一阶段：Leader election（选举阶段）
    最初时，所有节点都处于选举阶段，当其中一个节点得到了超过了半数节点的票数，它才能当选准Leader。只有达到第三阶段，准Leader才回变成实际的Leader。这一阶段Zookeeper使用的算法有Fast Leader Election。
    
    第二阶段：Discovery（发现阶段）
    这个阶段中，Followers和准Leader进行通信，同步Followers最近最近接收的事务提议。这一阶段的主要目的是发现当前大多数节点接受的最新提议，并让Followers接收准Leader定义的epoch（相当于朝代号，每一代Leader会有自己的epoch）。
    
    第三阶段：Synchronization（同步阶段）
    同步阶段主要是利用Leader前一阶段获得的最新提议历史，同步集群中的所有副本。只有当Quorum都同步完成，准Leader才回称为真的Leader。
    
    第四阶段：Broadcast（广播阶段）
    这个阶段Zookeeper才能够正式对外提供事务服务，并且Leader可以进行消息广播。


## zk的observer
observer除了不参与投票，其他功能与follower一样，在zk3.3版本之后加入的。
新增observer的目的是为了扩容读性能而不影响写性能。因为随着Follower节点数量的增加，ZooKeeper服务的写性能受到了影响。
写的过程需要follower参与投票，follower数目越多，投票耗时越长，性能余越低。

<ZooKeeper学习第八期——ZooKeeper伸缩性> http://www.cnblogs.com/sunddenly/p/4143306.html

## zk读写数据流程
写数据，一个客户端进行写数据请求时，如果是follower接收到写请求，就会把请求转发给Leader，Leader通过内部的Zab协议进行原子广播(类似2PC)，
zab协议实现了类似2pc协议，就是先选主， 有了主之后的事务操作的数据同步使用的是提案，实际就是2pc.
直到所有Zookeeper节点都成功写了数据后（内存同步以及磁盘更新），这次写请求算是完成，然后Zookeeper Service就会给Client发回响应。

读数据，因为集群中所有的Zookeeper节点都呈现一个同样的命名空间视图（就是结构数据），上面的写请求已经保证了写一次数据必须保证集群所有
的Zookeeper节点都是同步命名空间的，所以读的时候可以在任意一台Zookeeper节点上。


<咱们一起聊聊Zookeeper> https://juejin.im/post/5b03d58a6fb9a07a9e4d8f01

## 分布式锁的实现
MySQL数据库： 利用数据库的主键功能，不同节点插入同一条数据，插入成功的就拿到锁，用的数据库本身的锁。 并发不够高，有单点问题
redis: setnx key value指令，还能设置超时时间。 并发高，有可能导致锁泄露
zk: 多个客户端创建同一个节点，创建成功的拿到锁。 目前最常用的方式。

<分布式锁实现汇总> https://juejin.im/post/5a20cd8bf265da43163cdd9a

## zk在kafka中的作用
Kafka通过Zookeeper管理集群配置，选举leader,以及在consumer group发生变化时进行rebalance.
Kafka将元数据信息保存在Zookeeper中，但是发送给Topic本身的数据是不会发到Zk上的。
broker会在zookeeper注册并保持相关的元数据(如topic)更新。而客户端会在zookeeper上注册相关的watcher。
一旦zookeeper发生变化，客户端能及时感知并作出相应调整。
这样就保证了添加或去除broker时，各broker间仍能自动实现负载均衡。这里的客户端指的是Producer和Consumer。
Producer端使用zookeeper用来"发现"broker列表,以及和Topic下每个partition的leader建立socket连接并发送消息。
也就是说每个Topic的partition是由Lead角色的Broker端使用zookeeper来注册broker信息,
以及监测partition leader存活性.Consumer端使用zookeeper用来注册consumer信息,其中包括consumer消费的partition列表等,
同时也用来发现broker列表,并和partition leader建立socket连接,并获取消息.


<一篇文章深入浅出理解zookeeper> https://juejin.im/entry/5bf378e5f265da615f76e1ee
<使用Go基于zookeeper编写服务发现> https://juejin.im/post/5ab45e2751882510fd3f8d1e