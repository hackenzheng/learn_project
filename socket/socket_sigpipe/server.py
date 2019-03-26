# -*- coding: utf-8 -*-
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('127.0.0.1', 2222))
s.listen(5)
c, addr = s.accept()
a=c.recv(1024)
print(a)
c.close()
print('a')