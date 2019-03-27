"""
多线程CPU使用率测试，机器是4核，跑起来通过top查看CPU只有125%左右，而不是400%
python多线程由于GIL的存在，利用不了多核的优势。而IO密集型的多线程仍然是高效的，
因为线程在等待io的时候是会释放GIL的, Ctypes库可以解决该问题
"""
from threading import Thread

def test():
    i = 0
    while True:
        print('i===%d' %i)
        i += 1


for i in range(4):
    t = Thread(target=test)
    t.start()



