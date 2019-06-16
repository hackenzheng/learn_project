##### 设置指定用户（示例用户dev）使用有限kubectl权限
1. 生成相关认证证书
```
openssl genrsa -out dev-key.pem 2048
openssl req -new -key dev-key.pem -out dev.csr -subj "/CN=dev"
openssl x509 -req -in dev.csr -CA /etc/kubernetes/ssl/ca.pem -CAkey /etc/kubernetes/ssl/ca-key.pem -CAcreateserial -out dev.pem -days 1095
```

2. 创建训练专用的namespace mxnet
```
kubectl create -f namespace.yaml
```

3. 设置kubectl配置文件
```
cp /etc/kubernetes/admin.conf dev.kubeconfig
#设置客户端认证参数:
kubectl config set-credentials dev \
 --client-certificate=/path/to/dev.pem \
 --client-key=/path/to/dev-key.pem \
 --embed-certs=true \
 --kubeconfig=/path/to/dev.kubeconfig
#设置上下文参数：
kubectl config set-context dev-context \
 --cluster=cluster.local \
 --user=dev \
 --namespace=mxnet \
 --kubeconfig=/path/to/dev.kubeconfig
#设置默认上下文：
kubectl config use-context dev-context --kubeconfig=/path/to/dev.kubeconfig
```

4. 生成Role并指定Role权限，并绑定到user dev
```
#可以根据情况修改相关内容
kubectl create -f role.yaml
kubectl create -f rolebinding.yaml
kubectl create -f clusterrole.yaml
kubectl create -f clusterrolebinding.yaml
```

5. 使用新的config文件
```
cp /path/to/dev.kubeconfig /home/dev/.kube/config
```
6. 参考博客

[https://www.kubernetes.org.cn/3238.html](https://www.kubernetes.org.cn/3238.html)

[https://docs.bitnami.com/kubernetes/how-to/configure-rbac-in-your-kubernetes-cluster/](https://docs.bitnami.com/kubernetes/how-to/configure-rbac-in-your-kubernetes-cluster/)

[http://blog.csdn.net/shenshouer/article/details/53035948](http://blog.csdn.net/shenshouer/article/details/53035948)
