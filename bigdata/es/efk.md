## ekf日志采集平台

fluented 用于采集pod日志，pod的日志需要输出到文件，不能只输出到stdout。 fluented配置好日志的采集目录，就会从目录下去读取日志文件。

<elk docker-compose部署>https://github.com/deviantony/docker-elk