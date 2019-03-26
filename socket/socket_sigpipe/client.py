# -*- coding: utf-8 -*-
import socket
import time
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 2222))
s.send(b'hello')
time.sleep(1)     # 睡眠过程中，对端已经退出，会close socket,发送fin包，此时操作系统有没有回收socket资源？，因为这边还没有发fin包
s.send(b'hello')  # 会写入到发送缓冲区，但发送的报文会导致对端发送rst包， 既然会rst包，socket资源是被回收了，从另一个角度，对端进程都已经退出了，资源自然回收
s.send(b'hello')
s.close()


"""
sigpipe信号: 客户端往关闭的socket继续写，第一次写会收到rst包，再次写就会生成sigpipe信号，该信号默认结束进程
"""