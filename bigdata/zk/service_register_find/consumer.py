# 服务发现消费者
import json
import kazoo

zk = KazooClient(hosts="127.0.0.1:2181")
zk.start()
zk_root = '/demo'
servers = set()
for child in zk.get_children(zk_root):  # 获取子节点名称
    node = zk.get(zk_root + "/" + child)  # 获取子节点 value
    addr = json.loads(node[0])
    servers.add("%s:%d" % (addr["host"], addr["port"]))
    servers = list(servers)       # 转成列表


# def callback(*args):
#     new_children = zk.get_children(zk_root, watch=callback)  # 继续 watch
#
# children = zk.get_children(zk_root, watch=callback)  # 增加 watch 参数