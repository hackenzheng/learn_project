#!/usr/bin/env python

"""
simple server
run as:
    1. ./t_epoll_level.py
    2. use browser open 'http://localhost:8080'.
    3. siege -c 100 -r 10 -b http://localhost:8080
"""

import socket
import select

from config import *

ser_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ser_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ser_socket.bind(('0.0.0.0', 8080))
ser_socket.listen(50)
ser_socket.setblocking(0)

epoll = select.epoll()
epoll.register(ser_socket.fileno(), select.EPOLLIN)

try:
    conns = {}
    requs = {}
    resps = {}
    while True:
        events = epoll.poll(10)
        for fileno, event in events:
            if fileno == ser_socket.fileno():
                conn, addr = ser_socket.accept()
                conn.setblocking(0)
                epoll.register(conn.fileno(), select.EPOLLIN)
                conns[conn.fileno()] = conn
                requs[conn.fileno()] = b''
                resps[conn.fileno()] = response
            elif event & select.EPOLLIN:
                requs[fileno] += conns[fileno].recv(1024)
                if EOL1 in requs[fileno] or EOL2 in requs[fileno]:
                    epoll.modify(fileno, select.EPOLLOUT)
            elif event & select.EPOLLOUT:
                bw = conns[fileno].send(resps[fileno])
                resps[fileno] = resps[fileno][bw:]
                if len(resps[fileno]) == 0:
                    epoll.modify(fileno, 0)
                    conns[fileno].shutdown(socket.SHUT_RDWR)
            elif event & select.EPOLLHUP:
                epoll.unregister(fileno)
                conns[fileno].close()
                del conns[fileno]
finally:
    epoll.unregister(ser_socket.fileno())
    epoll.close()
    ser_socket.close()




