软件破解注册： 亦是美网络 http://www.yishimei.cn/

vmware安装centos，既能上外网，又能xshell连接。 
     
    vmware有三种连网络方式，桥接方式能够实现，但是需要与宿主机同一网段的IP，不够方便。 使用NAT模式，虚拟机配置静态IP。 
     
    1.宿主机（windows）的网络配置，需要设置本地网卡能够共享， 
     
    2.VMware的网络配置确认好网管IP，地址段 
     
    3.虚拟机的配置 
     vi /etc/sysconfig/network-scripts/ifcfg-ens33 
    内容增加静态模式及静态IP，网关IP 
    TYPE=Ethernet 
    PROXY_METHOD=none 
    BROWSER_ONLY=no 
    BOOTPROTO=static 
    DEFROUTE=yes 
    IPV4_FAILURE_FATAL=no 
    IPV6INIT=yes 
    IPV6_AUTOCONF=yes 
    IPV6_DEFROUTE=yes 
    IPV6_FAILURE_FATAL=no 
    IPV6_ADDR_GEN_MODE=stable-privacy 
    NAME=ens33 
    UUID=f193f8d1-d9d8-43d9-ab29-0bd32e1b8865 
    DEVICE=ens33 
    ONBOOT=yes 
    IPADDR=192.168.30.220 
    NETMASK=255.255.255.0 
    GATEWAY=192.168.30.2 
     
    然后重启网卡  service network restart 
     
    安装好虚拟机后ip a后不显示IP，是因为vmnet8的属性设置的是静态IP，非自动获取IP。 
    