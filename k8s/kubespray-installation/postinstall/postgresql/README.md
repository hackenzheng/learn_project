##### helm 安装postgresql
1. 创建ROOK Storage Class
```
kubectl create -f rook/operator.yaml
kubectl create -f rook/cluster.yaml
kubectl create -f rook/rook-storage.yaml
```

2. helm安装
```
git clone -b dev-zb https://gitlab.com/intellif/charts.git
helm install --name postgresql -f values.yaml charts/stable/postgresql
```

##### postgres连接测试
```
# 获取密码
PGPASSWORD=$(kubectl get secret --namespace kube-system postgres-postgresql -o jsonpath="{.data.postgres-password}" | base64 --decode; echo)
# 连接测试，在default命令空间起一个pod连接postgres
kubectl run --namespace default postgres-postgresql-client --restart=Never --rm --tty -i --image postgres \
   --env "PGPASSWORD=$PGPASSWORD" \
   --command -- psql -U postgres \
   -h postgres-postgresql.kube-system postgres
```
