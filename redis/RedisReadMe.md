## 缓存
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


## 一致性哈希
在分布式集群中，要有足够的容错(节点故障)和扩容(新增节点)能力，无状态的服务天然支持，而对于有状态的服务比如数据库和缓存redis等，
在分区存储的情况下首先保证同一个数据映射到同一台服务器，一般用hash取模，在这之上很好的支持容错和扩容，就要一致性哈希。

在nginx的配置中的负载均衡策略也有一致性哈希，因为服务器随时都有可能增减，通过hash $consitent_key来指定。

一致性哈希是将整个哈希值空间组织成一个虚拟的圆环，圆环的大小一般是2的n次方，实现的时候就用一个数组就可以。首先对服务器(ip或name)取hash确定在环
的位置上，数据过来用同样的hash函数取hash值，根据hash值落到顺时针方向第一个服务器上。这样解决了扩容时对所有数据重新hash的问题，只需要对一个节点上的数据重hash.

但还存在数据倾斜的问题，于是又引入了虚拟节点。

<一致性哈希算法及其在分布式系统中的应用> http://blog.codinglabs.org/articles/consistent-hashing.html
<一致性哈希的Java实现> https://github.com/crossoverJie/JCSprout/blob/master/docs/algorithm/consistent-hash-implement.md


## redis cluster中的分区方法
redis cluster是官方推出的去中心化的集群方案，每个节点存储一部分数据，数据划分通过手动预分桶(slot)的方式，总共是16384个桶。
预分桶的方案介于“硬Hash”和“一致性Hash”之间，牺牲了一定的灵活性，但相比“一致性Hash“，数据的管理成本大大降低

客户端与redis节点直连,不需要中间proxy层.客户端不需要连接集群所有节点,连接集群中任何一个可用节点即可

在redis cluster出来之前如果要用redis的分布式集群方式需要自行实现一致性哈希，既可以在客户端实现，也可以在中间件上实现，使用中间件比较好，
比如twitter的twemproxy,以及开源的codis.

<redis集群方案-一致性hash算法> https://blog.csdn.net/u014490157/article/details/52244378
<Redis分布式部署，一致性hash> https://www.cnblogs.com/taosim/articles/4238674.html

## 布隆过滤器
用于判断一个元素在不在库里面，如果判断结果不在库里面那就一定不在，如果在库里面，有一定的错误率是不在的。
判断一个元素在不在最直接的方式使用hash,但如果数据量比较大，使用hash很耗存储，所以使用布隆过滤器，用一定的误报率换取存储空间。

edis 在 4.0 的版本中加入了 module 功能，布隆过滤器可以通过 module 的形式添加到 redis 中，所以使用 redis 4.0 以上的版本
可以通过加载 module 来使用 redis 中的布隆过滤器。但是这不是最简单的方式，使用 docker 可以直接在 redis 中体验布隆过滤器。

    > docker run -d -p 6379:6379 --name bloomfilter redislabs/rebloom
    > docker exec -it bloomfilter redis-cli
    
redis 布隆过滤器主要就两个命令：

    bf.add 添加元素到布隆过滤器中：bf.add urls https://jaychen.cc。
    bf.exists 判断某个元素是否在过滤器中：bf.exists urls https://jaychen.cc。

上面说过布隆过滤器存在误判的情况，在 redis 中有两个值决定布隆过滤器的准确率：

    error_rate：允许布隆过滤器的错误率，这个值越低过滤器的位数组的大小越大，占用空间也就越大。
    initial_size：布隆过滤器可以储存的元素个数，当实际存储的元素个数超过这个值之后，过滤器的准确率会下降。

redis 中有一个命令可以来设置这两个值：

    bf.reserve urls 0.01 100
    复制代码三个参数的含义：
    
    第一个值是过滤器的名字。
    第二个值为 error_rate 的值。
    第三个值为 initial_size 的值。

另外可以基于redis的bitmap实现布隆过滤器，而不是直接使用redis的布隆过滤器