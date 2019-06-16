##### 下载charts到本地
```
git clone -b dev-zb https://gitlab.com/intellif/charts.git
```

##### helm安装prometheus
1. 根据需要修改prom-values.yml中persistent volume 的size，accsess mode和claim name, 可以通过nodeSelector字段将pv绑定到指定节点
2. 根据1中的修改创建pv和pvc，默认alert manager和server分别需要一个pvc，可以对prom-pv.yml中相应内容进行修改，然后执行
```
kubectl create -f prom-pv.yml
```

3. 执行安装命令
```
helm install --name my-prometheus -f prom-values.yml path/to/charts/stable/prometheus
```

##### helm安装grafana
1. 根据需要修改gra-values.yml中相关内容,可以通过nodeSelector字段将pv绑定到指定节点
2. 创建pv
```
kubectl create -f gra-pv.yml
```

3. 执行安装
```
helm install --name my-grafana -f values.yaml path/to/charts/stable/grafana
```

##### helm 卸载应用
```
helm del --purge package-name
```
