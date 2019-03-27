#!/usr/bin/env python

"""
simple server
run as:
    1. ./t_baseline.py
    2. use browser open 'http://localhost:8080'.
    3. siege -c 100 -r 10 -b http://localhost:8080
"""

import socket

from config import *

ser_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ser_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ser_socket.bind(('0.0.0.0', 8080))
ser_socket.listen(100)

try:
    while True:
        conn, addr = ser_socket.accept()
        request = b''
        while EOL1 not in request and EOL2 not in request:
            request += conn.recv(1024) 
        conn.send(response)
        conn.close()
finally:
    ser_socket.close()
