## 什么是lua脚本
Lua 是一种轻量小巧的脚本语言，用标准C语言编写并以源代码形式开放， 其设计目的是为了嵌入应用程序中，从而为应用程序提供灵活的扩展和定制功能。
安装lua执行器，就可以执行用lua编写的脚本,类似shell一样。

## redis为什么要支持lua脚本
1.减少开销–减少向redis服务器的请求次数
2.原子操作–redis将lua脚本作为一个原子执行
3.可复用–其他客户端可以使用已经执行过的lua脚本
4.增加redis灵活性–lua脚本可以帮助redis做更多的事情，比如自定义命令

## redis中怎么使用lua脚本
redis在服务器端内置lua解释器，在redis客户端交互环境中，使用eval和evalsha指令执行lua脚本,或者redis-cli --eval执行指定路径的lua脚本，
evalsha 不同之处是scrip是之前脚本的sha1校验和，这个校验和所对应的脚本必须至少被 EVAL 执行过一次. 不同于eval, script load命令将lua
脚本加载到服务端进行缓存而不是立即执行，然后evalsha 执行，能够加载的也是定义的函数，而非脚本路径。 在redis中不应该执行太过复杂的lua脚本。

    EVAL script numkeys key [key …] arg [arg …]
    
    EVAL —lua程序的运行环境上下文
    script —lua脚本，定义的lua函数字符串格式，而非lua脚本路径
    numkeys —参数的个数(key的个数)
    key —redis键 访问下标从1开始,例如:KEYS[1]
    arg —redis键的附加参数


可以使用两个不同的Lua函数从Lua脚本调用Redis命令
redis.call() – 出错时返回具体错误信息,并且终止脚本执行
redis.pcall() –出错时返回lua table的包装错误,但不引发错误

Redis保证以原子方式执行脚本：执行脚本时不会执行其他脚本或Redis命令。与 MULTI/EXEC 事务的概念相似。从所有其他客户端的角度来看，
脚本要不已经执行完成，要不根本不执行。

<深入分析 Redis Lua 脚本运行原理> https://juejin.im/post/5bce7e9fe51d457a772bcfc6