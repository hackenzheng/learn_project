# -*- coding: utf-8 -*-
import socket
import time
"""
客户端一直写,因为服务端不会读，当服务端的缓冲区满了之后就会阻塞，因为发不出去了. 当服务端读取一部分之后那么就可以接着发送
"""

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 2222))
while True:
    s.send(b'hello world')

s.close()

