# -*- coding: utf-8 -*-
import os
import sys
import subprocess
import re


# 将一组镜像重新retag(包括修改仓库库名和版本号)并且push到镜像仓库, 只适合三段式的


def image_retag(old_registry, old_repo, new_registry, new_repo, push=True, new_tag=''):
    """
    比如将registry.cn-shenzheng.aliyuncs/aios_demo/aios_demo_test:10 retag 成 192.168.99.10:5000/aios_dev/aios_demo_test:latest
    :return:
    """
    p = subprocess.Popen('docker images', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    regexp_str = old_registry + '/' + old_repo

    for image in p.stdout.readlines():
        m = re.match(r'(^%s[^\s]*\s*)\s([^\s]*\s)'%regexp_str, image.decode("utf-8"))
        if not m:
            continue

        print("start to save ....")
        image_full_name = m.group(1).strip(' ')
        image_tag = m.group(2).strip(' ')
        print(image_full_name)
        tmp = image_full_name.split('/')
        if len(tmp) != 3:
            print(tmp)
            continue
        image_name = tmp[-1]

        if new_tag:
            image_tag = new_tag
        new_full_name = new_registry + '/' + new_repo + '/' + image_name + ':' + image_tag


        cmd = 'docker tag %s %s' % (image_full_name + ':' + image_tag, new_full_name)
        print(cmd)
        # os.system(cmd)

        if push:
            cmd = 'docker push %s' % new_full_name
            #os.system(cmd)

    retval = p.wait()



if __name__ == "__main__":
    image_retag('luanpeng', 'lp', '192.168.1.1', 'aios', push=False, new_tag='latest')
