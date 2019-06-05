## k8s安装部署

学习环境 用有minikube, k8s-for-desktop等项目。集群环境部署方式可以用rancher，kubeadm,kubespray, ansible等方式。
rancher最简单，屏蔽了很多过程，如果要学习安装过程中需要的组件可以用二进制的kubeadm。

kubespray和ansible的关系：

    kubespray本质是一堆ansible的role文件,通过ansible方式可以自动化的安装高可用k8s集群,目前支持1.9.
    <kubespray 中文安装指南> https://kubernetes.feisky.xyz/bu-shu-pei-zhi/cluster/kubespray
    
kubespray部署k8s：

    ansible安装
    sudo apt-add-repository ppa:ansible/ansible
    sudo apt-get update
    sudo apt-get install ansible
    
    kubespray安装
    wget https://github.com/kubernetes-incubator/kubespray/archive/v2.1.2.tar.gz
    tar -zxvf v2.1.2.tar.gz
    mv kubespray-2.1.2 kuberspray
    cd kubespray
    pip install -r requirements.txt  # 安装kubespray所需依赖包，包括ansible和jinja2
    
    IP=(172.31.84.155 172.31.84.156)   # 设置环境变量定义集群，ip为集群各个节点ip
    CONFIG_FILE=./kubespray/inventory/inventory.cfg python36 ./kubespray/contrib/inventory_builder/inventory.py ${IP[*]}
    
    vim ~./kubespray/inventory/inventory.cfg # 配置节点名和ip的关系, 也可以是其他文件比如scsz/hosts.ini，通过-i指定
    
    cd kubespray  # 替换gcr.io等镜像后用ansible部署
    ansible-playbook -i inventory/inventory.cfg cluster.yml -b -v --private-key=~/.ssh/id_rsa
    
    kubectl get node  #验证是否成功
    
    <使用Kubespray部署Kubernetes集群> https://blog.csdn.net/forezp/article/details/82730382
    
## k8s增加新节点

kubeadm新增：

    kubeadm join 192.168.111.130:6443 --token [token] --discovery-token-ca-cert-hash [sha256]
    其中token通过kubectl token list获取，每个token只有24小时的有效期，如果没有有效的token可以创建kubectl token create
    
    Kubernetes认证的SHA256加密字符串
    openssl x509 -pubkey -in /etc/kubernetes/pki/ca.crt | openssl rsa -pubin -outform der 2>/dev/null | openssl dgst -sha256 -hex | sed 's/^.* //'

kubespray新增：
    
    关闭防火墙
    systemctl stop firewalld
    systemctl disable firewalld
    
    kubespray安装目录下的host.ini文件， 例如inventory/mycluster/hosts.ini，必须与原有k8s集群的相同，增加新的结点
    
    扩容 ansible-playbook -i inventory/mycluster/hosts.ini scale.yml
    官方说明 https://github.com/kubernetes-sigs/kubespray/blob/master/docs/getting-started.md
    
