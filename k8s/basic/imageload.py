import os
import sys


def load_fix_dir(workdir = '/tmp/xfleet-images'):
    # load指定目录的镜像
    tarball = sys.argv[1]
    print(tarball)

    os.system('rm -rf %s'%workdir)
    os.system('mkdir -p %s'%workdir)
    ret = os.system('tar -zxvf %s -C %s'%(tarball, workdir))
    print('tar consume...')

    os.chdir(workdir)
    files = os.listdir(workdir)
    for filename in files:
        print(filename)
        if filename.endswith('tar'):
            os.system('docker load -i %s'%filename)


def load_current_dir():
    # load当前目录的镜像,将imageload.py放到目录下，然后执行即可
    files = os.listdir('./')
    for filename in files:
        print(filename)
        if filename.endswith('tar'):
            os.system('docker load -i %s'%filename)


if __name__ == "__main__":
    load_current_dir()
