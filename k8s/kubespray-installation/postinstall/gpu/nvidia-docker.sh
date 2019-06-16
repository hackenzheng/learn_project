#!/usr/bin/env bash

#nvidia-docker
apt-get purge -y nvidia-docker
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | \
  apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/ubuntu16.04/amd64/nvidia-docker.list | \
  tee /etc/apt/sources.list.d/nvidia-docker.list
apt-get update
apt-get install -y nvidia-docker2

tee /etc/docker/daemon.json <<EOF
{
    "default-runtime": "nvidia",
    "runtimes": {
        "nvidia": {
            "path": "/usr/bin/nvidia-container-runtime",
            "runtimeArgs": []
        }
    }
}
EOF
pkill -SIGHUP dockerd
systemctl restart docker.service
