## k8s部署机器学习等应用

### gluoncv训练yolo模型做物体检测的shm-size设置
问题：使用gluocv, voc数据集，yolo模型训练物体检测，在服务器直接运行没有问题，若docker运行或k8s运行会出现卡死的现象，
通过strace分析可以看到进程阻塞在read等系统调用

原因：共享内存过小，要设大一点https://discuss.gluon.ai/t/topic/8443/21

解决方法： 
若是docker启动，运行时加-shm-size选项。 docker通过修改daemon.json的文件方式不可行，"default-shm-size":"64M"
这个配置加到daemon.json文件中docker会启动失败。

k8s本身只提供cpu和memory的配置，没提供shm-size的配置，https://github.com/kubernetes/kubernetes/issues/28272。
修改daemon.json的方式也不可行。 可行的方式是把/dev/shm挂载到内存。参考https://stackoverflow.com/questions/46085748/define-size-for-dev-shm-on-container-engine/46434614#46434614



