#!/usr/bin/env bash

docker run -d \
  --net=host \
  --name=rbd \
  --restart=always \
  --privileged=true \
  -v /etc/localtime:/etc/localtime \
  -v /data/ceph/etc:/etc/ceph \
  -v /data/ceph/lib:/var/lib/ceph \
  -v /data/ceph/logs:/var/log/ceph \
  ceph/daemon:latest rbd_mirror
