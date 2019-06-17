# 服务发现生产者
import json
import kazoo   # 访问zk的Python客户端

zk = kazoo.KazooClient(hosts="localhost:2181")
zk.start()  # 启动客户端，尝试连接
value = json.dumps({"host": "127.0.0.1", "port": 8080})
zk.ensure_path("/demo")  # 确保根节点存在，如果没有会自动创建
# 创建顺序临时节点，这就是服务列表中的一个子服务地址信息
zk.create("/demo/rpc", value, ephemeral=True, sequence=True)
# 关闭 zk 会话，关闭客户端，否则临时节点不会立即消失
zk.stop()