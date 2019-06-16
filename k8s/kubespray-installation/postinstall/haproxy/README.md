##### Apiserver haproxy and keepalived
```
sudo mkdir /etc/kubernetes/haproxy
sudo cp haproxy.cfg /etc/kubernetes/haproxy
sudo cp keepalived.yml haproxy.yaml /etc/kubernetes/manifests
sudo systemctl restart kubelet.service
# Access Dashboard via VIP https://192.168.2.154:30090
# Access haproxy_stats via VIP http://192.168.2.154:9090/haproxy_stats
```
