## 基于k8s的机器学习平台

类似托拉拽的平台有TAI,PAI,先知平台，任务都是以docker形式运行，通过k8s等平台调度任务。

机器学习的过程一般包括数据处理(特征工程)，训练，推理，预测，部署等。模型的评估可以是在训练的过程中同时对验证集的数据进行预测，然后计算得到验证集上的精度，
也可以在模型训练完之后。TAI等平台的评估只做accuracy等指标的计算，不做预测，假定输入的数据是预测过的带标签，选择特征列和标签列就可以。

阿里的存储分为maxcompute和oss,maxcompute是数据库,用于存放结构化数据, oss是块存储,存放非结构化数据.通过PAI命令来执行的py脚本,不直接执行py脚本。
阿里pai中的oss同步组件是将oss上的文件拉取下来，再maxcompute生成一张临时的表。腾讯tai one中访问cos路径要目录需以${cos}开头,是用于区分容器本地文件，阿里的访问oss也是加前缀。