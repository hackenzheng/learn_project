## 介绍
etcd是分布式高可用kv存储，键值对使用b+tree存储，使用raft协议，go编写，在k8s中用做配置共享，服务注册。
默认暴露给客户端的端口是2379，集群节点通信的端口是2380。每个节点都存储了完整的数据，并且通过Raft协议保证每个节点维护的数据是一致的.

etcd的操作类似redis,支持的类型不一样，单个value默认限制为1.5MB,整个存储限制默认是2GB，推荐用8GB。可以存储百万到千万级别的key.

ETCD提供HTTP协议，在最新版本中支持Google gRPC方式访问。具体支持接口情况如下：

    ETCD是一个高可靠的KV存储系统，支持PUT/GET/DELETE接口；
    为了支持服务注册与发现，支持WATCH接口（通过http long poll实现）；
    支持KEY持有TTL属性；
    CAS（compare and swap)操作;
    支持多key的事务操作；
    支持目录操作


## 安装使用

1. 单一节点安装
从github: https://github.com/etcd-io/etcd上下载编译好的安装包 
curl https://github.com/etcd-io/etcd/releases/download/v3.3.13/etcd-v3.3.13-linux-arm64.tar.gz
tar zxvf etcd-v3.3.13-linux-arm64.tar.gz -C /usr/local/bin/etcd
解压后会得到两个可执行文件etcd和etcdctl,etcd是服务端，etcdctl是客户端

启动服务端： etcd
客户端操作： etcd get mykey hello; etcd set mykey hello
API操作：
   curl http://127.0.0.1:2379/v2/keys     查看所有的key
   curl http://127.0.0.1:2379/v2/keys/hello -XPUT -d value="world"  创建key
   curl http://127.0.0.1:2379/v2/keys/dir -XPUT -d dir=true    创建目录
   curl http://127.0.0.1:2379/v2/keys/seqvar -XPOST -d value="seq1"  创建有序键值


etcd在键的组织上采用了层次化的空间结构(类似于文件系统中目录的概念)，用户指定的键可以为单独的名字，如testkey，此时实际上放在根目录/下面，
也可以为指定目录结构，如/test/k1，则是先创建目录test,再在test目录下创建k1. 

    etcdctl set /test/k1 hello
    etcdctl get /test    # 返回信息是/test: is a directory
    etcdctl get /test/k1  # 返回设置的值
    
2. 集群模式安装

https://github.com/etcd-io/etcd/blob/master/Documentation/demo.md


## etcd存储
etcd的key可以是任意字符串，所以仍旧可以模拟出目录，例如：key=/a/b/c。
在btreey中，key就是用户传入的原始key，而value并不是用户传入的value，当存储大量的K-V时，因为用户的value一般比较大，
全部放在内存btree里内存耗费过大，所以etcd将用户value保存在磁盘中。
简单的说，etcd是纯内存索引，数据在磁盘持久化，在磁盘上，etcd使用了一个叫做bbolt的纯K-V存储引擎（可以理解为leveldb），

<Etcd V3> https://blog.csdn.net/lingzhiwangcn/article/details/78958536 
