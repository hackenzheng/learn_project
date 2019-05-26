from redis.connection import PythonParser

# 模拟对响应的解析


data = b'+OK\r\n'
pp = PythonParser(socket_read_size=65536)
pp.on_connect(data)
print(pp.read_response())
