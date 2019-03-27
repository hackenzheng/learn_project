# -*- coding utf-8 -*-
import re
import os
import subprocess

if __name__ == "__main__":
    os.system('rm -rf /tmp/xfleet')
    os.system('mkdir -p /tmp/xfleet')
    p = subprocess.Popen('docker images', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():

        m = re.match(r'(^gcr.io[^\s]*\s*)\s([^\s]*\s)', line.decode("utf-8"))
        if not m:
            continue
        print("start to save ....")
        iname = m.group(1).strip(' ')
        # tag
        itag = m.group(2)

        tarname = iname.split('/')[-1]
        tarball = tarname + '.tar'
        ifull = iname + ':' + itag
        print("image is :" + ifull)
        print("save path is :" + tarball)
        #save
        cmd = 'docker save -o ' + tarball + ' ' + ifull
        os.system(cmd)

        #os.system('mv %s /tmp/xfleet/'%tarball)


retval = p.wait()
