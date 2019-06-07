## docker compose
用于定义和运行多个docker容器的应用，dockerfile只适用于单一应用的容器，需要多个应用配合的应用就可以用docker-compose实现。
它允许用户通过一个单独的 docker-compose.yml 模板文件来定义一组相关联的应用容器为一个项目。Compose 项目由 Python 编写，实现上调用了 Docker 服务提供的 API 来对容器进行管理。

Compose 中有两个重要的概念：

    服务 (service)：一个应用的容器，实际上可以包括若干运行相同镜像的容器实例。
    项目 (project)：由一组关联的应用容器组成的一个完整业务单元，在 docker-compose.yml 文件中定义。
    
    
安装：

    Docker for Mac 自带 docker-compose 二进制文件，安装 Docker 之后可以直接使用
    Ubuntu下 sudo pip install -U docker-compose
    或者 curl -L https://raw.githubusercontent.com/docker/compose/1.8.0/contrib/completion/bash/docker-compose > /etc/bash_completion.d/docker-compose
    

使用：
    
    使用dockerfile构建镜像
    编写docker-compose.yml文件
    """
    version: '3'
    services:
      web:
        image: "web"
        command:
         - /bin/bash 
        ports:
         - "5000:5000"
      redis:
        image: "redis:alpine"
    """
    运行项目 docker-compose up   

运行docker-compose目录下要有docker-compose.yml文件，docker-compose有多个选项，类似于docker命令，只不过是针对的都是一组服务或镜像。
一份标准配置文件应该包含 version、services， version指的是compose文件格式版本而非服务的版本，目前为止有三个大版本分别为Version 1,Version 2,Version 3。
对于有依赖关系的服务之间，可以通过depends_on标签来解决，比如数据库要先在web服务之前启动。