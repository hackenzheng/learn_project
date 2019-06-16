1. format and mount bricks
```
mkfs.xfs -i size=2048 disk-name or partition-name(/dev/sdc)
mkdir -p /data/brick1
mount /dev/sdc /data/brick1
tip: you can use a directory as brick, and you can skip the steps above
```

2. install glusterfs //run on every nodes
```
add-apt-repository ppa:gluster/glusterfs-3.10
apt-get update
apt-get install glusterfs-server
iptables -I INPUT -p all -s <ip-address> -j ACCEPT //ip address of other nodes
```

3. configure cluster
```
gluster peer probe node1 //on node2
```

4. set up glusterfs volume
```
gluster volume create gv0 replica 2 node1:/data/brick1/gv0 node2:/data/brick1/gv0
gluster volume start gv0
```

5. some useful commands
```
gluster peer status
gluster volume info
```

6. client
```
apt-get install glusterfs-client //glusterfs-client was installed when installing glusterfs-server on server node
mount -t glusterfs node1:/gv0 /mnt
```

7. set up on k8s
```
kubectl create -f glusterfs-ep.json
kubectl create -f glusterfs-sv.json
# use case
kubectl create -f glusterfs-pod.json
```
