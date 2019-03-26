# -*- coding: utf-8 -*-
from socket import *
import time
client = socket(AF_INET, SOCK_STREAM)
client.connect(('127.0.0.1', 8080))

client.send(b'hello')
# time.sleep(1)
client.send(b'world')
time.sleep(1)
client.close()