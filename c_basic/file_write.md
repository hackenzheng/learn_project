## 写文件操作过程

多进程是可以同时读写一个文件的。当一个进程在写，读的进程能否读到最新的内容，取决于最新的内容是否真正写到了磁盘上。

## 写缓存与写磁盘
我们通常用到的写文件API，其实是写到缓存上，可用python语言做一个实验：

    if opt == '-w':
        with open('1.txt', 'w') as writer:
            writer.write('hehe\n')
            time.sleep(10)
    elif opt == '-r':
        with open('1.txt') as fp:
            for line in fp:
                line = line.rstrip()
                print line

我们在用-w选项写hehe之后不会立刻关闭文件，而是sleep了10s，方便使用-r选项去读文件，读的时候我们发现，除非文件关闭，否则读不出任何内容。
这印证了前面的说法，hehe字符串在文件关闭前只在缓存里，还未真正写到磁盘上，所以读进程无法读出。

如何确保写到磁盘上而不只是缓存里呢？python文档给出了建议：

    file.flush() 
    Flush the internal buffer.
    
    Note
    flush() does not necessarily write the file’s data to disk. Use flush() followed by os.fsync() to ensure this behavior.

文档建议我们flush+fsync，确保内容确实更新到了磁盘。

fsync的帮助也指出了这一点：

    os.fsync(fd) 
    Force write of file with filedescriptor fd to disk. On Unix, this calls the native fsync() function; on Windows, the MS _commit() function.
    
    If you’re starting with a Python file object f, first do f.flush(), and then do os.fsync(f.fileno()), to ensure that all internal buffers associated with f are written to disk.

所谓的“内部缓存”就是用户进程内缓存，flush会把用户缓存的内容刷新到内核缓冲区。如果要进一步强制更新到磁盘，linux下用的是大家熟知的fsync，windows下则是_commit函数。

我们将写的代码改成:

    if opt == '-w':
        with open('1.txt', 'w') as writer:
            writer.write('hehe\n')
            writer.flush()
            os.fsync(writer.fileno())
            time.sleep(10)

果然，读进程就能在文件尚未关闭时读到hehe字符串了。

但是，fsync是要慎用的，因为每条内容都强制刷新到磁盘，虽然非常可靠，却会带来性能的急剧下降，我们可以在上述例子的基础上改成写10万条字符串，
对比“普通写”与“fsync写”的效率，会发现后者的耗时是前者的数千倍甚至是上万倍！这也正是redis的AOF日志虽然提供了fsync级别的磁盘
同步却不建议我们使用的原因（也因此redis的日志做不到绝对的单点可靠）。

这里再强调一下，flush只是简单的把用户缓存的内容放到内核缓冲区就返回，本质上是异步的，而fsync要亲自将内核缓冲区的内容交给磁盘驱动程序并等待返回结果，
本质上是同步的。由于fsync还要额外经历：提交到磁盘驱动程序+磁盘驱动程序调用磁盘控制器+磁盘控制器写到物理磁盘等步骤，自然就拖慢了fsync的速度。

## 进程内缓存与内核缓冲区
进程内缓存指的是我在写内核缓冲区前，在自己的程序里再做一个缓存，将多条消息累积到一定的大小，再一次提交给内核缓冲区，这样能避免频繁的write系统调用，
提升写的效率。java里一般要在FileWriter之上再套一层BufferedWriter写入，就是这个用途，实测下来，能有一倍的效率提升。 
python语言里没有BufferedWriter，对于10万条字符串的写可以考虑别的方法，比如我们可以每500条拼成一个大的字符串再做写入，实测也有一倍的效率提升。 
不过，如同前面的“普通写”与“fsync写”一样，效率的提升不是全无代价，它往往伴随着可靠性的降低。进程内缓存是属于某个进程的，一旦该进程突然core掉，
进程内缓存就会丢失，从用户层面看来，就是我明明已经写好了的数据，很可能并未写到磁盘里。相比之下，内核缓冲区就更可靠一些，因为它是由操作系统管理的，
与进程无关，除非是操作系统崩溃或机器断电，否则它不会丢失数据，也就是说，即使我的进程core掉，之前写的内容依然可以安全到达磁盘上。


<转自> https://blog.csdn.net/tlxamulet/article/details/78825396