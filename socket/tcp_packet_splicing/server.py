# -*- coding: utf-8 -*-
from socket import *
import time
server = socket(AF_INET, SOCK_STREAM)
server.bind(('127.0.0.1', 8080))
server.listen(5)

conn, client_addr = server.accept()

res1 = conn.recv(1)
print('第一次:', res1)
res2 = conn.recv(1024)
print('第二次:', res2)

time.sleep(3)
res2 = conn.recv(1024)
print('第三次:', res2)
time.sleep(3)
res2 = conn.recv(1024)
print('第四次:', res2)
conn.close()
server.close()


"""
参考: https://blog.csdn.net/miaoqinian/article/details/80020291
tcp粘包问题，是客户端和服务端之间需要发送有界限的数据流，需要能够正确的处理边界，不然会出现解析不完整的现象。
直观的现象是客户端一次发10个字节，而服务端每次只读取一个字节，并当做完整的，就出现了不匹配。
应用中http协议通过定义请求头响应头\r\n符号来解决
redis的通信协议中也需要解决此问题，不然读取到的命令不全
"""