## 介绍
golang是编译型语言，需要先安装golang编译器，类似于gcc。golang编译器是用go写的，代码托管在https://github.com/golang/go。
在go1.4之前，要编译golang编译器，用到另外一个工具gccgo，是用c写的。Go 1.5实现了bootstrapping(自举)，通俗地讲“用要编译的目标语言编写其编译器（汇编器）。


### 二进制安装
从官网https://golang.google.cn/dl/下载linux版编译好的安装包。
解压到/usr/local/go,设置环境变量/etc/profile: export PATH=$PATH:/usr/local/go/bin


### 源码安装
编译go1.4：

    cd ~
    wget https://storage.googleapis.com/golang/go1.4-bootstrap-20170531.tar.gz
    或者wget https://golang.google.cn/doc/install/source?download=go1.12.4.src.tar.gz
    tar zxvf go1.4-bootstrap-20170531.tar.gz
    cd go/src/
    ./all.bash
    
    编译完成后，可以看到如下输出:
    ALL TESTS PASSED

编译go1.5及以上版本：

    Go 1.5开始编译器和运行时用go自身编写，要编译它们，首先要安装go编译器。all.bash 编译脚本会在$GOROOT_BOOTSTRAP环境变量中查找一个已经存在的go 
    tool chain，实际上就是要有一个编译好的bin/go程序，$GOROOT_BOOTSTRAP/bin/go应该是go二进制命令。有很多选择，
    可以在官网(https://golang.org/dl/)下载go发布包；也可以用go1.4源码编译，也就是按照上面的步骤编译go1.4，然后再去编译更高版本的go。
    用官方下载的go1.7编译go 1.8，ubuntu 16.04.2 举例:
    
    cd ~
    wget https://storage.googleapis.com/golang/go1.7.6.linux-amd64.tar.gz
    wget https://github.com/golang/go/archive/go1.8.3.tar.gz
    tar zxvf go1.7.6.linux-amd64.tar.gz
    tar zxvf go1.8.3.tar.gz
    export GOROOT_BOOTSTRAP=/home/dell/go
    cd go-go1.8.3/src
    ./all.bash
    
    编译成功后，有如下输出：
    ##### API check
    Go version is "go1.8.3", ignoring -next /home/dell/go-go1.8.3/api/next.txt
    ALL TESTS PASSED
    
如下两种方式是参考： https://www.cnblogs.com/majianguo/p/7258975.html，没有在本地跑过
    
## 编辑器
Ubuntu下可选的有jetbrains的Goland， vscode.
vscode： 从官网下载deb包，直接安装.
其他工具参考： https://github.com/astaxie/build-web-application-with-golang/blob/master/zh/01.4.md

## 参考资料
<go-web编程中文版>https://github.com/astaxie/build-web-application-with-golang/blob/master/zh/preface.md

<腾讯 go语言最佳实践>https://cloud.tencent.com/developer/article/1145176

## 并发
go的协程goroutine比起线程使用起来更方便更轻量，能替代线程的使用，并配套了channel用于通信作同步。
如果实在要用多进程多线程模式用syscall里面的方法。

go的channel既能做同步，也能通信用.