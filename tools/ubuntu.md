# ubuntu环境下的工具
    
色温调整

    Windows下是flux, ubuntu下是redshift
    安装 apt-get install redshift
    启动 redshift 或redshift &
    源码地址 https://github.com/jonls/redshift
    
  
  
截图 shutter




## 软件安装
二进制安装， 将二进制文件放到/usr/bin或/usr/local/bin等目录下， make install 就是将二进制文件移动到系统目录

源码安装， 是指将源代码弄成可执行文件，再将可执行文件移动到系统目录

deb安装， 下载deb包，然后dpkg -i **.deb即可

apt安装， 在线安装的方式，能够自动解决软件依赖关系，安装的包会下载到/var/cache/apt/archives，可以手动清理或者sudo apt-get clean的方式清理。
在用docker发布时如果有通过此方式安装最好清理一下。 另外apt安装时还会在/var/lib/apt/lists存储软件包列表信息，可以手动清理



