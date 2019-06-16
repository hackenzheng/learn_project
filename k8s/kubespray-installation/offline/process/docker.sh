#!/usr/bin/env bash

# docker
apt-get purge -y docker-ce
dpkg -i libltdl7_2.4.6-0.1_amd64.deb
dpkg -i libseccomp2_2.3.1-2.1ubuntu2_16.04.1_amd64.deb
dpkg -i docker-ce_18.03.1_ce-0_ubuntu_amd64.deb

# nvidia-docker
apt-get purge -y nvidia-docker2
dpkg -i libnvidia-container1_1.0.0~rc.2-1_amd64.deb
dpkg -i libnvidia-container-tools_1.0.0~rc.2-1_amd64.deb
dpkg -i nvidia-container-runtime-hook_1.3.0-1_amd64.deb
dpkg -i nvidia-container-runtime_2.0.0+docker18.03.1-1_amd64.deb
dpkg -i nvidia-docker2_2.0.3+docker18.03.1-1_all.deb
dpkg -i pigz_2.3.1-2_amd64.deb

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

rm *.deb

# netaddr
pip install netaddr-0.7.19-py2.py3-none-any.whl

# swapoff
swapoff -a
