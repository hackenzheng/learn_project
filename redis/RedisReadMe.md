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


## redis存储中文
set chinese 中国 将编码成*3\r\n$3\r\nSET\r\n$7\r\nchinese\r\n$6\r\n\xe4\xb8\xad\xe5\x9b\xbd\r\n，
汉字中国的按照utf-8编码的方式编码成bytes为*\xe4\xb8\xad\xe5\x9b\xbd，一个汉字三个字节，因此中国的长度是6。
get chinese返回的也是"中国"的utf-8编码。

执行上述命令的过程中，使用sudo tcpdump -i any port 6379 -vv 抓包可以看到传输的内容， 英文字符都能直接看到，而中文字符看起来是乱码。