import time
import threading


# 新线程执行的代码:
def loop():
    print('thread %s is running...' % threading.current_thread().name)
    n = 0
    while n < 5:
        n = n + 1
        print('thread %s >>> %s' % (threading.current_thread().name, n))
        time.sleep(2)
    print('thread %s ended.' % threading.current_thread().name)


def loop2():
    print('thread %s is running...' % threading.current_thread().name)
    n = 0
    while n < 5:
        n = n + 1
        print('thread %s >>> %s' % (threading.current_thread().name, n))
        time.sleep(2)
        raise Exception('thread 2 report')
    print('thread %s ended.' % threading.current_thread().name)

print('thread %s is running...' % threading.current_thread().name)
t = threading.Thread(target=loop, name='LoopThread')
t2 = threading.Thread(target=loop2, name='LoopThread2')
time1 = time.time()
t2.start()
t.start()
t.join()
t2.join()
print(time.time() - time1)
print('thread %s ended.' % threading.current_thread().name)