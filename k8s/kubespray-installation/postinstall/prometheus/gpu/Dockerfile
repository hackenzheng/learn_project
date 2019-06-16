FROM nvidia/cuda:9.0-cudnn7-devel-ubuntu16.04
ADD sources.list sources.list
RUN cp sources.list /etc/apt && rm -rf /etc/apt/sources.list.d && \
    apt-get update && \
    apt-get install -y wget git python python-pip
RUN pip install nvidia-ml-py prometheus_client
RUN mkdir -p workdir
ADD nvidia-prometheus-stats.py workdir/nvidia-prometheus-stats.py
WORKDIR workdir
