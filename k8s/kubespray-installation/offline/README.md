#### 离线安装kubernetes

##### Requirements
1. ubuntu16.04
2. nvidia driver installed
3. Internal ubuntu apt source enabled to install required softwares in required-debs.txt

##### step 1 ssh免密登录
需要保证当前节点root用户能ssh免密码登录到所有节点的root用户
1. root用户默认可能没有设置密码，sudo su切换到root用户后passwd更新root密码
2. 默认ssh不支持root账户，需要将/etc/ssh/sshd_config文件中PermitRootLogin设置为yes保存后，重启ssh.service
```
sudo systemctl restart ssh.service
```

3. 在root账户下使用ssh-keygen命令生成密钥，ssh-copy-id到其他所有需要部署的节点

##### step 2 部署节点安装依赖
```
# 在process目录下执行
sh requirements.sh
# 验证是否安装成功
sudo ansible --version
```

##### step 3 安装docker及nvidia-docker,netaddr,以及关闭交换分区
```
# 在process目录下执行
declare -a IPS=(192.168.99.17 ...)
sh install_docker.sh ${IPS[@]}
# 注意：如果已经安装了docker18.03以及相应的nvidia-docker版本，可以跳过此步骤，但需要执行sh ../preinstall/preoption.sh ${IPS[@]} 以关闭所有节点的交换分区
```

##### step 4 解压docker images，重命名后push到私有的仓库
```
# 注意：只在一台机器上安装测试，则不需要以下1，2，3步，只需要在process目录下执行以下两条命令，解压image压缩包，然后load所有的images
python preprocess_imgs.py --options decom
python preprocess_imgs.py --options load
# 1. 创建私有的docker仓库，只在当前网段或者环境中没有私有仓库的情况下需要创建,在修改process/docker_registry.sh中/path/to/registry,然后在process目录中执行,可以将该脚本拷贝至安装有docker且有registry镜像的机器，当前内网环境已经在99.10部署好了私有docker仓库
sh docker_registry.sh
# 2. 非安全的私有仓库设置
sudo tee /etc/systemd/system/docker.service.d/docker-options.conf <<EOF
[Service]
Environment="INSECURE_REGISTRY=--insecure-registry=192.168.99.10:5000"
EOF
# 如果/etc/systemd/system/docker.service不存在，则修改/lib/systemd/system/docker.service：
ExecStart=/usr/bin/dockerd -H fd:// --insecure-registry=192.168.99.10:5000
# 重启docker服务
sudo systemctl daemon-reload
sudo systemctl restart docker.service
# 3. 在process目录下执行
python preprocess_imgs.py
```

##### step 5 更新docker image相关配置文件
```
# 如果在单机上安装，且没有创建私有的docker registry则可以跳过整个step 5
# 在process目录下执行
python update_img_repo.py
```

##### step 6 更新集群配置文件
```
# 生成host配置文件, 需要在kubespray根目录执行，也可以手动修改inventory/sample/host.ini然后拷贝至mycluster文件夹
declare -a IPS=(192.168.2.177...) #空格隔开需要安装的节点ip
CONFIG_FILE=inventory/mycluster/hosts.ini python3 contrib/inventory_builder/inventory.py ${IPS[@]}
# 根据需要修改k8s-cluster.yml中配置，目前针对内网环境不需要修改,其他需要根据情况修改k8s-cluster.yml中 docker_options中insecure-registry地址;helm_stable_repo_url地址等配置
# 注意：如果需要配置haproxy以及keepalived，需要按照需求修改k8s-cluster.yml中相应的配置项，以及roles/kubernetes/master/default/main.yml和roles/kubernetes/master/templates/haproxy.cfg,默认haproxy_keepalived为false
cp config/k8s-cluster.yml ../../../inventory/mycluster/group_vars/
cp config/main.yml ../../../roles/docker/tasks/
```

##### step 7 开始安装
```
# 在kubespray根目录下执行
sudo ansible-playbook -i inventory/mycluster/host.ini cluster.yml
# 查看是否安装成功
kubectl get node # 查看node是否ready
kubectl get pod -n kube-system # 查看所有的pod是否处于running状态
# 依次给节点打标签，标签格式为node=node_name
kubectl label node node_name node=node_name
# 依次根据机器显卡的类型及显存给节点打标签，标签格式为gpu=显卡类型/显存
kubectl lablel node node_name gpu=gputype-gpumemory
```

##### step 8 安装显卡插件
```
# 修改installation/postinstall/gpu/nvidia-device-plugin.yml 中image字段
kubectl create -f nvidia-device-plugin.yml
# 查看gpu资源, 可以在Capacity和Allocatable下看到nvidia.com/gpu字段
kubectl describe node node_name
```

##### TODO
1. 离线安装部分需要软件以离线安装包的形式安装，另一部分通过内网ubuntu源直接apt-get安装，后续可以将所有软件的安装源都部署到内网99.10web服务器，统一通过apt-get安装
2. 目前所有的python软件包只能通过外网下载离线包安装，需要找到一个解决方法
