## k8s调度gpu


<Kubernetes安装GPU支持插件> https://my.oschina.net/u/2306127/blog/1808304
<官方Schedule GPUs> https://kubernetes.io/docs/tasks/manage-gpus/scheduling-gpus/
<官方插件介绍> https://kubernetes.io/docs/concepts/extend-kubernetes/compute-storage-net/device-plugins/

## amd的gpu使用
amd gpu又叫dcu,不同于NVIDIA的cuda编程框架，amd使用的是rocm平台，也支持mxnet等多种框架，基础镜像使用rocm/dev-ubuntu-16.04