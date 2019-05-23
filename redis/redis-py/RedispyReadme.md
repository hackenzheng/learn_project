## redisy-py
官方推荐的访问redis的客户端https://redis.io/clients#python， 比较常用的是redis-py,项目地址https://github.com/andymccurdy/redis-py。
Parser可以控制如何解析redis响应的内容。redis-py包含两个Parser类，PythonParser和HiredisParser。如果已经安装了hiredis模块，redis-py会使用HiredisParser，否则会使用PythonParser。
Hiredis是Redis数据库的简约C客户端库。

redis-py源码目录

    -_init_.py
    -_compact_.py (python 2.X版和 3.X版一些库/函数/方法的兼容）
    -client.py （redis客户端，实例一个StrictRedis或者Redis，就可以操作Redis Server）
    -connection.py（与Redis Server的联接，同时提供一个Redis连接池）
    -exceptions.py （定义的异常）
    -util.py （工具方法）
    redis-py的核心代码都在 connection.py和client.py。前一个与Redis Server联通，后一个是操作Redis Server。
    
redis-py提供两个类：StrictRedis和Redis，用于实现Redis的命令，推荐使用StrictRedis。StrictRedis实现了绝大部分官方的命令，
并且使用官方的语法和命令（比如，SET命令对应与StrictRedis.set方法）。Redis是StrictRedis的子类, Redis类是用来向后兼容旧版本的。

redis-py使用connection pool来管理对一个redis server的所有连接，避免每次建立、释放连接的开销。默认时，每个Redis实例都需要维护一个自己的连接池.
也可以通过ConnectionPool直接建立一个连接池，然后作为参数传递到Redis类进行覆盖，这样就可以实现多个 Redis 实例共享一个连接池资源。
意思是默认的话每实例化一个Redis类就会建一个连接池。redis-cli info可查看连接数。
 
 
 <python – 如何在redis中正确使用连接池？> https://codeday.me/bug/20181031/339827.html
 <redis-py源码分析 > https://www.zoulei.net/2016/08/06/redis_py_note/
 
 
 http://xiaorui.cc/2016/05/17/%e7%bb%99redis-py%e6%8f%90%e4%ba%a4pull-request%e5%bc%95%e8%b5%b7%e7%9a%84%e6%80%9d%e8%80%83/
 https://blog.csdn.net/weixin_34348174/article/details/87325512
 https://www.jianshu.com/p/a79fc17ebdf4