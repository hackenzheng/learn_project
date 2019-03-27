# -*- coding: utf-8 -*-
import socket
import time
"""
服务端一直在listen状态，不读取数据,数据会进入到读缓冲区，当缓冲区满了后就不会继续接收，客户端就会阻塞
"""


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('127.0.0.1', 2222))
s.listen(5)
c, addr = s.accept()


time.sleep(1000)
a=c.recv(1024)
c.close()
