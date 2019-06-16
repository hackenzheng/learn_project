- Deploy istio to kubernetes
1. Reference: [https://istio.io/docs/setup/kubernetes/](https://istio.io/docs/setup/kubernetes/)
2. Deploy:
```
kubectl delete namespace istio-system
kubectl create -f istio.yaml
```

- Bookinfo example
1. Reference: [https://istio.io/docs/guides/bookinfo/](https://istio.io/docs/guides/bookinfo/)
```
Version v1 doesn’t call the ratings service.
Version v2 calls the ratings service, and displays each rating as 1 to 5 black stars.
Version v3 calls the ratings service, and displays each rating as 1 to 5 red stars.
```

2. Deploy:
```
# Deploy bookinfo app
kubectl label namespace default istio-injection=enabled
kubectl create -f bookinfo.yaml
kubectl create -f bookinfo-gateway.yaml
export INGRESS_PORT=$(kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.spec.ports[?(@.name=="http")].nodePort}')
export INGRESS_HOST=$(kubectl get po -l istio=ingressgateway -n istio-system -o 'jsonpath={.items[0].status.hostIP}')
export GATEWAY_URL=$INGRESS_HOST:$INGRESS_PORT
# Access via browser: http://${GATEWAY_URL}/productpage
```

3. Intelligent Routing:
```
# Request routing
kubectl create -f route-rule-all-v1.yaml # Set the default version for all microservices to v1
kubectl replace -f route-rule-reviews-test-v2.yaml # User “jason” by routing productpage traffic to reviews:v2 instances
# Fault injection
kubectl replace -f route-rule-ratings-test-abort.yaml # User “jason” product ratings not available
# Traffic Shifting
kubectl delete -f route-rule-all-v1.yaml
kubectl create -f route-rule-all-v1.yaml
kubectl replace -f route-rule-reviews-50-v3.yaml # reviews v1 and v3 weight 50%:50%
kubectl replace -f route-rule-reviews-v3.yaml # reviews v3 100%
```

4. Expose nginx service
```
kubectl create -f my-nginx.yaml
kubectl delete -f bookinfo-gateway.yaml
kubectl create -f gateway.yaml
# Access nginx service on browser: http://${GATEWAY_URL}/nginx
```

5. Watch jaeger web UI
```
export JAEGER_HOST=$(kubectl get po -l app=jaeger -n istio-system  -o 'jsonpath={.items[0].status.hostIP}')
export JAEGER_PORT=$(kubectl get svc tracing -n istio-system -o 'jsonpath={.spec.ports[0].nodePort}')
# Access on browser: http://$JAEGER_HOST:$JAEGER_PORT
```

6. Watch grafana dashboard
```
export GRAFANA_HOST=$(kubectl get po -l app=grafana -n istio-system  -o 'jsonpath={.items[0].status.hostIP}')
export GRAFANA_PORT=$(kubectl get svc -l app=grafana -n istio-system -o 'jsonpath={.spec.ports[0].nodePort}')
# Access on browser: http://$GRAFANA_HOST:$GRAFANA_PORT
```
