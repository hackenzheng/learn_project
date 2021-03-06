## docker pull gcr.io镜像

拉取gcr.io等镜像需要翻墙，在有梯子以及设置好shadowsocks的基础上进行：

安装privoxy设置全局代理：

    sudo apt-get install python-m2crypto privoxy
    修改配置文件/etc/privoxy/config如下两行
        listen-address localhost:8118   # 本地接收请求的端口
        forward-socks5 / 127.0.0.1:1080 .   # shadowsocks的代理端口， 末尾的.不能去掉
    sudo service privoxy restart
    
docker代理设置：
    
    mkdir -p /etc/systemd/system/docker.service.d  # 如果没有就创建
    vim /etc/systemd/system/docker.service.d/http-proxy.conf # 创建http代理文件，写入如下配置
    
    [Service]
    Environment="HTTPS_PROXY=http://127.0.0.1:8118"
    
    # 还可以设置指定的镜像不走代理"NO_PROXY=localhost,127.0.0.1,docker-registry.somecorporation.com"
    
    ###Flush changes:
    systemctl daemon-reload
    
    ###Restart Docker:一定要通过重启让配置生效
    systemctl restart docker
    
    systemctl show --property=Environment docker  #查看修改结果
    
    就可以尝试pull gcr.io类的镜像，一定是重启docker才能让代理生效


    
直接用别人封装好的代理，没有试过： https://mritd.me/2017/02/09/gcr.io-registy-proxy/

registry.cn-hangzhou.aliyuncs.com/google_containers 替换 gcr.io

## 阿里云镜像仓库使用
登录到阿里云的容器镜像服务管理控制台，如果registry的密码忘了，在访问凭证的地方可以重置

创建命名空间，在命名空间里面再创建镜像。可以手动创建镜像，并指定镜像从哪里构建，比如是github还是gitlab。
如果不通过代码构建，将命名空间设置公有，可以直接docker push。

在本地登录阿里云仓库
sudo docker login --username=hackenzheng registry.cn-shenzhen.aliyuncs.com
输入密码进行授权，第一个密码是本地sudo权限需要的密码，别弄混了
 
将本地的镜像重新tag:
sudo docker tag gcr.io/ml-pipeline/persistenceagent:0.1.16 registry.cn-shenzhen.aliyuncs.com/kfp/persistenceagent:0.1.16

推送到云端，这样在公有镜像里面就能够搜索到
sudo docker push registry.cn-shenzhen.aliyuncs.com/kfp/persistenceagent:0.1.16


## 使用dockerhub拉取gcr.io的镜像
使用dockerhub作为代理，能够拉取gcr.io等被墙的镜像，dockerhub注册时的验证码也需要翻墙才能刷出来，正常的登录不用。

步骤是：

    将github关联到dockerhub, 新建一个repository，在build里面设置自动构建，需要设置build context(用于指定子目录)和dockerfile location
    编写Dockerfile，以grc.io等镜像为基础镜像，FROM gcr.io/google_containers/example-guestbook-php-redis:v3，提交到github就会自动触发构建，
    也可以手动触发构建。

 

