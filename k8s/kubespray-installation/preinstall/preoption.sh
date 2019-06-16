#!/usr/bin/env bash
for ip in $@
do
  echo $ip
  ssh -o StrictHostKeyChecking=no root@$ip "swapoff -a;apt-get update;apt-get install -y python-netaddr"
done
