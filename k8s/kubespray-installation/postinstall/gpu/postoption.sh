#!/usr/bin/env bash
for ip in $@
do
  echo $ip
  ssh -o StrictHostKeyChecking=no root@$ip < nvidia-docker.sh 
done
