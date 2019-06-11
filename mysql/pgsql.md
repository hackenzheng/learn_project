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


## 分区
pgsql支持分区，通过分区在底层分文件存储可以存储更多的数据。不同于分表，分区对外仍然是一张表，会有解析上的性能瓶颈。

pgsql 10.0之前的版本创建分区需要使用inherit，新版本是不用，创建表时指定分区字段，并且能获取分区存储使用情况及动态增加分区。


## 查询时间测试

postgres 数据库查看sql的执行时间：

    \timing on  \timing off  打开时间分析开关
    explain select count(*) from table; 只要查询计划，不会真正的执行
    EXPLAIN ANALYZE select count(*) from table;  既有查询计划也会真正的执行耗时
    
    

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


## pgbench
pgbench是基于tpc-b模型的postgresql测试工具

创建好数据库pgbench : create database pgbench-test

初始化数据库pgbench-test: pgbench -i pgbench-test -h localhost -U postgres , 需要输入密码，会创建
pgbench_history, pgbench_tellers, pgbench_accounts, pgbench_branches四个表,但不会有数据。

执行测试：pgbench -h localhost -U postgres -c 10 -t 100 -d pgbench-test.
-c clients 模拟的客户数，也就是并发数据库会话数目,默认是1。 -t transactions 每个客户端跑的事务数目，默认是 10。


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
    select * from day_result where age = :age;
    select * from day_result where age > :age;
    3. 保存为test.sql
    pgbench -h localhost -U postgres -c 10 -t 100 -d pgbench-test -f ./test.sql
    
    <官方手册 有自定义脚本的说明>https://www.postgresql.org/docs/9.6/pgbench.html