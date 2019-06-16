#!/usr/bin/env bash
# kubernetes apiserver bind port 8080， so RGW_CIVETWEB_PORT changed to 8083
docker run -d \
  --net=host \
  --name=rgw \
  --restart=always \
  --privileged=true \
  -v /etc/localtime:/etc/localtime \
  -v /data/ceph/etc:/etc/ceph \
  -v /data/ceph/lib:/var/lib/ceph \
  -v /data/ceph/logs:/var/log/ceph \
  -e RGW_CIVETWEB_PORT=8083 \
  ceph/daemon:latest rgw
