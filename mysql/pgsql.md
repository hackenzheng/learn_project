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

创建用户 create user dbuser with password 'postgres'
修改密码 ALTER USER postgres WITH PASSWORD 'postgres';


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


## 分区
pgsql支持分区，通过分区在底层分文件存储可以存储更多的数据。不同于分表，分区对外仍然是一张表，会有解析上的性能瓶颈。

pgsql 10.0之前的版本创建分区需要使用inherit，新版本是不用，创建表时指定分区字段，并且能获取分区存储使用情况及动态增加分区。

