import redis

args = ('PING',)

# 将redis命令安装redis的协议编码,返回编码后的数组,如果命令很大,返回的是编码后chunk的数组
packed_command = redis.Connection().pack_command(*args)
print(packed_command)  # 输出[b'*1\r\n$4\r\nPING\r\n']