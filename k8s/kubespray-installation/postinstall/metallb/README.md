##### Metallb
- Reference
1.[https://metallb.universe.tf/](https://metallb.universe.tf/)
2.[https://github.com/google/metallb](https://github.com/google/metallb)

- Deployment
```
# basic
kubectl create -f metallb.yaml
# get available ip for loadbalance in current network segment and modify metallb-config.yaml
# deploy config
kubectl create -f metallb-config.yaml
```
- Expose service with type=LoadBalancer 
