#!/usr/bin/env bash
# https://github.com/kubernetes/dashboard/wiki/Certificate-management
openssl genrsa -des3 -passout pass:x -out dashboard.pass.key 2048
openssl rsa -passin pass:x -in dashboard.pass.key -out dashboard.key
rm dashboard.pass.key
openssl req -new -key dashboard.key -out dashboard.csr
openssl x509 -req -sha256 -days 365 -in dashboard.csr -signkey dashboard.key -out dashboard.crt
mkdir -p certs
mv dashboard.crt dashboard.key certs
kubectl delete -f dashboard-admin.yaml
kubectl delete -f kubernetes-dashboard.yaml
kubectl create secret generic kubernetes-dashboard-certs --from-file=cert/s -n kube-system
kubectl create -f dashboard-admin.yaml
kubectl create -f kubernetes-dashboard.yaml
