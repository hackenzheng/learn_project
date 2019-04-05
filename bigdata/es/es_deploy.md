## es单机测试环境部署
从官网下载编译好的二进制安装包https://www.elastic.co/downloads/elasticsearch， 选择Linux版本，格式为tar.gz.
解压到/usr/local/目录下，配置文件为config/elasticsearch.yml.　ElasticSearch所有的操作都可通过Rest API完成,例如增删改查。

启动：

       /usr/local/elasticsearch/bin/elasticsearch     # 前台启动
       /usr/local/elasticsearch/bin/elasticsearch -d  #　后台启动

索引操作：

    curl http://localhost:9200/_cat/indices?v　　#初始状态是没有索引的
    curl -XPUT http://localhost:9200/customer　　# 创建索引，默认5个主分片１个副本
    curl localhost:9200/_cat/indices?v          #列出所有索引
    curl localhost:9200/customer/_search?q=*&pretty   # 查询索引customer下所有数据

文档操作：为了索引一个文档，必须告诉es这个文档要到索引的哪个类型

    下面这条命令是将一个简单的客户文档索引到customer索引、“external”类型中，指定文档的ID是1。新增记录的时候，也可以不用指定id，但是得改成POST请求，生成的id为一个随机字符串
    curl -H "Content-Type: application/json" -XPUT 'http://localhost:9200/customer/external/1' -d '{"name": "John Doe"}'
    
    查看刚才添加的文档, pretty是以可视化的json输出，不加是字符串输出
    curl -XGET http://localhost:9200/customer/external/1?pretty
    
    修改之前的文档，因为指定id相同，原来的文档会被覆盖，再次查找只会有age字段，而不是name和age
    curl -H "Content-Type: application/json" -XPUT 'http://localhost:9200/customer/external/1' -d '{"age": 10}'

检索：

      查询name字段含有Doe的记录
      curl -H "Content-Type: application/json" -XPOST http://localhost:9200/customer/_search?pretty -d '{"query":{"match": {"name": "Doe"}}}'
  

映射：
   
      curl localhost:9200/customer/_mapping?pretty
      自动根据提交的文档创建映射
      {
        "customer" : {      # 索引名
          "mappings" : {
            "external" : {  # type名
              "properties" : {
                "name" : {      # filed
                  "type" : "text",
                  "fields" : {
                    "keyword" : {
                      "type" : "keyword",
                      "ignore_above" : 256
                    }
                  }
                }
              }
            }
          }
        }
      }
    
    映射就是模式定义，比如有支持哪些字段，字段是什么类型，当然字段可以自动扩充。但如果新的数据与已有的类型冲突，会添加文档失败。
    比如：第一个命令会添加成功，并设置age类型为整型，但第二个数据是字符型，类型冲突。 
    curl -H "Content-Type: application/json" -XPUT 'http://localhost:9200/customer/external/1' -d '{"age": 10}'
    curl -H "Content-Type: application/json" -XPUT 'http://localhost:9200/customer/external/2' -d '{"age": "sz"}'
    
    在同一个index的不同type下，有相同的filed但是类型不一样也会报错，如果类型相同是可以的。比如下面两个，type分别是external和internal，因为映射最终都会展开在一个index下面。
    curl -H "Content-Type: application/json" -XPUT 'http://localhost:9200/customer/external/3' -d '{"age": 10}'
    curl -H "Content-Type: application/json" -XPUT 'http://localhost:9200/customer/internal/4' -d '{"age": "sz"}'
        
## 概念介绍
  Elasticsearch是一个基于Lucene的搜索和数据分析工具，它提供了一个分布式服务，会自动为提交的文档创建索引，索引通常比源数据大10%，es的磁盘大小源数据大小和副本数有关。
  
    cluster
    代表一个集群，集群中有多个节点，其中有一个为主节点，这个主节点是可以通过选举产生的，主从节点是对于集群内部来说的。Elasticsearch的一个概念就是去中心化，字面上理解就是无中心节点，这是对于集群外部来说的，因为从外部来看Elasticsearch集群，在逻辑上是个整体，你与任何一个节点的通信和与整个Elasticsearch集群通信是等价的。
    
    shards
    索引分片，es可以把一个完整的索引分成多个分片，这样的好处索引分布到不同的节点上，构成分布式搜索，在数据量很大的时候，进行水平的扩展，提高搜索性能。分片的数量只能在索引创建前指定，并且索引创建后不能更改。
    
    replicas
    索引副本，副本的作用一是提高系统的容错性，当某个节点某个分片损坏或丢失时可以从副本中恢复。二是提高查询效率，es会自动对搜索请求进行负载均衡。
    
    recovery
    数据恢复或叫数据重新分布，Elasticsearch在有节点加入或退出时会根据机器的负载对索引分片进行重新分配，挂掉的节点重新启动时也会进行数据恢复。
    
    gateway
    Elasticsearch索引快照的存储方式，Elasticsearch默认是先把索引存放到内存中，当内存满了时再持久化到本地硬盘。gateway对索引快照进行存储，当这个Elasticsearch集群关闭再重新启动时就会从gateway中读取索引备份数据。Elasticsearch支持多种类型的gateway，有本地文件系统（默认）、分布式文件系统、Hadoop的HDFS和阿里云的OSS云存储服务。
    
    discovery.zen
    Elasticsearch的自动发现节点机制，Elasticsearch是一个基于p2p的系统，它先通过广播寻找存在的节点，再通过多播协议来进行节点之间的通信，同时也支持点对点的交互。
    
    Transport
    Elasticsearch内部节点或集群与客户端的交互方式，默认内部是使用tcp协议进行交互，同时它支持http协议（json格式）、thrift、servlet、memcached、zeroMQ等的传输协议（通过插件方式集成）。

    Index: 一系列文档的集合，类似于mysql中数据库的概念
    Type: 在Index里面可以定义不同的type，type的概念类似于mysql中表的概念，是一系列具有相同特征数据的结合。
    Document: 文档的概念类似于mysql中的一条存储记录，并且为json格式，在Index下的不同type下，可以有许多document。
    
    映射：描述了文档可能具有的字段或属性，每个字段的数据类型—比如string, integer或date，以及Lucene是如何索引和存储这些字段的。
    
    编程过程：建立索引对象 --- 建立映射 ---  存储数据[文档] --- 指定文档类型进行搜索数据[文档]
    
https://www.jianshu.com/p/6333940621ec

_index, _type和_id的组合唯一标识一个文档,可以提供自定义的 _id值，或者让index API自动生成。自动生成的ID是URL-safe、基于Base64编码且长度为20个字符的GUID字符串。


<es权威指南>https://www.elastic.co/guide/cn/elasticsearch/guide/current/index.html

给索引添加文档

    url格式为 PUT /{index}/{type}/{id}，
    PUT /website/blog/123
    {
      "title": "My first blog entry",
      "text":  "Just trying this out...",
      "date":  "2014/01/01"
    }

对应的响应：

    {
       "_index":    "website",
       "_type":     "blog",
       "_id":       "123",
       "_version":  1,
       "created":   true
    }

在 Elasticsearch 中每个文档都有一个版本号。当每次对文档进行修改时（包括删除）_version 的值会递增

可以将一个JSON文档扔到es里，然后根据ID检索。但es真正强大之处在于可以从无规律的数据中找出有意义的信息。
es不只会存储文档，为了能被搜索到也会为文档添加索引,这也是为什么我们使用结构化的 JSON 文档，而不是无结构的二进制数据。

一个type下有多个document，每个document可以是完全不同的字段，每个字段的所有数据都是默认被索引的。
type类似于table，所以就有对应的模式定义即映射(mapping),映射定义了类型中的域(field)，每个域的数据类型，以及es如何处理这些域。
es会默认自动根据document创建mapping,但仍需要为单独域自定义映射，特别是字符串域。自定义映射允许的操作有：全文字符串域和精确值字符串域的区别;使用特定语言分析器比如中文和英文等。 
