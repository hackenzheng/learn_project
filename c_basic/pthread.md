## 互斥锁
计算机原理中单条指令不会被中断，只会在指令之间处理中断信号，中断导致了非原子操作，会影响到对内存、打印机等共享变量的操作。
在smp架构下的多CPU情况中，原子操作的保证更复杂些，有对总线加锁以及对缓存加锁等方式。


## unix多线程使用的锁pthread_mutex_t
Linux环境下多线程同步中常用的互斥锁的实现pthread_mutex_t，是个结构体，定义在/usr/include/x86_64-linux-gnu/bits/pthreadtypes.h 文件中

获取锁的核心是LLL_MUTEX_LOCK宏，其定义：

    # define LLL_MUTEX_LOCK(mutex) \
      lll_lock ((mutex)->__data.__lock, PTHREAD_MUTEX_PSHARED (mutex))
    
    lll_lock中使用到了汇编代码，用的cmpxchgl指令实现了CAS达到了原子操作。先使用CAS判断_lock是否占用，若未占用，直接返回。否则，
    通过__lll_lock_wait_private调用SYS_futex系统调用迫使线程进入沉睡。 上述过程就是所谓的FUTEX同步机制，CAS是用户态的指令，
    若无竞争，简单修改锁状态即返回，非常高效，只有发现竞争，才通过系统调用陷入内核态。所以，FUTEX是一种用户态和内核态混合的同步机制，它保证了低竞争情况下的锁获取效率。
                     

<pthread包的mutex实现分析> https://blog.csdn.net/tlxamulet/article/details/79047717

pthread_mutex_t中用到了futex,在不存在竞争的情况下，不用调用系统调用陷入到内核，提高了系统性能。

<futex原理> https://blog.csdn.net/qq100440110/article/details/52304389


## linux内核实现的锁
在Ubuntu等系统中，Linux内核源码在/usr/src/linux*目录下，不同版本号不一样，比如当前环境定义mutex的头文件路径/usr/src/linux-headers-4.15.0-48-generic/include/linux/mutex.h
这个锁的本质也是互斥锁，与pthread_mutex一样，只是内核自身用。


<linux 2.6 互斥锁的实现-源码分析>  https://www.bbsmax.com/A/o75NWBjWdW/

<Linux内核互斥锁--mutex> https://www.bbsmax.com/A/QV5ZeDlwJy/


## 自旋锁 spin_lock
<Pthreads并行编程之spin lock与mutex性能对比分析>  http://www.parallellabs.com/2010/01/31/pthreads-programming-spin-lock-vs-mutex-performance-analysis/