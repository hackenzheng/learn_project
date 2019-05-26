import time
import threading
import redis

r = redis.Redis(host='127.0.0.1', port=6379, db=0)

def func():
    for i in range(30):
        print(r.keys())
        time.sleep(1)
    return "done "


if __name__ == "__main__":
    task = []
    for i in range(5):
        t1 = threading.Thread(target=func)
        task.append(t1)
    for i in task:
        i.start()

    for i in task:
        i.join()
