## 分布式一致性协议
出现背景：分布式一致性协议是在分布式系统出现之后才提出来的，90年代开始，互联网公司大量出现，原来的单体应用不能满足需求。
分布式系统给一致性问题带来了巨大的挑战, 理想情况下的一致性模型在分布式系统中几乎无法实现, 不得不设计应用于不同场景的各种一致性模型。


一致性问题就是相互独立的节点之间如何达成一项决议的问题。分布式系统中，进行数据库事务提交(commit transaction)、Leader选举、序列号生成等都会遇到一致性问题
分布式一致性不仅仅两个节点最终对一个值的结果一致, 还需要对这个值的修改过程也要一致，这样外界任何时候访问任何节点，看到的才是一致的。

发展历史：
重要的节点：1978年提出的Lamport Clock对分布式系统的启发, 1979年提出的Sequential Consistency和1987年提出的最重要的一致性模型Linearizability.
1990年Lamport提出的Paxos是第一个正确实现适用于分布式系统的Consensus(一致性)算法. Paxos算法有很多缺点，实现也很复杂，但是分布式一致性问题解决的基础，zk用到的
zab协议就是在这之上实现的。raft近似是Paxos的一个简化版本，是chubby的开源实现。


## 应用
主从架构也是分布式系统。像MySQL只通过binlog日志进行数据同步，会有延时，只要写主成功就是成功，不管从节点状态怎么样，一致性是比较差的。
但是mongodb是可以设置多数从节点也写成功才是成功，这样即使主节点挂了切到从节点仍然正常，不会出现数据落后。而且当节点数小于一半时会自动停止写的服务。 
mongodb是实现了分布式一致性协议的。redis的主从模式没有使用分布式一致性协议，没有实现强一致，数据有可能不同步从而导致丢失。

Raft集群跟mongodb的副本集的集群方式类似，要解决如果数据commit成功，那么不仅是主机上有，从机上也会有。如果主节点挂了，会自动选出新的主节点。


## paxos和2pc
分布式系统分中心化和去中心化两类，中心化的分布式有协调者和参与者，由协调者去协商，有2pc和3pc两种协议。去中心化的由节点之间互相通信去协商一致，比如paxos.

2PC是解决ACID中的一致性，paxos是解决CAP中的一致性。
2PC用于保证多个数据分片上事务的原子性，Paxos协议用于保证同一个数据分片在多个副本的一致性(如果多个从节点存活，那么从节点的数据跟主节点一定是一致的)。
2PC协议最大的缺陷在于无法处理协调者宕机问题。如果协调者宕机，那么，2PC协议中的每个参与者可能都不知道事务应该提交还是回滚，整个协议被阻塞，
申请的资源都无法释放。因此，常见的做法是将2PC和Paxos协议结合起来，通过2PC保证多个数据分片上的操作的原子性，通过Paxos协议实现同一个
数据分片的多个副本之间的一致性。另外，通过Paxos协议解决2PC协议中协调者宕机问题。当2PC协议中的协调者出现故障时，通过Paxos协议选举出新的协调者继续提供服务。


## paxos
paxos并不指代一个协议，而是一类协议的统称，比较常见的paxos类协议有：basic paxos以及multi-paxos. 
paxos的目的是为了多个参与者达成一致观点.paxos基于一个原则，参与者不能阳奉阴违，一致的观点不会在传递过程中反转.
basic paxos 的协议更复杂，且相对效率较低。所以现在所有的和paxos有关的协议，一定是基于multi-paxos来实现的

paxos中的角色： proposer发送提案；acceptor裁决提案，只能批准一个提案，过半批准原则；learner学习提案；

## raft
Raft在2013年提出,Raft将问题分解和具体化：Leader统一处理变更操作请求，一致性协议的作用具化为保证节点间操作日志副本(log replication)一致，
以term作为逻辑时钟(logical clock)保证时序，节点运行相同状态机(state machine)得到一致结果

一个Raft集群只包含一个Leader节点，其余均为Follower节点；客户端只允许和Leader节点进行交互；Follower节点只允许从Leader节点接收写日志的请求（AppendEntries RPC）；
Leader节点将客户端的请求发送给所有的Follower节点，只有至少一半的节点回复OK时，才可以将日志commit，并返回给用户成功；Leader节点定期向所有的Follower节点
发送心跳信息（不包含实际操作的 AppendEntries RPC），来告诉它们自己依然健康；


<raft论文>： https://raft.github.io/raft.pdf
<入门raft> https://zhuanlan.zhihu.com/p/27910576
<etcd Raft库解析> https://www.codedump.info/post/20180922-etcd-raft/
<Raft算法原理> https://www.codedump.info/post/20180921-raft/
<Raft 为什么是更易理解的分布式一致性算法> https://www.cnblogs.com/mindwind/p/5231986.html
<raft动画演示> http://thesecretlivesofdata.com/raft/

## zab
Zab的全称是Zookeeper atomic broadcast protocol，是Zookeeper内部用到的一致性协议。相比Paxos，Zab最大的特点是保证强一致性(strong consistency，或叫线性一致性linearizable consistency)。


## CAP中的一致性和ACID中的一致性
事务的ACID中的一致性(consistency)是指事务的执行数据库中数据的完整性约束没有被破坏，比如转账操作，A和B账户转账之前账户之和是100元，
转账之后也是100元。其中Atomicity（原子性）、Durability（持久性）和 Isolation（隔离性）
都是存储引擎提供的能力保障，但是Consistency（一致性）却不是存储引擎提供的，相反，它是业务层面的一种逻辑约束。
约束有两个层面：a)数据库机制层面，事务执行前后，数据能符合设置的约束，如唯一约束、外键约束；
b)业务层面，由应用开发人员保证业务一致性。还是以银行转账为例，A、B两个账号，转账之前和之后，A、B两个账号余额总额必须一致

分布式系统的CAP中的一致性(consistency)是数据在多个副本之间保持一致的特性。

Consistency(一致性)和Consensus(共识)是有区别的，consistency指的是， consensus是指多个节点对某个提议达成一致

<分布式理论中各个概念的区分> https://juejin.im/post/5be990d96fb9a049ed3064ba


## 比较总结
Paxos和raft都是一旦一个entries（raft协议叫日志，paxos叫提案，叫法而已）得到多数派的赞成，这个entries就会定下来，不丢失，值不更改，
最终所有节点都会赞成它。Paxos中称为提案被决定，Raft,ZAB,VR称为日志被提交，这只是说法问题。一个日志一旦被提交(或者决定），就不会丢失，
也不可能更改，这一点这4个协议都是一致的。Multi-paxos和Raft都用一个数字来标识leader的合法性，multi-paxos中叫proposer-id，Raft叫term，
意义是一样的，multi-paxos proposer-id最大的Leader提出的决议才是有效的，raft协议中term最大的leader才是合法的



参考：

    <分布式系统一致性的发展历史（一）> https://danielw.cn/history-of-distributed-systems-1
    <分布式系统一致性的发展历史（二）> https://danielw.cn/history-of-distributed-systems-1
    <关于分布式系统的思考> https://www.cnblogs.com/nongchaoer/p/6273044.html
    <Paxos和Raft的前世今生> https://cloud.tencent.com/developer/article/1352070
    <分布式系统理论基础 - 时间、时钟和事件顺序> http://www.cnblogs.com/bangerlee/p/5448766.html
    <分布式系统理论基础 - 一致性、2PC和3PC>  http://www.cnblogs.com/bangerlee/p/5268485.html