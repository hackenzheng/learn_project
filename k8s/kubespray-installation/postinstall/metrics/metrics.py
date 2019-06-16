#!/usr/bin/python3.5
import socket
import time
import argparse
import os, sys, stat
import json
import logging
from kubernetes import client, config
from kubernetes.stream import stream

config.load_incluster_config()
k8s_coreapi = client.CoreV1Api()

logger = logging.getLogger("Metrics")
formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
console_handler = logging.StreamHandler(sys.stdout)
console_handler.formatter = formatter
logger.addHandler(console_handler)
logger.setLevel(logging.DEBUG)

def get_util_memory(pod_name, namespace, command=["/bin/sh", "-c", "ps -aux|awk '{print$3\" \"$4\" \"$11}';nvidia-smi | grep % |awk '{print$9\" \"$11\" \"$13}'"], ps="python"):
    cpu = None
    memory = None
    gpu_util_memory = [] 
    try:
        resp = stream(k8s_coreapi.connect_get_namespaced_pod_exec, pod_name, namespace,
                  command=command,
                  stderr=True, stdin=False,
                  stdout=True, tty=False)
        resp = resp.splitlines()
        for r in resp:
            if ps in r:
                temp = r.strip().split(" ")
                cpu = temp[0] + "%"
                memory = temp[1] + "%"
            if "MiB" in r:
                temp = r.split(" ")
                gpu_memory = temp[0] + "/" + temp[1]
                gpu_util = temp[2]
                device_usage = {"util": gpu_util, "memory": gpu_memory}
                gpu_util_memory.append(device_usage)
    except:
        logger.error("can not exec into pod %s in namespace %s" % (pod_name, namespace))
    return cpu, memory, gpu_util_memory


def get_node_name(namespace):
    current_pod_name = socket.gethostname() 
    pod = k8s_coreapi.read_namespaced_pod(current_pod_name, namespace)
    return pod.spec.node_name


def get_pods_by_nodename(node_name, namespace):
    pods_info = []
    pods = k8s_coreapi.list_namespaced_pod(namespace=namespace).items
    for pod in pods:
        if pod.spec.node_name == node_name and len(pod.spec.containers) == 1:
            pods_info.append(pod.metadata.name)
     
    return pods_info  


def main():
    parser = argparse.ArgumentParser(description='metrics')
    parser.add_argument('-n', '--namespace', type=str, default="kube-system", help='namespace current pod created in')
    parser.add_argument('-u', '--update-period', type=str, default="60", help='time interval to query for cpu/memory/gpu util')
    parser.add_argument('-p', '--path', type=str, default="/gfs/fl/metrics", help='shared path to store metrics files')
    args = parser.parse_args()
    namespace = args.namespace
    node_name = get_node_name(namespace)
    if not os.path.exists(args.path):
        os.makedirs(args.path)
        os.chmod(args.path, stat.S_IRWXU|stat.S_IRWXG|stat.S_IRWXO)
    while True:
        pods = get_pods_by_nodename(node_name, namespace)
        for i in range(len(pods)):
            pod_name = pods[i]
            cpu, memory, gpu = get_util_memory(pod_name, namespace)
            dct = {}
            if cpu and memory:
                logger.info("pod %s in namespace %s cpu and memory metrics gathered: cpu %s; memory %s" % (pod_name, namespace, cpu, memory))
                dct["cpu"] = cpu
                dct["memory"] = memory
            for j in range(len(gpu)):
                gpu_id = "device_"+ str(j)
                dct[gpu_id] = gpu[j]
                logger.info("pod %s in namespace %s gpu %d metrics gathered: util %s; memory %s" % (pod_name, namespace, j, gpu[j]["util"], gpu[j]["memory"]))
            if len(dct) != 0:
                f = open(os.path.join(args.path, pod_name), "w")
                f.write(json.dumps(dct))
                f.close() 
        time.sleep(float(args.update_period)) 


if __name__ == "__main__":
    main()
