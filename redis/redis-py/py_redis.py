import logging
import redis     # pip install redis 或者 从github下载源码后python setup.py install

REDIS_IP = 'localhost'
REDIS_PORT = '6379'
REDIS_USER = 'admin'
REDIS_PASSWD = 'admin'


class PyRedis(object):
    def __init__(self, db=0):
        #pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
        #self.redis_obj = redis.Redis(connection_pool=pool)
        self.redis_obj = redis.Redis(host=REDIS_IP, port=REDIS_PORT, db=db)

    def close(self):
        pass

    def set(self, key, value):
        if not isinstance(key, str):
            return False

        try:
            self.redis_obj.set(key, value)
        except Exception as e:
            logging.info('set database error %s' % e)
            return False
        return True

    def get(self, key):
        if not isinstance(key, str):
            return False

        try:
            ret = self.redis_obj.get(key)
            return ret
        except Exception as e:
            print 'set database error %s' % e
            return False

    def hset(self, name, key, value):
        try:
            self.redis_obj.hset(name, key, value)
        except Exception as e:
            logging.info('insert hash item error %s' % e)
            return False
        return True

    def hgetall(self, name):
        try:
            return self.redis_obj.hgetall(name)
        except Exception as e:
            logging.info('get hash item error %s' % e)
            return False

    def hget(self, name, field):
        try:
            return self.redis_obj.hget(name, field)
        except Exception as e:
            logging.info('get hash item error %s' % e)
            return False

    def get_all_key(self):
        return self.redis_obj.keys()

    def del_key(self, key):
        try:
            return self.redis_obj.delete(key)
        except Exception as e:
            logging.info('delete key error %s' % e)
            return False


if __name__ == "__main__":
    redis_obj = PyRedis()
    # ret = redis_obj.set('sz', 'ft')
    # print redis_obj.get('sz')
    k_list = redis_obj.get_all_key()
    print k_list
    for k in k_list:
        #redis_obj.del_key(k)
        print redis_obj.hgetall(k)

