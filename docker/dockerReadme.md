## 整体介绍
在kubeflow的分布式训练中，如果起的任务(pod)占的内存比较大，直接现象是宿主机的dockerd进程是是耗费很大内存，
会唤醒kswaped进程频繁的换页，大量消耗CPU。 拖慢服务器的响应，并且任何docker相关的命令都会卡住没有输出


docker源码及原理的解读：

<docker源码分析> https://www.kancloud.cn/infoq/docker-source-code-analysis/80525
<docker从入门到实战> https://yeasy.gitbooks.io/docker_practice/content/
实验楼教程<C++ 实现简易 Docker 容器 >  https://www.shiyanlou.com/courses/608

<美团-Linux资源管理之cgroups简介> https://tech.meituan.com/2015/03/31/cgroups.html


## 
所有的容器数据都存在/var/lib/docker/aufs/diff/路径下, 一个容器的数据对应这其中的一个或多个目录。
其中目录名的前几位就是容器的ID，可以直接修改该路径下的文件，在docker中可以看到修改后的内容。