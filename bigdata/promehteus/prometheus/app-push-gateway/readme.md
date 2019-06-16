用于自建服务监控push-gateway,项目中的服务将metric推到该服务器，prometheus再从这里拉取数据。
python server.py即可启动
python client.py 模拟去读metrics

缺少DockerFile

需要应用代码将数据push到gateway-server