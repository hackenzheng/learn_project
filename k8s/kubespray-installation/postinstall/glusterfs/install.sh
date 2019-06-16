#!/usr/bin/env bash

cd ../../contrib/network-storage/glusterfs
ansible-playbook -i inventory.cfg glusterfs.yml
