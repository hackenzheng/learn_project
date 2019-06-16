#!/usr/bin/env python
'''
Offline deployment neccessary step
update docker image repo url in "../../../roles/download/defaults/main.yml" and "../../../roles/kubernetes-apps/ansible/defaults/main.yml"
replace former url prefix with specified internal docker registry url and project name, for example: "192.168.99.10:5000/intellif-k8s/"
'''
import os
import yaml
import sys


def replace_prefix(prefix, yml_file):
    bk_file = yml_file + ".bk"
    os.system("cp %s %s" % (yml_file, bk_file))
    f = open(yml_file)
    dt = yaml.load(f)
    f.close()
    for k in dt.keys():
        if "image_repo" in k:
            v = dt[k]
            dt[k] = prefix + "/" + v.split("/")[-1] 
    f = open(yml_file, "w")
    yaml.dump(dt, f)
    f.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        replace_prefix("192.168.99.10:5000/intellif-k8s", "../../../roles/kubernetes-apps/ansible/defaults/main.yml")
        replace_prefix("192.168.99.10:5000/intellif-k8s", "../../../roles/download/defaults/main.yml")
    else:
        replace_prefix(sys.argv[1], "../../../roles/kubernetes-apps/ansible/defaults/main.yml")
        replace_prefix(sys.argv[1], "../../../roles/download/defaults/main.yml")

