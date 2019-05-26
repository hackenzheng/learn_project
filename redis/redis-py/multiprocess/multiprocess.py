# redis-py做到了多进程安全
import time
import multiprocessing

import redis

r = redis.Redis(host='127.0.0.1', port=6379, db=0)

def func(msg):
    for i in range(30):
        time.sleep(1)
        print(r.keys())
    return "done " + msg


if __name__ == "__main__":
    pool = multiprocessing.Pool(processes=4)
    result = []
    for i in range(4):
        msg = "hello %d" %(i)
        result.append(pool.apply_async(func, (msg, )))
    pool.close()
    pool.join()
    for res in result:
        print(res.get())
    print("Sub-process(es) done.")