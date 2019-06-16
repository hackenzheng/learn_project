#!/usr/bin/env bash
docker run -d \
  --net=host \
  --name=mds \
  --restart=always \
  --privileged=true \
  -v /etc/localtime:/etc/localtime \
  -v /data/ceph/etc:/etc/ceph \
  -v /data/ceph/lib:/var/lib/ceph \
  -v /data/ceph/logs:/var/log/ceph \
  -e CEPHFS_CREATE=0 \
  -e CEPHFS_METADATA_POOL_PG=512 \
  -e CEPHFS_DATA_POOL_PG=512 \
  ceph/daemon:latest mds

