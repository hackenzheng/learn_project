## pgsql

按照官方Ubuntu apt方式安装后pgsql会自动启动，ps -ef | grep post可以看到启动命令是
`/usr/lib/postgresql/10/bin/postgres -D /var/lib/postgresql/10/main -c config_file=/etc/postgresql/10/main/postgresql.conf`
以及6个子进程。安装过程会自动创建一个 postgres的用户，也给ubuntu创建了一个postgres用户，都没有密码。

登录 sudo -u postgres psql 或者su postgres; psql， 默认端口是5432

查看当前用户： select user;


设置postgres用户密码

    先清除 sudo passwd -d postgres
    在设置密码 sudo -u postgres passwd


默认pg只允许本机通过密码认证登录，且认证方式是peer和ident，远程登录设置, peer认证指的是切换到有权限的用户不用密码

    sudo vi /etc/postgresql/10/main/postgresql.conf 
    将 #listen_addresses = 'localhost' 改为 listen_addresses = '*'
    
    sudo vi /etc/postgresql/10/main/pg_hba.conf 
    添加如下行
    # TYPE  DATABASE  USER  CIDR-ADDRESS  METHOD
    host  all  all 0.0.0.0/0 md5
    
    重启服务 sudo /etc/init.d/postgresql restart

远程登录

    psql --host=192.168.99.100 --port=30432 --username=postgres --password=postgres
    psql --h 192.168.99.100 --p 5432 -U postgres -W postgres
    
    psql -U postges -W 登录走的是unix socket，用的是peer认证
    psql -h localhost -U postges -W 走的是ident认证
    
    将pg_hba.conf文件中的如下配置中的peer改为md5这样就会使用密码认证
    # Database administrative login by Unix domain socket
    local   all             postgres                                md5/peer
    
    <连接PostgreSQL> https://www.jianshu.com/p/f246dc45e6dc

service postgresql restart/start/stop/reload/status

如果忘记密码：

    方式一: 开启peer认证,使用sudo -u postgres psql即可登录，然后修改密码
    方式二： 将md5改为trust,即不用认证，psql -h localhost -U postgres登录重置密码后再改回去

    修改密码 ALTER USER postgres WITH PASSWORD 'postgres';

用户和密码：
    
    pg会自动在操作系统和postgres数据库中分别创建一个名为postgres的用户以及一个同样名为postgres的数据库。
    创建用户的方式：
    (1) 在linux系统命令行中使用createuser命令中创建  createuser admin
    (2)在pg命令行中使用CREATE ROLE指令创建 CREATE ROLE admin;
    (3)在PostgresSQL命令行中使用CREATE USER指令创建 create user admin with password 'postgres';  登录提示数据库不在
    CREATE USER和CREATE ROLE的区别在于，CREATE USER指令创建的用户默认是有登录权限的，而CREATE ROLE没有。
    
    \du 查看当前所有用户
    select user 查看当前登录用户

常用操作：

    create database day_result;
    drop table day_result;  # 删除数据库
    \c dbname 切换数据库
    \l 列举数据库
    \dt 列举表
    \d tablename  描述表结构
    create table grade(id int, score int);  # 创建成绩表


## 分区
pgsql支持分区，通过分区在底层分文件存储可以存储更多的数据。不同于分表，分区对外仍然是一张表，会有解析上的性能瓶颈。
PostgreSQL 10 是第一个支持内置声明式分区表的版本。支持 range、list 分区，与以前的版本相比，提供了显著的性能和易用性优势，但却忽略了许多功能特性和性能优化。
PostgreSQL 11 为分区表功能提供更多的改进。这些特性包括：hash 分区、索引增强、DML改进，以及性能优化：faster partition pruning、run-time partition pruning,、partition-wise join。

分区方式有范围分区和列表分区两种， 范围分区就是指定一个区间，列表分区是将符合条件的都要列出来.
分区表的使用也要看场景，有些场景有优势，有些场景没有优势。

    在特定场景下，查询性能极大提高，尤其是当大部分经常访问的数据记录在一个或少数几个分区表上时。表分区减小了索引的大小，并使得常访问的分区表的索引更容易保存于内存中。
    当查询或者更新访问一个或少数几个分区表中的大部分数据时，可以通过顺序扫描该分区表而非使用大表索引来提高性能。
    可通过添加或移除分区表来高效的批量增删数据。如可使用ALTER TABLE NO INHERIT可将特定分区从主逻辑表中移除（该表依然存在，并可单独使用，只是与主表不再有继承关系并无法再通过主表访问该分区表），或使用DROP TABLE直接将该分区表删除。这两种方式完全避免了使用DELETE时所需的VACUUM额外代价。
    很少使用的数据可被迁移到便宜些的慢些的存储介质中
    以上优势只有当表非常大的时候才能体现出来。一般来说，当表的大小超过数据库服务器的物理内存时以上优势才能体现出来

分区要先建立父表，然后再手动建立分区表，所以分区表的个数可以手动调整。

<PostgreSQL 10分区表详解及性能测试报告> http://www.postgres.cn/news/viewone/1/271

<PostgreSQL 11 分区表用法及增强> http://www.postgres.cn/news/viewone/1/347

<PostgreSQL 创建分区表> https://blog.csdn.net/zpf336/article/details/73809481


## 查询时间测试

postgres 数据库查看sql的执行时间：

    \timing on  \timing off  打开时间分析开关
    explain select count(*) from table; 只要查询计划，不会真正的执行
    EXPLAIN ANALYZE select count(*) from table;  既有查询计划也会真正的执行耗时
    

## 索引优化
索引可以提高查询速度，但是不代表加了索引就一定会加快查询速度，有时甚至会适得其反。
另外要看数据的分布，你先看哪个语句慢，条件是什么，这个条件下，数据的分布如何，如果这个条件下，数据超过10%的分布在某个值，那这个索引基本也提高不了性能，因为筛选出的数据集还是很大。
另外对长字段加索引查询速度也可能变慢，可以使用前缀索引，即对字段的前多个少个字符索引。

explain结果查看：

    seq scan，顺序扫描又是全表扫描
    
    index scan，索引扫描（需要回表）
    
    index only scan，索引扫描（通过VM减少回表，大多数情况下，不需要回表）
    
    bitmap scan，普通的index scan一次只读一条索引项，那么一个PAGE面有可能被多次访问；而 bitmap scan一次性将满足条件的索引项全部取
    出，并在内存中进行排序, 然后根据取出的索引项访问表数据。当 PostgreSQL 需要合并索引访问的结果子集时 会用到这种方式 ，通常是在用到 "or"，
    “and”时会出现"Bitmap heap scan"。即bitmap分为bitmap index scan和bitmap heap scan两个阶段,bitmap index scan 就是index scan。
    先扫描索引获取到对应的page页，这个时候可能会有不同的索引项对应到通一个page,统计出最终需要扫描的page，然后将数据取出来进行排序等，减少io次数。
    对于每个查询条件，在对应索引中找到符合条件的堆表PAGE，每个索引构造一个bitmap串。在这个bitmap串中，每一个BIT位对应一个HEAP PAGE，
    代表这个HEAP PAGE中有符合该条件的行。


<PostgreSQL 9种索引的原理和应用场景>  https://github.com/digoal/blog/blob/master/201706/20170627_01.md

<postgresql中的各种scan的比较> https://www.cnblogs.com/flying-tiger/p/6702796.html

<PostgreSQL bitmapAnd> https://yq.aliyun.com/articles/70462

## Greenplum
Greenplum是基于postgresql的MPP架构的大数据处理开源数据库，能够线性扩展，支持pb级数据。 采用master/segment架构，
每个segment都是一个pg实例，master负责sql解析，每个表根据字段hash存储到多个segment节点，查询的时候并行查询然后再将结果汇总。

Greenplumd的存储方式可以灵活配置，一张表的不同数据可以使用不同的物理存储方式，支持的存储方式有行存储，列存储以及外部表， 
外部表是数据保存在其他系统中例如HDFS，数据库只保留元数据信息。

数据库的数据来源：Oracle这样的数据库里面的数据多是客户生成的，譬如你银行转账、淘宝订单等。对于数据分析型的数据库，其源数据通常是在其他系统中，而且数据量很大。
这样数据加载的能力就变得非常重要。Greenplum提供了非常好的数据加载方案，支持高速的加载各种数据源的不同数据格式的数据。
数据源支持Hadoop，文件系统，数据库，还有 ETL管理的数据。数据格式支持文本，CSV，Parquet，Avro等。

MPP(Massively Parallel Processing)的重点首先是本地存储数据，其次是通过网络交换数据，最后是每个数据都是数据节点的一部分，它们之间没有共享(shared nothing)。

<在 MySQL 和 PostgreSQL 之外，为什么阿里要研发 HybridDB 数据库？> https://www.infoq.cn/article/2016/12/MySQL-PostgreSQL-Greenplum


## 性能测试时碰到的问题
目的是造1亿条数据，索引字段是age和datestr，不小心datestr只限制在一个月内，导致每天的数据量特别大，建了索引之后查询反而更慢了。
explain会发现走的是bitmap scan.

即使建了索引，如果索引字段的某个值对应有很多数据，查询会很耗时。 比如当获取的数据分布很大(比如70%以上)时，
用index scan 已经没有意义了，因为数据太多了，走索引再走表的代价已经超过了单纯走表的代价了。这里的分布考虑两点，
一个是本身的数据量，如果是百万级即使只有3%也会慢；另外就是占比，如果超过50%比全量扫描的代价也差不多，因为走索引要回表。
如果通过limit限制查询数量会加快。

但如果用到了排序，即使用了limit,查询也会耗时, 所以测试应用用深分页查询。
select * from day_result where datestr='20190605' offset 100000 limit 10;  # 立即出结果
select * from day_result where datestr='20190605' order by age offset 100000 limit 10; #需要等几秒

查询的时候mongodb比较耗内存，pgsql比较耗cpu.


## pgbench
pgbench是基于tpc-b模型的postgresql测试工具，安装好pgsql自带pgbench

创建好数据库pgbench : create database pgbench-test

初始化数据库pgbench-test: pgbench -i pgbench-test -h localhost -U postgres , 需要输入密码，会创建
pgbench_history, pgbench_tellers, pgbench_accounts, pgbench_branches四个表,但不会有数据。

执行测试：pgbench -h localhost -U postgres -c 10 -t 100  pgbench-test.
-c clients 模拟的客户数，也就是并发数据库会话数目,默认是1。 -t transactions 每个客户端跑的事务数目，默认是 10。 -d是打印日志，不能重定向，
如果服务端没有响应会一直client 0 receiving


执行自定义测试脚本：pgbench -h 192.168.11.127 -U postgres  -c 1 -t 1 -P 2 ailite -f ./pg.sql, -P 2是每隔2s输出信息。
如果执行报错先pgbench -i ailite初始化一下，测试的时候仍然是执行自定义的语句，如果自定义的语句有错会执行不下去


四个表的结构：
```
pgbench=# \d pgbench_accounts
              Table "public.pgbench_accounts"
  Column  |     Type      | Collation | Nullable | Default 
----------+---------------+-----------+----------+---------
 aid      | integer       |           | not null | 
 bid      | integer       |           |          | 
 abalance | integer       |           |          | 
 filler   | character(84) |           |          | 
Indexes:
    "pgbench_accounts_pkey" PRIMARY KEY, btree (aid)
```

```$xslt
pgbench=# \d pgbench_branches
              Table "public.pgbench_branches"
  Column  |     Type      | Collation | Nullable | Default 
----------+---------------+-----------+----------+---------
 bid      | integer       |           | not null | 
 bbalance | integer       |           |          | 
 filler   | character(88) |           |          | 
Indexes:
    "pgbench_branches_pkey" PRIMARY KEY, btree (bid)
```

```$xslt
pgbench=# \d pgbench_history 
                    Table "public.pgbench_history"
 Column |            Type             | Collation | Nullable | Default 
--------+-----------------------------+-----------+----------+---------
 tid    | integer                     |           |          | 
 bid    | integer                     |           |          | 
 aid    | integer                     |           |          | 
 delta  | integer                     |           |          | 
 mtime  | timestamp without time zone |           |          | 
 filler | character(22)               |           |          | 
```

```$xslt
pgbench=# \d pgbench_tellers
              Table "public.pgbench_tellers"
  Column  |     Type      | Collation | Nullable | Default 
----------+---------------+-----------+----------+---------
 tid      | integer       |           | not null | 
 bid      | integer       |           |          | 
 tbalance | integer       |           |          | 
 filler   | character(84) |           |          | 
Indexes:
    "pgbench_tellers_pkey" PRIMARY KEY, btree (tid)
```

默认执行的测试语句
```
\set aid random(1, 100000 * :scale)
\set bid random(1, 1 * :scale)
\set tid random(1, 10 * :scale)
\set delta random(-5000, 5000)
BEGIN;
UPDATE pgbench_accounts SET abalance = abalance + :delta WHERE aid = :aid;
SELECT abalance FROM pgbench_accounts WHERE aid = :aid;
UPDATE pgbench_tellers SET tbalance = tbalance + :delta WHERE tid = :tid;
UPDATE pgbench_branches SET bbalance = bbalance + :delta WHERE bid = :bid;
INSERT INTO pgbench_history (tid, bid, aid, delta, mtime) VALUES (:tid, :bid, :aid, :delta, CURRENT_TIMESTAMP);
END;
```


使用自定义脚本测试：

    默认只能用固定的四张表进行，实际中往往会结合自己的业务进行测试，就要自行编写sql脚本用于测试。
    
    1.先创建好数据库和表
    2.编写sql, 变量只支持数值型
    \set age random(1, 95)
    select * from day_result where age = :age offset 10000 limit 10;
    select * from day_result where age > :age;
    3. 保存为test.sql
    pgbench -h localhost -U postgres -c 10 -t 100 -d pgbench-test -f ./test.sql
    
    <官方手册 有自定义脚本的说明>https://www.postgresql.org/docs/9.6/pgbench.html
    


## sysbench
SysBench是一个模块化的、跨平台、多线程基准测试工具,除了测性能之外还可以测试系统负载如cpu,磁盘io,内存分配和传输速度等。
目前sysbench主要支持 MySQL,pgsql,oracle 这3种数据库。

安装： sudo apt-get install sysbench

<详解MySQL基准测试和sysbench工具>  https://www.cnblogs.com/kismetv/p/7615738.html


## pgsql中文存储
在postgresql中，中文是以中文编码的方式存储在服务端，比如'中文'两个字实际存储为utf-8为'\u4e2d\u6587'。
pgsql支持简体中文有四种编码：EUC_CN（Extended UNIX Code-CN）、GB18030、GBK和UTF-8。但GB18030和GBK只能作为客户端编码，不能设置为服务端编码,服务端一般都用utf-8.

查看pg客户端字符编码: show client_encoding；
查看pg服务端字符编码: show server_encoding。

python中对utf-8的处理

    1 >>> s = u'\u4e2d\u6587'
    2 >>> print s
    3 中文
    1 >>> s = '\u4e2d\u6587'    
    2 >>> print s
    3 中文
    
    Python3中默认就是utf-8编码，是否前缀u''不影响
    
<PostgreSQL 字符集问题> https://www.douban.com/note/331854618/