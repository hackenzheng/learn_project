import redis
import socket

args = ('ping',)    # 也可以尝试info命令
command = redis.Connection().pack_command(*args)
print(command)

# 直接socket传输
address = ('127.0.0.1', 6379)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(address)
sock.sendall(command[0])
print(sock.recv(1024))

# 用redis-py传输并解析
conn = redis.Connection()
conn.send_command("info")
print(conn.read_response())  #返回的还是字节串(bytes)
