##### ceph集群部署(以三个节点为例,ceph1,ceph2,ceph3)
参考[https://hub.docker.com/r/ceph/daemon/](https://hub.docker.com/r/ceph/daemon/)

1. 在ceph1创建用于存储配置及日志文件的目录 假设在/data目录下创建
```
mkdir -p /data/ceph/{admin,etc,lib,logs}
# docker内ceph用户id为167
chown -R 167:167 /data/ceph
# 将deploy目录下的shell脚本拷贝至/data/ceph/admin目录下
sudo chmod 777 -R /data/ceph/admin
cp /deploy/* /data/ceph/admin
```

2. 在ceph1将ceph命令alias到本地
```
# 在/etc/profile文件末尾添加alias ceph="docker exec mon ceph"
source /etc/profile
```

3. 在ceph1启动mon
```
# 根据需求修改/data/ceph/admin/start_mon.sh脚本中路径，以及MON_IP,如果节点不在同一网段需要在CEPH_PUBLIC_NETWORK中添加所有的IP段
sh /data/ceph/admin/start_mon.sh
# 启动成功后在/data/ceph/etc/ceph.conf文件中添加
mon clock drift allowed = 2
mon clock drift warn backoff = 30
mon_allow_pool_delete = true
[mgr]
mgr initial modules = dashboard
#如果想要修改osd的备份数，默认为3，可以在/data/ceph/etc/ceph.conf文件中global下添加
osd pool default size = num
#如果将要用作osd的磁盘的文件格式不是xfs格式，需要在/data/ceph/etc/ceph.conf文件global下添加以下内容
osd max object name len = 256
osd max object namespace len = 64
```

4. 将/data/ceph文件夹scp到ceph2,ceph3节点/data目录下,拷贝完成后需要将ceph2,ceph3节点/data/ceph/logs目录的权限修改为167:167，否则启动monitor时将出现没有权限写日志的错误, ceph2,ceph3分别执行start_mon.sh脚本，启动monitor

5. 启动osd
```
# 在三个节点分别准备一块磁盘，并且格式化为xfs格式，并挂载到/data1目录，并在/data1目录新建目录osd，在三个节点依次执行start_osd.sh
# 查看osd状态，在ceph1执行
ceph osd tree
```

6. 启动mds
```
# 三个节点分别执行start_mds.sh脚本
# 在ceph1节点创建文件系统
ceph osd pool create cephfs_data 512 512
ceph osd pool create cephfs_metadata 512 512
ceph fs new cephfstest cephfs_metadata cephfs_data
# 查看cephfs
ceph fs ls
# 查看集群状态
ceph -s
```

7. 启动mgr
```
# 只需要在ceph1执行start_mgr.sh
ceph mgr module enable dashboard
# 启动dashboard
ceph dashboard create-self-signed-cert
# 更新用户名和密码
ceph dashboard set-login-credentials <username> <password>
# 访问https://ceph1-ip:8080 （默认port为8080）可以通过docker logs mgr查看默认端口号
# 修改默认端口号
ceph config-key put mgr/dashboard/server_port port-num
docker restart mgr
```

8. 启动rbd和rgw，分别在三台机器上执行start_rbd.sh和start_rgw.sh

##### 挂载cephfs到k8s pod

1. 获取ceph集群ceph.client.admin.keyring文件中的key值，并做base64加密,用加密后的字符串代替ceph-secret.yaml文件中的key值
```
kubectl create -f example/ceph-secret.yaml
```

2. 直接挂载cephfs到pod中，根据ceph集群中monitor的实际情况，修改cephfs-monitors的内容, namespace必须与ceph-secret中的namespace一致，否则无法读到secret，另外path为/时，表示把cephfs整个mount到容器中，path也可以为/dir，即把cephfs中的dir文件夹mount到容器中，dir文件夹需要提前创建好
```
kubectl create -f example/ceph-example.yaml
```

3. 不直接挂载cephfs，先创建PV和PVC，然后将PVC挂载到指定容器
```
kubectl create -f example/ceph-pv.yaml
kubectl create -f example/ceph-use-pv.yaml
```

##### 挂载cephfs到任一主机

1. 安装ceph-fuse(内网环境也可以直接安装)
```
wget -q -O- 'https://download.ceph.com/keys/release.asc' | sudo apt-key add -
echo deb https://download.ceph.com/debian-luminous/ $(lsb_release -sc) main | sudo tee /etc/apt/sources.list.d/ceph.list
sudo apt update
sudo apt-get install -y ceph-fuse
# 如果内网无法直接apt-get安装 则尝试以下命令
sudo dpkg -i ../../offline/debs/libibverbs1_1.1.8-1.1ubuntu2_amd64.deb
sudo dpkg -i ../../offline/debs/ceph-fuse_12.2.5-1xenial_amd64.deb
```

2. 将ceph集群ceph.client.admin.keyring文件拷贝至当前目录，并创建一个用于挂载的文件夹/mnt/cephfs, 其中ip为集群中任一monitor节点的IP地址
```
sudo ceph-fuse -k ceph.client.admin.keyring -m ip:6789 /mnt/cephfs
```

3. umount
```
sudo fusermount -u /mnt/cephfs
```

##### 局域网离线状态下机器之间时钟同步（不然ceph会出现clock skew告警）
1. 选择局域网中某台机器(选择192.168.99.18)作为时钟同步的标准，编辑/etc/ntp.conf，如果不存在则先执行sudo apt-get install ntp ntpdate
```
# /etc/ntp.conf内容
### begin
driftfile /var/lib/ntp/ntp.drift
statistics loopstats peerstats clockstats
filegen loopstats file loopstats type day enable
filegen peerstats file peerstats type day enable
filegen clockstats file clockstats type day enable
# Specify one or more NTP servers,因为是内网，所以用本地时间做为服务器时间，注意这里不是127.0.0.1
server 127.127.1.0
#我注释掉了这些东西
#pool 0.ubuntu.pool.ntp.org iburst
#pool 1.ubuntu.pool.ntp.org iburst
#pool 2.ubuntu.pool.ntp.org iburst
#pool 3.ubuntu.pool.ntp.org iburst
# Use Ubuntu's ntp server as a fallback.
#pool 127.127.1.0
#增加了NTP服务器自身到时间服务器的同步
fudge 127.127.1.0 stratum 8
#增加了一些需要同步的客户端的ip
restrict -4 default kod notrap nomodify nopeer noquery limited
restrict -6 default kod notrap nomodify nopeer noquery limited
restrict 192.168.99.17
restrict 192.168.99.38
restrict 127.0.0.1
restrict ::1
# Needed for adding pool entries
restrict source notrap nomodify noquery
### end
#重启ntp服务
sudo systemctl restart ntp.service
```

2. 在需要同步的客户端机器上执行
```
sudo apt-get install ntp ntpdate
sudo systemctl stop ntp.service
ntpdate 192.168.99.18
# 在/etc/ntp.conf中添加server 192.168.99.18，并注释掉网络时间服务器
sudo systemctl starts ntp.service
```
##### 在线安装，非容器化形式
1. 准备工作
```
# 假设当前需要部署的节点hostname为node1,node2,node3，hostname为机器/etc/hostname中的值
在部署节点/etc/hosts中添加以下内容：
ip-node1 node1
ip-node2 node2
ip-node3 node3
重启network
sudo systemctl restart networking.service

# 部署节点安装ceph-deploy:
wget -q -O- 'http://mirrors.ustc.edu.cn/ceph/keys/release.asc' | sudo apt-key add -
sudo apt-add-repository 'deb http://mirrors.ustc.edu.cn/ceph/debian-mimic/ xenial main'
sudo apt-get update
sudo apt-get install ceph-deploy
# 每个节点创建cephadmin用户，使得cephadmin用户执行sudo时不需要密码,
ssh user@node1
sudo useradd -d /home/cephadmin -m cephadmin
sudo passwd cephadmin
echo "cephadmin ALL = (root) NOPASSWD:ALL" | sudo tee /etc/sudoers.d/cephadmin
sudo chmod 0440 /etc/sudoers.d/cephadmin
# 部署节点免密登录其他节点
ssh-copy-id cephadmin@node1
ssh-copy-id cephadmin@node2
ssh-copy-id cephadmin@node3
```

2. 开始部署
```
# 创建一个部署文件夹
mkdir ceph-deploy
cd ceph-deploy
# 创建一个集群
ceph-deploy new node1
# 根据网段在ceph.conf中添加public network = 10.1.2.0/24
# 每个节点安装ceph
export CEPH_DEPLOY_REPO_URL=http://mirrors.ustc.edu.cn/ceph/debian-mimic/
export CEPH_DEPLOY_GPG_URL=http://mirrors.ustc.edu.cn/ceph/keys/release.asc
ceph-deploy --username cephadmin install node1 node2 node3
# 初始化monitor
ceph-deploy --username cephadmin mon create-initial
# 拷贝配置文件到各个节点
ceph-deploy --username cephadmin admin node1 node2 node3
# 创建mgr
ceph-deploy --username cephadmin mgr create node1
# 创建osd(需要先umount/dev/vdb，且不能设置自动挂载，删除/etc/fstat中相关内容)
# 如果部署没有报错，但是osd down，可以到指定节点systemctl start对应的osd服务
ceph-deploy --username cephadmin osd create --data /dev/vdb node1
ceph-deploy --username cephadmin osd create --data /dev/vdb node2
ceph-deploy --username cephadmin osd create --data /dev/vdb node3
# MDS
ceph-deploy --username cephadmin mds create node1
# RGW 
ceph-deploy --username cephadmin rgw create node1
# cephfs
sudo ceph osd pool create cephfs_data <pg_num>
sudo ceph osd pool create cephfs_metadata <pg_num>
sudo ceph fs new <fs_name> cephfs_metadata cephfs_data
```
