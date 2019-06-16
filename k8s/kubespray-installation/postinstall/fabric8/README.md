##### Deploy fabric8 platform on kubernetes cluster
```
helm repo add fabric8 https://fabric8.io/helm
helm fetch fabric8/fabric8-platform
# 解压下载下来的压缩文件，并修改exposecontroller-sa.yaml, fabric8-sa.yaml,configmapcontroller-sa.yaml以及exposecontroller-configmap.yaml,本例中已经修改好了
# 创建PersistentVolume,本例中以hostPath为例，需要将gogs-data对应的host文件夹的权限修改为777
kubectl create -f pv.yml
# 安装
helm install --name fabric8 fabric8-platform/
# Access dashboard
HOST_IP=$(kubectl get pod -l project=fabric8-console -o 'jsonpath={.items[0].status.hostIP}')
PORT=$(kubectl get svc fabric8 -o 'jsonpath={.spec.ports[0].nodePort}')
open brower: $HOST_IP:$PORT
```
