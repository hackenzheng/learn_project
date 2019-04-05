## 整体介绍
   传统的监控比如zabbix一般是监控物理机或者虚拟机上的cpu,网络等资源信息,需要在被监控的对象上安装一个agent,
   用于定期收集数据并上报。zabbix适合于监控机器，而不方便监控服务。在微服务场景中，通过docker起服务，需要监控到
   每个服务的运行状态，CPU等信息，在docker里面安装一个agent显得比较笨重，不方便。所以prometheus出来了，
   在每个微服务中提供一个http接口，用于传输metric信息，prometheus定时从这个接口去拉取，然后存储到自己的时序数据库。
   另外也提供了pushgateway,支持服务的metric主动push到gateway,但prometheus仍然是定期去gateway拉取。
   
   输出被监控组件信息的HTTP接口被叫做exporter，常用的组件大部分都有exporter可以直接使用，比如Nginx、MySQL
   
   Grafana可以作为Kibana的替代品，grafana也支持es数据源，可同时用于日志分析和监控信息的展示。
   grafana是用于可视化大型测量数据的开源程序，他提供了强大和优雅的方式去创建、共享、浏览数据。dashboard中显示了不同metric数据源中的数据。
   grafana有热插拔控制面板和可扩展的数据源，目前已经支持Graphite、InfluxDB、OpenTSDB、Elasticsearch等。

   grafana可以设置直接连接MySQL通过sql语句查询得到所需要的数据，在dashboard的json文件里面配置。

https://www.jianshu.com/p/339db34e4afe