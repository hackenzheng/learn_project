#### Metrics Gathering Guide
1. 构建docker image
```
sh build.sh
```
2. 构建DaemonSet
```
# 根据需要修改metrics.yaml中的docker image路径以及metrics volume的主机路径
kubectl create -f metrics.yaml
```
