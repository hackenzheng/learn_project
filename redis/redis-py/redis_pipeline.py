"""
尽管redis-py中使用了连接池，但每次在执行请求时都会创建和断开一次连接操作（连接池申请连接，归还连接池），
如果想要在一次请求中执行多个命令，则可以使用 pipline 实现一次请求执行多个命令.
redis-py默认在一次pipeline中的操作是原子的，要改变这种方式，可以传入transaction=False
"""
import redis

pool = redis.ConnectionPool(host='10.211.55.4', port=6379)
r = redis.redis(connection_pool=pool)
# pipe = r.pipeline(transaction=False)

pipe = r.pipeline(transaction=True)

r.set('name', 'nick')
r.set('age', '18')

pipe.execute()