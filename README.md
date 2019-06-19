## 介绍
   环境是Ubuntu16.04 
   
   
## 综合类

<从技术演变的角度看互联网后台架构 >  https://cloud.tencent.com/developer/article/1404117。
对后台架构的变化，技术的演进，各个技术的应用做了系统性的介绍


zk,mysql,redis, etcd,其实本质都是一样，都是一种组件，能提供的基本操作都是固定的。但是基于这些基本操作能做什么，就看开发者自己的使用。
有可能这个组件开发出来可能没有想到这个应用场景，但开发人员根据自己的业务需求结合这个组件恰好实现了，就拓宽了其应用。 有些通用的功能用的多了，就形成了共识，
比如zk一开始并不是做配置共享的，而是基本功能出来之后，很多应用都这么用，也觉得好用，就接着用了。比如redis的基本操作就是对key-val对的操作，基本的数据类型也就5类，
但可以基于redis做分布式锁，做分布式限流。

用Python基于redis实现分布式锁，分布式限流   https://github.com/rfyiamcool/redis_netlock/blob/master/redis_netlock/__init__.py
c或python实现一致性哈希， 增加虚拟节点怎么会保证分布均匀？
限流漏斗算法的实现
限流令牌桶的实现， 为什么能够应对突发流量？  平滑模式，突发模式
c语言实现用读写文件的方式拷贝一个文件到另外一个文件
模拟下建立连接后fork进程，同时读取看有什么现象
go客户端协程传输文件 或者多线程传输
socket传递结构体数据 https://blog.csdn.net/ikerpeng/article/details/38387171
socket传输字符串，本质传的是二进制，然后读取的时候自动按字节进行asscii编码，那么传数字了


待处理的：

bigdata/hbase/deploy/hbase-deploy/
bigdata/hbase/deploy/hbase-kubernetes-master/
"bigdata/hbase/deploy/hbase\350\241\250\346\225\260\346\215\256/"
bigdata/zk/zookeeper-deploy/
mxnet/mxnet_learn/Attribute_Multitask/
mxnet/mxnet_learn/evaluation.py
mxnet/mxnet_learn/gender/
mxnet/mxnet_learn/mxnet_office/
mxnet/mxnet_learn/mxnet_official_learn/
mxnet/mxnet_learn/resnet_train/
socket/linux_network_program2-master/
