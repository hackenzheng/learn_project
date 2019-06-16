###### Deploy Kong and Kong proxy
1. Create PersistenVolume to persist postgresql
```
kubectl create -f pv.yml
```

2. Create Kong related sources
```
kubectl create -f all-in-one-postgres.yaml
```

3. Get envs
```
export KONG_ADMIN_PORT=$(kubectl get svc -n kong kong-ingress-controller -o 'jsonpath={.spec.ports[0].nodePort}')
export KONG_ADMIN_IP=$(kubectl get pod -l app=ingress-kong -n kong -o 'jsonpath={.items[0].status.hostIP}')
export PROXY_IP=$(kubectl get pod -l app=kong -n kong -o 'jsonpath={.items[0].status.hostIP}')
export HTTP_PORT=$(kubectl get svc -n kong kong-proxy -o 'jsonpath={.spec.ports[0].nodePort}')
export HTTPS_PORT=$(kubectl get svc -n kong kong-proxy -o 'jsonpath={.spec.ports[1].nodePort}')
```

4. Deploy service examples
```
kubectl create -f httpsvc.yaml
kubectl create -f my-nginx.yaml
# ingress
kubectl create -f ingress.yaml
# tls ingress
# step 1 generate certs，press "Enter" till end
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout tls.key -out tls.crt
# step2 create k8s secret
kubectl create secret tls tls-secret --key tls.key --cert tls.crt -n kong
# step3 create secure ingress
kubectl create -f ingress_tls.yaml
```

5. Test
```
# insecure access
http ${PROXY_IP}:${HTTP_PORT} Host:foo.bar
http ${PROXY_IP}:${HTTP_PORT} Host:my.nginx
# another access way
http_proxy=${PROXY_IP}:${HTTP_PORT} curl -v http://foo.bar
http_proxy=${PROXY_IP}:${HTTP_PORT} curl -v http://my.nginx
# secure access
curl -v -k --resolve secure.foo.bar:${HTTPS_PORT}:${PROXY_IP} https://secure.foo.bar:${HTTPS_PORT}
curl -v -k --resolve secure.my.nginx:${HTTPS_PORT}:${PROXY_IP} https://secure.my.nginx:${HTTPS_PORT}
```

6. Add rate limiting plugin
```
kubectl create -f kong_plugin.yaml
```

7. Retest will get ratelimit statistics

8. Deploy konga (Kong dashboard)
```
kubectl create -f konga.yaml
export KONGA_IP=$(kubectl get pod -l app=konga -n kong -o 'jsonpath={.items[0].status.hostIP}')
export PORT=$(kubectl get svc -n kong konga -o 'jsonpath={.spec.ports[0].nodePort}')
# Access via http://${KONGA_IP}:${PORT}
# Admin login: admin | password: adminadminadmin
# Demo user login: demo | password: demodemodemo
```

