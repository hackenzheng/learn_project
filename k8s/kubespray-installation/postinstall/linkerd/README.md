##### Linkerd-namerd Deployment
1. Namerd管理dtabs规则，同时可以通过namerdctl修改规则
```
# 部署namerd
kubectl create -f namerd.yaml
NAMERD_HOST_IP=$(kubectl get po -l app=namerd -o 'jsonpath={.items[0].status.hostIP}')
curl http://$NAMERD_HOST_IP:$(kubectl get svc namerd -o 'jsonpath={.spec.ports[2].nodePort}')
# 本地安装namerctl
wget https://dl.google.com/go/go1.10.3.linux-amd64.tar.gz
sudo tar -C /usr/local -xzf go1.10.3.linux-amd64.tar.gz
cat << ~/.bashrc >> EOF
export PATH=$PATH:/usr/local/go/bin:~/go/bin
EOF
source ~/.bashrc
export NAMERCTL_BASE_URL=http://$NAMERD_HOST_IP:$(kubectl get svc namerd -o 'jsonpath={.spec.ports[1].nodePort}')
namerdctl help
```

2. 部署Linkerd
```
kubectl create -f linkerd-namerd.yaml
L5D_HOST_IP=$(kubectl get po -l app=l5d -o 'jsonpath={.items[0].status.hostIP}')
open http://$L5D_HOST_IP:$(kubectl get svc l5d -o 'jsonpath={.spec.ports[3].nodePort}')
```

3. Helloworld 样例
```
kubectl create -f hello-world-legacy.yaml
L5D_INGRESS_LB=$L5D_HOST_IP:$(kubectl get svc l5d -o 'jsonpath={.spec.ports[0].nodePort}')
curl $L5D_INGRESS_LB
```

4. Nginx样例
```
kubectl create -f nginx.yaml
namerdctl update external config
curl $L5D_INGRESS_LB
```

##### 待更新
1. Service Promethues/grafana Dashboard
```
kubectl create -f linkerd-viz.yml
VIZ_HOST_IP=$(kubectl get po -l name=linkerd-viz -o jsonpath="{.items[0].status.hostIP}")
VIZ_PORT=$(kubectl get svc linkerd-viz -o 'jsonpath={.spec.ports[0].nodePort}')
open http://$VIZ_HOST_IP:$VIZ_PORT
```

2. Add TLS
```
# Secret
kubectl create -f certificates.yml
# Remove former daemonset and service
kubectl delete ds/l5d configmap/l5d-config svc/l5d
# Recreate daemonset
kubectl create -f linkerd-tls.yml
# Access
http_proxy=$HOST_IP:$(kubectl get svc l5d -o 'jsonpath={.spec.ports[0].nodePort}') curl -s http://hello
# Skip tls curl
curl -skH 'l5d-dtab: /svc=>/#/io.l5d.k8s/default/admin/l5d;' https://$HOST_IP:$(kubectl get svc l5d -o 'jsonpath={.spec.ports[1].nodePort}')/admin/ping
```
