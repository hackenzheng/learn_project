## kubectl debug
在实践中常用的方式是kubectl exec -it podname /bin/bash, 原理上在pod内起另外一个进程,跟原有的pod共享namespace。
这种方式调试需要所依赖的docker image安装了对应的工具，才能执行对应的命令。

另外一种思路是不需要为了调试而安装额外的工具，而是实现准备好这个工具，运行的时候启动一个新容器，并且加入到目标容器的pid,user, network以及ipc namespace中。

<kubectl-debug插件> https://github.com/aylei/kubectl-debug