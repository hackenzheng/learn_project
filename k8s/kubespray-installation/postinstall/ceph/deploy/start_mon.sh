#!/usr/bin/env bash
docker run -d \
  --net=host \
  --name=mon \
  --restart=always \
  -v /etc/localtime:/etc/localtime \
  -v /data/ceph/etc:/etc/ceph \
  -v /data/ceph/lib:/var/lib/ceph \
  -v /data/ceph/logs:/var/log/ceph \
  -e MON_IP=192.168.2.156,192.168.2.46,192.168.2.177 \
  -e CEPH_PUBLIC_NETWORK=192.168.2.0/24 \
  ceph/daemon:latest mon
