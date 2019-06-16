#!/usr/bin/env bash
  docker run -d \
  --name=osd_data1 \
  --net=host \
  --restart=always \
  --privileged=true \
  --pid=host \
  -v /etc/localtime:/etc/localtime \
  -v /data/ceph/etc:/etc/ceph \
  -v /data/ceph/lib:/var/lib/ceph \
  -v /data/ceph/logs:/var/log/ceph \
  -v /data1/osd:/var/lib/ceph/osd \
  ceph/daemon:latest osd
