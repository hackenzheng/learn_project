import socket
import time

"""
阻塞和非阻塞io的对比，
"""

def blocking_way():
    print('start ..' + str(time.time()))
    sock = socket.socket()
    print(time.time())
    sock.connect(('www.baidu.com', 80))
    print(time.time())
    request = 'GET / HTTP/1.0\r\nHost: www.baidu.com\r\n\r\n'
    req_str = request.encode('ascii')
    print(req_str)
    sock.send(req_str)
    response = b''
    chunk = sock.recv(10)
    print(type(chunk))
    print(chunk)
    while chunk:
        response += chunk
        print('====')
        print(time.time())
        chunk = sock.recv(4096)
        print(time.time())

    return response


def nonblocking_way():
    sock = socket.socket()
    sock.setblocking(False)

    try:
        # 不管是否连接成功，不进行等待，在write数据的时候再处理
        print(time.time())
        ret = sock.connect(('www.baidu.com', 80))
        print(time.time())
        print('connect return =====')
        print(ret)
    except BlockingIOError as e:
        print(e)
    request = 'GET / HTTP/1.0\r\nHost: www.baidu.com\r\n\r\n'
    req_str = request.encode('ascii')

    print('start to send **************')
    while True:
        try:
            ret = sock.send(req_str)
            print('send return =====++++++++')
            print(ret)
            break
        except OSError as e:
            print(e)

    response = b''
    while True:
        try:
            chunk = sock.recv(4096)
            print('chunk ....')
            print(chunk)
            while chunk:
                response += chunk
                print(time.time())
                chunk = sock.recv(4096)
                print(time.time())
                print('--------------------------')
                print(chunk)
            break
        except OSError as e:
            print(e)
    return response


def main():
    ret = nonblocking_way()
    print(ret)


if __name__ == '__main__':
    main()