1. 惊群问题：
在《unix网络编程中》介绍了多进程模式下同时accept()会唤醒所有的工作进程，在Linux2.6版本以后，内核内核已经解决了accept()函数的“惊群”问题。
但在nginx中，每个worker进程不是直接accept，而是使用epoll等机制进行等待，新版本Linux部分的解决了epoll的“惊群”问题。Nginx中使用mutex互斥锁解决这个问题，具体措施有使用全局互斥锁
具体参考：https://mp.weixin.qq.com/s/hSCm-aYw1qmcx7tks-ApUg