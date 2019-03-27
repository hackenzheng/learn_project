
from gevent.server import StreamServer
from config import *

def httpd(socket, addr):
    while True:
        line = socket.recv(1024)
        if EOL1 in line or EOL2 in line:
            break
    socket.sendall(response)
            
ser = StreamServer(('0.0.0.0', 8080), httpd)
ser.serve_forever()
