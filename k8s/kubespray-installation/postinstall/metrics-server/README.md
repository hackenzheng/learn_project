#### 安装metrics-server
1. 修改/etc/kubernetes/kubelet.env
```
--read-only-port=0 修改为 --read-only-port=10255
```
2. 命令行部署
```
kubectl create -f 1.8+/
```
