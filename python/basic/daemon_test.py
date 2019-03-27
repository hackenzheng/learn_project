# -*- coding:utf-8 -*-

def work():
    print("running")
    import time
    time.sleep(100)

import daemon
with daemon.DaemonContext(pidfile='/tmp/testdd.pi'):
    work()

