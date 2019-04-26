
## hbase介绍
  hbase是nosql一种，底层是k-v存储实现的列式数据库，原生不支持sql语句，需要转换。mysql中空字段是要占据存储空间的，
  因为要先定义好schema，并且按行存储，一行的数据存储在一起。而hbase将属于同一列簇的存储在一起。这种存储方式使得hbase方便用于稀疏数据的存储，
  空字段不占空间，以及能够很好的拓展到上百万列，查询某一列不需要全表扫描。查询一行的数据也比较快，因为属于同一个列簇的存放在一起，
  hbase不推荐使用多个列簇。而mysql中的列一多就会影响性能，往往需要分表，然后通过联表查询。

  hbase应用场景：hbase是大数据组件之一，是在数据量大的时候也不慢，但是数据量少的时候并不是特别快。支持百万级别高并发写入，因为直接与client端通信。
  hbase不支持事务，适用于OLAP场景，而mysql等适用OLTP场景。

## hbase原理与架构
   架构图：
   ![](./hbase.jpg)
   
   其中的hmaster节点不同于hdfs中的namenode，不需要hmaster提供元数据信息，元数据存储在zk里面.hmaster主要是维护regionserver.
   hbase底层存储用到的hdfs,hdfs存储小文件效率不高，以及不支持读写，支持追加。所以hbase的修改删除都是基于追加的方式，旧的数据仍然会在，并指定一个版本或timestamp，
   取的时候默认取最新的数据。
    
   Region是hbase在rowkey上的切分，每个Region都可以通过startKey和endKey来确定rowkey的范围，一个HRegionServer上可能会有多个Region。
   说数据是根据rowkey和一定的哈希规则，分散到不同的Region上面
   
   hbase会先把数据存到内存，内存满了之后刷写到磁盘，然后再定期对小文件合并为大文件。

   hbase写入流程： HMaster会对拆分后的Region重新分配RegionServer，这是HMaster的负载均衡策略
   
         1、hbase client要写输入了，先从zookeeper中拿到meta表信息，根据数据的rowkey找到应该往哪个RegionServer写
         
         2、然后hbase会将数据写入对应RegionServer的内存MemStore中，同时记录操作日志WAL
         
         3、当MemStore超过一定阈值，就会将内存MemStore中的数据刷写到硬盘上，形成StoreFile
         
         4、在触发了一定条件的时候，小的StoreFile会进行合并，变成大的StoreFile，有利于hdfs存储

   hbase读取流程：
   
       1、hbase client要读数据了，先从zookeeper中拿到meta表信息，根据要查的rowkey找到对应的数据在哪些RegionServer上
       
       2、分别在这些RegionServer上根据列簇进行StoreFile和MemStore的查找，得到很多key-value结构的数据
       
       3、根据数据的版本找到最新数据进行返回

   hbase内部使用LSM三层模型进行存储，数据先写到内存MemStore中，内存达到一定阈值再刷写到硬盘StoreFile中，再满足一定条件时，小的StoreFile会合并为大的StoreFile

## hbase使用

   rowkey设计：简短，hbase的查询通过对rowkey建索引实现，所以把要查询的字段设置在rowkey中。 另外可以对rowkey设置filter。
   rowkey设计的另一个原则，就是散列性，rowkey的头几个字母，最好不要是一样的，不然会分布在同一个HRegionServer上面，导致这个HRegionServer的负载非常高，
   一般可以根据一定规则算一个数据的摘要，比如md5，把md5的头几位拼在rowkey的前面。
   
   列簇的设计：列簇是在建表的时候定义好，最多两个，列可以随时添加


参考： https://mp.weixin.qq.com/s/r_ouxFJ4FajyDl835iEcBQ
