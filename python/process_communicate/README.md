多进程常用的通信方式：
文件
管道pipe
以太网套接字
unix域套接字
无名套接字socketpair
有名管道fifo
OS消息队列
共享内存
中间件消息队列redis等


例子： Python使用多进程完成计算密集型任务pi的计算，通信模式有多种，参考
<Python广为使用的并发处理库futures使用入门与内部原理> https://juejin.im/post/5b1e36476fb9a01e4a6e02e4
<Python多进程编程基础——图文版> https://juejin.im/post/5b0a88b4f265da0db06e4385
<深入Python进程间通信原理--图文版> https://juejin.im/post/5b0abab451882538c220440b