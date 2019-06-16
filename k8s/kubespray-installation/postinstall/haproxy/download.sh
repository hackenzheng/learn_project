#!/usr/bin/env bash
CORE_URL="https://kairen.github.io/files/manual-v1.10/master"
files=(kube-apiserver kube-controller-manager kube-scheduler haproxy keepalived etcd etcd.config)
for FILE in ${files[@]}
do
  wget "${CORE_URL}/${FILE}.yml.conf" -O ${FILE}.yml
done
