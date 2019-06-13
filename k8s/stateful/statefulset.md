## stateful set应用

stateful set解决的问题：单一容器就能启动不需要，即使需要数据持久化，需要数据持久化不代表就是有状态的应用。
那mongodb为例，如果是单例模式就直接启动，如果是副本集等模式就需要stateful set。

mongodb部署在k8s

    若一个容器挂了，并且被重新编排，数据丢失是不能接受的，通过volume来持久化。
    
    同一组MongoDB数据库备份节点之间需要通信，即使是在重编排之后。同一冗余备份集合的节点必须知道全部其他节点的地址，但是当某个容器重编排之后，它的IP地址会变化。
    例如，所有pod内的容器共享一个IP地址，当pod被重编排之后这个地址就会改变。在Kubernetes中，这个问题可以通过联系Kubernetes服务与MongoDB节点来解决，采用Kubernetes的DNS服务提供主机名给重编排之后的服务。
    
    一旦每个独立的MongoDB节点（每个节点在单独容器中）启动起来，备份集合必须初始化，并把每个节点加入进来。这可能需要编排工具之外的代码。具体而言，必须使用目标副本集群中的主MongoDB节点执行rs.initiate和rs.add命令。


需要通过stateful set部署的

    kubectl get statefulset -n cloudai-2
    NAME                   DESIRED   CURRENT   AGE
    airflow-worker         2         2         12d
    elasticsearch-data     2         2         12d
    elasticsearch-master   3         3         12d
    hadoop-hdfs-dn         3         3         12d
    hadoop-hdfs-nn         1         1         12d
    hadoop-yarn-nm         3         3         12d
    hadoop-yarn-rm         1         1         12d
    hbase-hbase-master     1         1         7d
    hbase-hbase-rs         3         3         7d
    redis-master           1         1         12d
    spark-worker           6         6         12d
    zookeeper              3         3         13d
    
    锁对应的svc
    kubectl get svc -n cloudai-2 
    NAME                         TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)                                                                              AGE
    airflow-flower               NodePort       10.43.135.168   <none>        5555:30444/TCP                                                                       12d
    airflow-web                  NodePort       10.43.57.196    <none>        8080:30445/TCP                                                                       12d
    airflow-worker               ClusterIP      None            <none>        8793/TCP                                                                             12d                                                           7d
    elasticsearch-client         NodePort       10.43.203.180   <none>        9200:31001/TCP                                                                       12d
    elasticsearch-discovery      ClusterIP      None            <none>        9300/TCP                                                                             12d
    glusterfs-cluster            ClusterIP      10.43.255.172   <none>        1990/TCP                                                                             13d
    hadoop-hdfs-dn               ClusterIP      None            <none>        9000/TCP,14000/TCP,50075/TCP                                                         12d
    hadoop-hdfs-nn               ClusterIP      10.43.23.211    <none>        9000/TCP,14000/TCP,50070/TCP                                                         12d
    hadoop-hdfs-nn-web           NodePort       10.43.34.43     <none>        9000:30010/TCP,14000:32366/TCP,50070:30011/TCP                                       12d
    hadoop-hive-service          NodePort       10.43.96.87     <none>        10000:30110/TCP,10002:30111/TCP,9083:30112/TCP                                       12d
    hadoop-yarn-nm               ClusterIP      None            <none>        8030/TCP,8031/TCP,8032/TCP,8033/TCP,8040/TCP,8042/TCP,8088/TCP,10020/TCP,19888/TCP   12d
    hadoop-yarn-rm               ClusterIP      None            <none>        8030/TCP,8031/TCP,8032/TCP,8033/TCP,8040/TCP,8042/TCP,8088/TCP,10020/TCP,19888/TCP   12d
    hbase-hbase-master           ClusterIP      None            <none>        16000/TCP,16010/TCP                                                                  12d
    hbase-hbase-rs               ClusterIP      None            <none>        16020/TCP,16030/TCP                                                                  12d
    hbase-master-service         LoadBalancer   10.43.6.168     <pending>     8080:32501/TCP,9090:30901/TCP,16000:30374/TCP,16010:30035/TCP                        12d
    hbase-thrift-service         LoadBalancer   10.43.122.177   <pending>     8080:30034/TCP,9090:30036/TCP                                                        12d
    hue-server                   NodePort       10.43.186.59    <none>        8888:30130/TCP                                                                       12d
    mysql-service                NodePort       10.43.170.134   <none>        3306:32003/TCP                                                                       12d
    postgres                     NodePort       10.43.205.156   <none>        5432:30432/TCP                                                                       3h
    presto-coordinator-service   NodePort       10.43.242.36    <none>        8080:30890/TCP                                                                       12d
    presto-exporter              ClusterIP      10.43.62.78     <none>        9483/TCP                                                                             12d
    redis-master                 ClusterIP      10.43.136.28    <none>        6379/TCP                                                                             12d
    redis-metrics                ClusterIP      10.43.157.178   <none>        9121/TCP                                                                             12d
    redis-slave                  ClusterIP      10.43.98.13     <none>        6379/TCP                                                                             12d
    spark-history                NodePort       10.43.54.54     <none>        18080:31203/TCP                                                                      12d
    spark-master                 NodePort       10.43.177.156   <none>        7077:31202/TCP,8080:31201/TCP                                                        12d
    spark-worker0-service        NodePort       10.43.159.151   <none>        8080:31110/TCP                                                                       12d
    spark-worker1-service        NodePort       10.43.217.191   <none>        8080:31111/TCP                                                                       12d
    spark-worker2-service        NodePort       10.43.186.89    <none>        8080:31112/TCP                                                                       12d
    zookeeper                    ClusterIP      10.43.217.59    <none>        2181/TCP                                                                             13d
    zookeeper-headless           ClusterIP      None            <none>        2181/TCP,3888/TCP,2888/TCP                                                           13d
    
    所对应的deploy
    kubectl get deployment -n cloudai-2 
    NAME                       DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
    airflow-flower             1         1         1            1           12d
    airflow-scheduler          1         1         1            1           12d
    airflow-web                1         1         1            1           12d
    elasticsearch-client       2         2         2            2           12d
    hadoop-hive                2         2         2            2           12d
    hbase-hbase-thrift         3         3         3            3           7d
    hue-server                 1         1         1            1           12d
    mysql                      1         1         1            1           12d
    postgres                   1         1         1            1           3h
    presto-coordinator         1         1         1            1           12d
    presto-exporter            1         1         1            1           12d
    presto-worker              2         2         2            2           12d
    redis-metrics              1         1         1            1           12d
    redis-slave                3         3         3            3           12d
    spark-history              1         1         1            1           12d
    spark-master               1         1         1            1           12d

    
    
    所对应的pod 
    kubectl get pods -n cloudai-2
    NAME                                        READY     STATUS    RESTARTS   AGE
    airflow-flower-7b8999645b-7b54q             1/1       Running   4          12d
    airflow-scheduler-6ddb554769-vq5rm          1/1       Running   4          12d
    airflow-web-6c59bff8c7-xmccd                1/1       Running   4          12d
    airflow-worker-0                            1/1       Running   1          7d
    airflow-worker-1                            1/1       Running   1          7d
    elasticsearch-client-67bb5758c-2hklj        1/1       Running   5          12d
    elasticsearch-client-67bb5758c-tlxr9        1/1       Running   5          12d
    elasticsearch-data-0                        1/1       Running   2          12d
    elasticsearch-data-1                        1/1       Running   2          12d
    elasticsearch-master-0                      1/1       Running   2          12d
    elasticsearch-master-1                      1/1       Running   2          12d
    elasticsearch-master-2                      1/1       Running   2          12d
    hadoop-hdfs-dn-0                            1/1       Running   10         12d
    hadoop-hdfs-dn-1                            1/1       Running   11         12d
    hadoop-hdfs-dn-2                            1/1       Running   10         12d
    hadoop-hdfs-nn-0                            1/1       Running   2          12d
    hadoop-hive-9cc465696-4w7zb                 1/1       Running   2          12d
    hadoop-hive-9cc465696-scfbz                 1/1       Running   3          12d
    hadoop-yarn-nm-0                            1/1       Running   7          12d
    hadoop-yarn-nm-1                            1/1       Running   7          12d
    hadoop-yarn-nm-2                            1/1       Running   7          12d
    hadoop-yarn-rm-0                            1/1       Running   2          12d
    hbase-hbase-master-0                        1/1       Running   0          1d
    hbase-hbase-rs-0                            1/1       Running   6          7d
    hbase-hbase-rs-1                            1/1       Running   7          7d
    hbase-hbase-rs-2                            1/1       Running   6          7d
    hbase-hbase-thrift-b5f96c978-dnc7d          1/1       Running   2          7d
    hbase-hbase-thrift-b5f96c978-mprxs          1/1       Running   2          7d
    hbase-hbase-thrift-b5f96c978-x89d6          1/1       Running   1          7d
    hue-server-ccbd8bdc9-dlsd9                  1/1       Running   10         12d
    mysql-7978df9544-cszgd                      1/1       Running   2          12d
    postgres-5454bcd7b4-pnwxh                   1/1       Running   0          3h
    presto-coordinator-5bfc984ff9-dj8cf         1/1       Running   9          12d
    presto-exporter-698458b98c-wfvbf            1/1       Running   12         12d
    presto-worker-67645c76d5-5f7mb              1/1       Running   5          12d
    presto-worker-67645c76d5-fwnrg              1/1       Running   4          12d
    redis-master-0                              1/1       Running   3          12d
    redis-metrics-7778f9b7db-pkrwx              1/1       Running   3          12d
    redis-slave-7c7fb9c4d6-4vwdl                1/1       Running   6          12d
    redis-slave-7c7fb9c4d6-95dc4                1/1       Running   7          12d
    redis-slave-7c7fb9c4d6-r7g8l                1/1       Running   5          12d
    spark-history-7d84558888-lxvqg              1/1       Running   2          12d
    spark-master-7c5c5c5878-j8vn2               1/1       Running   3          12d
    spark-worker-0                              1/1       Running   2          12d
    spark-worker-1                              1/1       Running   2          12d
    spark-worker-2                              1/1       Running   3          12d
    spark-worker-3                              1/1       Running   2          12d
    spark-worker-4                              1/1       Running   3          12d
    spark-worker-5                              1/1       Running   2          12d
    zookeeper-0                                 1/1       Running   2          7d
    zookeeper-1                                 1/1       Running   1          7d
    zookeeper-2                                 1/1       Running   1          7d
    