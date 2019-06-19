## 缓存
数据库加载到缓存有多种方式，一种是操作MySQL的时候更新redis,及时性比较高，一种是设置定时任务，定时将数据同步到redis,业务代码简单，
不用考虑一致性的问题，但数据同步慢。


(一)缓存和数据库双写一致性问题: 先写缓存,再写数据库,类似分布式的不一致性问题, 做不到强一致,只能是最终一致性.        
(二)缓存雪崩问题: 缓存同一时间大面积的失效(过期时间差不多同一时间到)，这个时候又来了一波请求，结果请求都怼到数据库上，从而导致数据库连接异常
(三)缓存击穿问题:即黑客故意去请求缓存中不存在的数据，导致所有的请求都怼到数据库上，从而数据库连接异常    
(四)缓存的并发竞争问题 : 多个客户端写一个key
Redis3.0以后开始支持集群,这个集群是分布式而不是高可用 ,增删集群节点后会自动的进行数据迁移。
Redis 集群为了保证一致性（consistency）而牺牲了一部分容错性： 系统会在保证对网络断线和节点失效具有有限抵抗力的前提下，尽可能地保持数据的一致性。

先操作缓存，还是先操作数据库？
方法：
    
    （1）读请求，先读缓存，如果没有命中，读数据库，再set回缓存
    （2）写请求
        （2.1）先操作缓存，再数据库
        （2.2）缓存操作使用delete，而不是set
    该方法来自<究竟先操作缓存，还是数据库？> https://mp.weixin.qq.com/s?__biz=MjM5ODYxMDA5OQ==&mid=2651961341&idx=1&sn=e27916b8e96bd771c72c055f1f53e5be&chksm=bd2d02218a5a8b37ecffd78d20b65501645ac07c7ba2eb65b7e501a3eb9de023febe63bfdb36&scene=21#wechat_redirect
    
    该方法能解决数据库没有从节点时操作缓存的一致性问题，若有从库，仍然会存在缓存与数据库不一致的现象。而且如果淘汰调一批热点key,会造成缓存穿透。
    <缓存与数据库不一致，咋办？> https://mp.weixin.qq.com/s?__biz=MjM5ODYxMDA5OQ==&mid=2651961356&idx=1&sn=8fa6a57d128a3255a049bee868a7a917&chksm=bd2d0dd08a5a84c62c1ac1d90b9f4c11915c9e6780759d167da5343c43445759bce0f16de395&scene=21#wechat_redirect
    
    在其他文章中，写请求会先操作数据库再操作缓存，所以没有绝对的先操作数据库还是先操作缓存，具体的操作应该跟业务结合起来
    <Cache Aside Pattern> https://mp.weixin.qq.com/s?__biz=MjM5ODYxMDA5OQ==&mid=2651961349&idx=1&sn=59119a223f62d3740712ca0f62064f04&chksm=bd2d0dd98a5a84cf94d75e8e84ad7fe35fd040dfe02fe49db8dd64127c548aa194d2d169e149&scene=21#wechat_redirect
    
参考：
    
    <缓存，究竟是淘汰，还是修改？> https://mp.weixin.qq.com/s?__biz=MjM5ODYxMDA5OQ==&mid=2651961313&idx=1&sn=60d74fdbc1fb1dae696e0f4997c09f21&chksm=bd2d023d8a5a8b2bba2f8a3807492771a442495d27323d8dbfae670508fd0c46780308a9280d&scene=21#wechat_redirect
    <缓存相关的整体介绍> https://mp.weixin.qq.com/s?__biz=MjM5ODYxMDA5OQ==&mid=2651961368&idx=1&sn=82a59f41332e11a29c5759248bc1ba17&chksm=bd2d0dc48a5a84d293f5999760b994cee9b7e20e240c04d0ed442e139f84ebacf608d51f4342&scene=21#wechat_redirect




