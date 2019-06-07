## helm介绍

docker是其单一的应用，docker-compose可以起多个相关的应用，但都在同一个服务器上，而k8s上同一组服务的不同应用可以起在不同的服务器上。
k8s管理和部署应用最直接的方式是写yaml文件，但如果一个应用包含十几个服务，而且需要各种volume,配置也比较多，直接写yaml文件是比较复杂，
有helm和ks可以简化管理和部署,虽然用到的yaml文件还是得事先写好。

最开始都是基于yaml文件来进行部署发布的，当项目变大拆分成微服务化或者模块化，会分成很多个组件来部署，每个组件可能对应一个deployment.yaml,
一个service.yaml,一个Ingress.yaml，还可能存在各种依赖关系。这样一个项目如果有5个组件，很可能就有15个不同的yaml文件，这些yaml分散存放，
如果某天进行项目恢复的话，很难知道部署顺序，依赖关系等。 通过helm来解决yaml配置的集中存放，项目的打包和组件间的依赖。


Helm 采用客户端/服务器架构，由如下组件组成：

    Helm CLI 是 Helm 客户端，可以在 Kubernetes 集群的 master 节点或者本地执行。
    Tiller 是服务器端组件，在 Kubernetes 集群上运行，并管理 Kubernetes 应用程序的生命周期。
    Repository 是 Chart 存储库，Helm 客户端通过 HTTP 协议来访问存储库中 Chart 的索引文件和压缩包。


基本概念：

    Chart：helm的包， 包含了运行一个应用所需要的镜像、依赖和资源定义等yaml文件，比如pgsql.tgz的包就包含启动pgsql所有需要的文件
    Release：在 Kubernetes 集群上运行的 Chart 的一个实例。一个 Chart 可以安装很多次。
    例如一个 MySQL Chart，如果想在服务器上运行两个数据库，就可以把这个 Chart 安装两次。每次安装都会生成自己的 Release
    Repository：用于发布和存储 Chart 的存储库。chart可以存放在本地，但不方便

helm可以作为yaml模板渲染引擎，
helm template compose > generated-docker-compose.yml


## helm安装

在能够执行kubectl的服务器上安装客户端
`curl https://raw.githubusercontent.com/kubernetes/helm/master/scripts/get | bash`

安装服务端tiller `help init --upgrade`

在本地构建chart 包：

    一个应用可能需要deployment.yaml, service.yaml, values.yaml
    helm package ./   将三个文件打包成tgz的包，在本地应用可以不打包，打包是为了方便第三方使用
    
    而标准的chart至少包括
    (1)应用的基本信息 Chart.yaml
    (2)一个或多个 Kubernetes manifest 文件模版（放置于 templates/ 目录中），可以包括 Pod、Deployment、Service 等各种 Kubernetes 资源
    (3)模板默认值 values.yaml （可选）

Helm 管理依赖的方式：

    把依赖的 package 放在 charts/ 目录中， 比如web应用需要pgsql, 就会把pgsql的chart包放到本地的charts目录
    在requirements.yaml中配置

安装本地应用 `helm install --name service-name chart-path`

更新本地应用 `helm upgrade flbackend --set flbackend.deployment.image=192.168.2.46:5000/aios/flbackend:0.2 charts/flbackend`