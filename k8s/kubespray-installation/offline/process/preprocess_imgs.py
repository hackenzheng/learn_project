#!/usr/bin/env python
import os
import argparse

def decompression(tar_path):
    path = os.getcwd()
    os.chdir(tar_path)
    os.system("tar -xvf %s" % os.path.join(tar_path, r"k8s-1.10.4.tar"))
    os.chdir(path)


def load(tar_path, old_tag_file):
    img_path = os.path.join(tar_path, r"k8s-1.10.4")
    f = open(old_tag_file, "w")
    for img in os.listdir(img_path):
        if ".tar" in img:
            cmd = "docker load -i %s" % os.path.join(img_path, img)
            out = os.popen(cmd).read()
            print(out)
            if "Loaded" in out:
                url = out.splitlines()[-1].strip().split(" ")[-1]
                f.write(url+"\n") 
    f.close() 
           

def tag(prefix, old_tag_file, new_tag_file):
    f = open(old_tag_file, "r")
    nt = open(new_tag_file, "w")
    while 1:
        line = f.readline()
        if not line:
            break
        line = line.strip()
        tag = prefix + "/" + line.split("/")[-1]
        os.system("docker tag %s %s" % (line, tag))
        nt.write(tag+"\n")
    f.close()
    nt.close()


def push(tag_file):
    f = open(tag_file, "r")
    while 1:
        line = f.readline()
        if not line:
            break
        line = line.strip()
        os.system("docker push %s" % line)
    f.close()


def rmi(tag_file):
    f = open(tag_file, "r")
    while 1:
        line = f.readline()
        if not line:
            break
        line = line.strip()
        os.system("docker rmi %s" % line)
    f.close()


def process(tar_path, old_tag, new_tag, prefix):
    decompression(tar_path)
    load(tar_path, old_tag)
    tag(prefix, old_tag, new_tag)
    push(new_tag)
    rmi(old_tag)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='docker images processing,process order: decom,load,tag,push,rmi')
    parser.add_argument('--tar-path', type=str, default="../images", help='')
    parser.add_argument('--old-tag', type=str, default="old-tag.lst", help='')
    parser.add_argument('--new-tag', type=str, default="new-tag.lst", help='')
    parser.add_argument('--prefix', type=str, default="192.168.99.10:5000/intellif-k8s", help='')
    parser.add_argument('--option', type=str, default="all", help='')
    args = parser.parse_args()
    if args.option == "all":
        process(args.tar_path, args.old_tag, args.new_tag, args.prefix)
    elif args.option == "decom":
        decompression(args.tar_path)
    elif args.option == "load":
        load(args.tar_path, args.old_tag)
    elif args.option == "tag":
        tag(args.prefix, args.old_tag, args.new_tag)
    elif args.option == "push":
        push(args.new_tag)
    elif args.option == "rmi":
        rmi(args.old_tag) 
