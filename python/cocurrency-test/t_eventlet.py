from eventlet import api
from config import *

def httpd(socket):
    while True:
        line = socket.recv(1024)
        if EOL1 in line or EOL2 in line:
            break
    socket.sendall(response)

ser = api.tcp_listener(('0.0.0.0', 8080))
while True:
    conn,addr = ser.accept()
    api.spawn(httpd, conn)

