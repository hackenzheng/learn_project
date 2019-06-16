##### In cluster Load balancer
- Reference: [https://github.com/munnerz/keepalived-cloud-provider](https://github.com/munnerz/keepalived-cloud-provider)
- Steps:
1. Install kube-keepalived-vip
```
kubectl create -f vip-daemonset.yaml
# Attention: image "kube-keepalived-vip:0.9" should be replaced by "aledbf/kube-keepalived-vip:0.27"
```
2. Set --cloud-provider=external on our kube-controller-manager master component
```
modify /etc/kubernetes/manifests/kube-controller-manager.manifest
```
3. Deploy keepalived-cloud-provider
```
kubectl create -f keepalived-cloud-provider.yaml
```
4. Create a service with type=LoadBalancer
