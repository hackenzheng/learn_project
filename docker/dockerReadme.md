## 整体介绍
在kubeflow的分布式训练中，如果起的任务(pod)占的内存比较大，直接现象是宿主机的dockerd进程是是耗费很大内存，
会唤醒kswaped进程频繁的换页，大量消耗CPU。 拖慢服务器的响应，并且任何docker相关的命令都会卡住没有输出


docker源码及原理的解读：

<docker源码分析> https://www.kancloud.cn/infoq/docker-source-code-analysis/80525
<docker从入门到实战> https://yeasy.gitbooks.io/docker_practice/content/
实验楼教程<C++ 实现简易 Docker 容器 >  https://www.shiyanlou.com/courses/608

<美团-Linux资源管理之cgroups简介> https://tech.meituan.com/2015/03/31/cgroups.html


## docker操作
所有的容器数据都存在/var/lib/docker/aufs/diff/路径下, 一个容器的数据对应这其中的一个或多个目录。
其中目录名的前几位就是容器的ID，可以直接修改该路径下的文件，在docker中可以看到修改后的内容。


ubuntu docker安装：

    apt-get update
    apt-get install docker.io
    
    刚装好的docker每次使用docker命令都需要sudo，比较麻烦，可以通过以下命令省去sudo
    sudo usermod -aG docker 当前用户名  # 将当前用户添加到docker 分组, 然后重新登录
    
    
ENTRYPOINT不能被覆盖，CMD可以被覆盖，如果用的是ENTRYPOINT调试的时候可以是docker run -it --entrypoint=/bin/bash feiyu/entrypoint:1

相关操作：

查看docker中运行的进程在宿主机上对应的pid:  docker inspect -f '{{ .State.Pid }}' container_id

本地和容器之间拷贝数据 sudo docker cp host_path containerID:container_path

删除为none的image  

    sudo docker rmi $(sudo docker images | grep none | awk '{print$3}')
    sudo docker rm $(sudo docker ps -a | grep Exited | awk '{print$1}')
    sudo docker rmi $(sudo docker images | grep none | grep weeks | awk '{print$3}')
    kubectl delete pod -n kubeflow $(kubectl get pods -n kubeflow | grep new-train-test | grep Error | awk '{print$1}')

强制删除pod:  kubectl delete pod -n tsest gput  --grace-period=0 --force

k8s中pod重启进程： kill -9 $(ps -ef | grep gunicorn | sed -n '2p' |awk '{print$2}')

清理资源 docker system prune -a

## docker存储目录修改或扩容

docker 默认的存储路径在 /var/lib/docker下面,当镜像和容器比较多的时候会出现存储空间不够，需要移动到其他目录。

停止docker服务：

    systemctl stop docker 或service docker stop 

将已有的文件从/var/lib/docker移动到 /home/docker:

    cp -R /var/lib/docker/* /home/docker/     # 用mv会提示文件不存在

修改docker的systemd的 docker.service的配置文件:

    vim /usr/lib/systemd/system/docker.service  或者/etc/systemd/system/multi-user.target.wants/docker.service
    在EXECStart后面增加新的路径
    ExecStart=/usr/bin/dockerd --graph /home/docker
    
加载新的配置并重启docker服务：

    systemctl daemon-reload
    systemctl start docker



## docker 镜像
基础镜像有busybox和apline, busybox是有netstat等上百种linux工具，apline是一个面向安全的轻型linux发型版。

<alpine介绍> https://yeasy.gitbooks.io/docker_practice/cases/os/alpine.html