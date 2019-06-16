##### helm 安装kafka
1. 如果使用local persistent volume,需要分别创建6个pv和pvc
```
kubectl create -f zookeeper-pv.yml kafka-pv.yml
```
2. 下载修改过的charts
```
git clone -b dev-zb git@gitlab.com:intellif/charts.git
```
3. 使用local persistent volume时需要根据pv的位置给对应的node打标签，然后相应的修改charts/incubator/kafka中相应的nodeSelector字段

4. 安装
```
cd charts
helm dep build ./incubator/kafka
helm install --name release-name ./incubator/kafka
```
