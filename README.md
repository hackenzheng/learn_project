## 介绍
   环境是Ubuntu16.04 
   
   
## 综合类

<从技术演变的角度看互联网后台架构 >  https://cloud.tencent.com/developer/article/1404117。
对后台架构的变化，技术的演进，各个技术的应用做了系统性的介绍


zk,mysql,redis, etcd,其实本质都是一样，都是一种组件，能提供的基本操作都是固定的。但是基于这些基本操作能做什么，就看开发者自己的使用。
有可能这个组件开发出来可能没有想到这个应用场景，但开发人员根据自己的业务需求结合这个组件恰好实现了，就拓宽了其应用。 有些通用的功能用的多了，就形成了共识，
比如zk一开始并不是做配置共享的，而是基本功能出来之后，很多应用都这么用，也觉得好用，就接着用了。比如redis的基本操作就是对key-val对的操作，基本的数据类型也就5类，
但可以基于redis做分布式锁，做分布式限流。

待处理的：

bigdata/es/data/
bigdata/hbase/deploy/hbase-deploy/
bigdata/hbase/deploy/hbase-kubernetes-master/
"bigdata/hbase/deploy/hbase\350\241\250\346\225\260\346\215\256/"
bigdata/zk/service_register_find/
bigdata/zk/zookeeper-deploy/
c_basic/daemonize.c
c_basic/gdb.md
c_basic/leetcode/isBalanced.py
c_basic/leetcode/isSymmetrical.cpp
c_basic/leetcode/mirror.cpp
k8s/yaml/dns-services.yaml
k8s/yaml/job.yaml
k8s/yaml/kubernetes-dashboard.yaml
k8s/yaml/namespace_mxnet.yaml
libevent/
machine_learning/mxnet.md
mxnet/
nginx/https_deploy/nginx.conf~
python/basic/logger.py
redis/key-value-server/CMakeLists.txt
redis/key-value-server/README.md
redis/key-value-server/client.cpp
redis/key-value-server/cmake-build-debug/
redis/key-value-server/hashtb.h
redis/key-value-server/makefile
redis/key-value-server/server.cpp
socket/linux_network_program2-master/
socket/python_thread/subprocess_dns.py
socket/sendfd.cpp
