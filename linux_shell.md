常用命令： 

    tcpdump -i eth1 -vnn  port 80 -e/tcpdump -i eth1 -vnn  port 80 
    tcpdump -i eth0 "host 113.105.88.151 && icmp"  -vnn   #支持的是网络层协议，不支持http等应用层协议
    tcp.flags.syn == 1 and tcp.flags.ack == 0   #过滤tcp连接时的包
    
    ping -c 1 -i 0.5 -t 3 www.baidu.com|grep PING|awk '{print $3}'
         
    date -d @1508450365    #时间戳转日期
    date -d '2013-2-22 22:14' +%s   #日期转时间戳
    
    gzip -d xxx.gz    #直接解压gz文件，不是tar.gz文件
    gzip xxx.file     #压缩某个文件为xx.gz
    
    ./mpstat -P ALL 1 4    #单独查看每个cpu的使用情况
    
    bash换行echo -e 和echo ‘-e’都可以
    
    grep -Rni 'key work' ./    # 在但当前目录下搜索含关键字的内容
    find ./ -name "*.html" -maxdepth 1|grep -v 'index.html'|xargs rm -f  
    
    du -h -d 1
    lsof | grep delete    #已经被删除但是仍被使用的文件
    echo "" >> file       #在线清空文件,rm只是删除了文件名与inode的link关系

netstat:

    -a (all)显示所有选项，只netstat不带任何选项是不显示LISTEN相关
    -t (tcp)仅显示tcp相关选项, udp是-u
    -n 拒绝显示别名，能显示数字的全部转化成数字,比如localhost会转成0.0.0.0， 服务器name会转成本机局域网ip，比如k8snode->192.168.12.189
    -l 仅列出有在 Listen (监听) 的服務状态
    -p 显示建立相关链接的程序名
    
    提示：LISTEN和LISTENING的状态只有用-a或者-l才能看到
  

top:
    
    load average 后面是平均3分钟，5分钟的cpu消耗指标，一个cpu用满就是1,5个cpu用满就是5
    
    KiB Mem 显示的是内存使用情况，total是物理内存总量， free是未分配的内存总量， used是已经使用的(不等于已分配的)， buff/cache是已分配里面未被使用的
    buff指的是写缓冲， chache指的是读缓存。 E(shift+e)可以切换内存的单位
    
    N – 以 PID 的大小的顺序排列表示进程列表
    P – 以 CPU 占用率大小的顺序排列进程列表
    M – 以内存占用率大小的顺序排列进程列表
    
set:
    
    设置环境变量用, 符号"+"和"-"的作用分别是打开和关闭指定的模式, 常用于执行脚本前的环境配置
    set -e; -e：若指令传回值不等于0，则立即退出shell。

挂载磁盘 

    （1）创建目录/data
    （2）使用fdisk -l 查看所有的磁盘信息，找到未挂载的磁盘
    （3）mkfs.xfs -f /dev/vdb 格式化分区
    （4）mount /dev/vdb /data挂载
    （5）df -h 查看挂载情况
    （6）编辑/etc/fstab，设置开机自动挂载
        /dev/vdb      xfs defaults  /virus 0 0
         
    给已有目录扩容：先加一块临时盘（原来的目录已没有多余空间了），将当前目录的数据拷贝到临时盘，然后将新盘挂到目录上，再从临时盘上将数据拷贝过去。
    同一目录不能挂两块盘，不用临时盘也可以，将新盘挂到原来的目录，再将原来的盘挂载到其他目录，数据不会丢失，再把原来的数据拷贝到新盘即可。 
    
    
ls查看的文件大小，du查看的是文件或文件夹占用的磁盘大小，df是查看磁盘分区的使用情况，-h都是以GB等显示。一般情况，ls显示的文件大小
比du显示的磁盘占用空间小，文件系统中是分block，一个block是4k只存储一个文件的内容，一个13k大小的文件，需要分做4个block存储，占用磁盘空间就是16k。


ubuntu下service、systemctl和/etc/init.d的关系：

    都是跟系统服务有关，/etc/init.d目录下是开机自启动脚本,比如重启网卡可以是/etc/init.d/networking restart
    service命令本身也是shell脚本,它会去/etc/init.d目录下查找对应服务的脚本然后启动,比如service networkking restart
    
    systemctl是新的机制,替换了service和chkconfig，service仍然能够使用,所有service能够管理的服务systemctl也可以，使用方式是systemctl restart networking.service,
    每个服务后面都要跟'.service'. 能够使用service命令进行操作的，就是已经注册成为linux的系统服务了，也就是service只对系统服务有效。注册为系统服务，
    可以方便的用service进行管理，不需要写一大串原始路径。把服务名放到/etc/rc.d/init.d目录中，就成了系统服务，比如httpd,network, 
    service本身是一个shell脚本。sudo /etc/init.d/http restart/service http start/systemctl start httpd.service三种方式是一样的.   
    有时会自己编写一个脚本/usr/sbin/startall，将/etc/init.d下的服务全部启动。 

进程卡住的排查思路： 
先查看日志信息，若卡住没有任何日志，则strace -p 进程号查看进程的堆栈调用信息。 若显示recvfrom(5,这种，则是进程调用recvfrom时，在文件描述符5的地方卡住了，
可在该进程的目录下查看文件描述为5的信息，被杀掉的进程改目录会被清掉，cd /proc/进程号/fd/5， socket连接也是文件，后面会附带端口， 
可在/proc/net/tcp查看链接的状态信息，可根据进程号或端口号grep过滤。


linux默认定时执行的任务只有hour,day,week,monthly，如果要增加每分中执行的，需要在/etc/cron.d目录下添加一个文件，比如1min文件，其中的内容如下，同时新建/etc/cron.min目录。
目录下的定时脚本脚本不能是.sh结尾。 要避免同时有多个定时任务在执行，比如某个定时任务是1min中执行一次，但某次执行的时间超过了一分中，所以要在脚本里面做判断。


## nfs
网络文件系统,类似于Windows下的共享目录， 有服务端和客户端之分，服务端需要安装nfs软件，然后配置好哪个目录是共享的。在任意服务器通过
挂载mount的方式将共享的目录挂载到本地，比如 mount 192.168.1.2:/home/zhg /mnt/zhg,这样就可以跟访问本地文件系统一样访问nfs服务器上的。



## vi
vi的可视化模式有三种：

    用 v 命令进入的字符可视化模式
    用 V 命令进入的行可视化模式
    用 ctrl-V 进入的块可视化模式(列模式)
    重复按一次或者esc退出到单行命令模式
    
    可视化模式下的操作：
    y 复制
    p 粘贴
    x 剪切
    I 列插入状态
    d只删除选中的字符，而D删除选中字符所在行的所有字符，c 和 C ， y 和 Y 同理
    
vim插件配置： spacevim 或 spf-13 vim 或youcompleteme+ctag

复制缩进问题： :set paste

从vi复制到浏览器:

    sudo apt-get install vim-gnome  
    
    vi ~/.vimrc 添加如下内容：
    nmap <c-c> "+y
    nmap <c-v> "+p


## 免密ssh登录
ssh认证方式有密码和秘钥两种方式， 将本机公钥放到对端，ssh及scp的时候就不用输密码

步骤：

    生成密钥对 ssh-keygen -t rsa  会在用户home目录下生成.ssh文件夹，如果已经有了就不用再生成
    拷贝秘钥 ssh-copy-id -i ~/.ssh/id_rsa.pub zhenghg@192.168.2.177
    给服务器设置别名 vi .ssh/config 添加如下四行
    Host z177     # 服务器别名，以后就可以ssh z177即可
    HostName 192.168.2.177
    User zhenghg
    IdentitiesOnly yes

ssh -o ServerAliveInterval=30 z177  定时连接，避免服务中断


