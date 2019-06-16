###  在线部署kubernetes
#### (一)部署kubernetes集群

##### step 1 安装所需要的环境依赖
```
sudo pip install -r requirements.txt
```

##### step 2 ssh 免密登录
需要保证当前节点root用户能ssh免密码登录到所有节点的root用户
使用命令ssh-copy-id

##### step 3 更新集群节点配置
```
declare -a IPS=(10.10.1.3 10.10.1.4 10.10.1.5)
CONFIG_FILE=inventory/mycluster/hosts.ini python3 contrib/inventory_builder/inventory.py ${IPS[@]}
# ps: 可以根据需要手动修改host.ini配置文件
```

##### step 4 关闭所有节点交换分区并安装python-netaddr
```
sh preinstall/preoption.sh ${IPS[@]}
```

##### step 5 根据需要安装组件的需求更新配置文件
inventory/mycluster/group_vars/k8s-cluster.yml

##### step 6 开始安装
```
sudo ansible-playbook -i inventory/mycluster/host.ini cluster.yml
# 查看是否安装成功
kubectl get node # 查看node是否ready
kubectl get pod -n kube-system # 查看所有的pod是否处于running状态
# 依次给节点打标签，标签格式为node=node_name
kubectl label node node_name node=node_name
# 依次根据机器显卡的类型及显存给节点打标签，标签格式为gpu=显卡类型/显存
kubectl lablel node node_name gpu=gputype-gpumemory
```

##### step 7 暴露GPU资源
1. 保证每台机器都安装了nvidia显卡驱动
2. 每台机器安装nvidia-docker，可以参考postinstall/gpu目录下的nvidia-docker.sh进行安装，也可以按照以下步骤安装
```
cd postinstall/gpu
sh postoption.sh ${IPS[@]}
```

3. 安装k8s nvidia plugin
```
kubectl create -f postinstall/gpu/nvidia-device-plugin.yml
# 查看gpu资源, 可以在Capacity和Allocatable下看到nvidia.com/gpu字段
kubectl describe node node_name
```

#### (二)卸载kubernetes集群
```
sudo ansible-playbook -i inventory/mycluster/host.ini reset.yml
```

#### (三)增加节点
1. 将需要加入的节点信息写入inventory/mycluster/host.ini
2. 执行

```
sudo ansible-playbook -i inventory/mycluster/host.ini scale.yml
```

3. 重新apiserver对应的pod(否则master节点无法通过hostname访问其他节点上的pod)

#### (四) 其他集群组件安装
1. metrics gathering
```
# gpu,cpu,memory metrics gathering plugin(optional for mxnet distributed training)
# 详细可参考installation/postinstall/metrics/README.md
kubectl create -f installation/postinstall/metrics/metrics.yaml
```

2. prometheus and grafana
参考installation/postinstall/prometheus

### 离线部署kubernetes参考./offline/README.md

