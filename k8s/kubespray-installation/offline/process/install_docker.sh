#!/usr/bin/env bash
for ip in $@
do
  echo $ip
  scp -r ../requirements/netaddr/netaddr-0.7.19-py2.py3-none-any.whl ../debs/* root@$ip:~/
  ssh -o StrictHostKeyChecking=no root@$ip < docker.sh
done
