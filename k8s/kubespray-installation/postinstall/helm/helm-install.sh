#!/usr/bin/env bash

# install helm client
wget https://storage.googleapis.com/kubernetes-helm/helm-v2.8.0-linux-amd64.tar.gz
tar -zxvf helm-v2.8.0-linux-amd64.tar.gz
sudo mv linux-amd64/helm /usr/local/bin/helm
rm -rf helm-v2.8.0-linux-amd64.tar.gz linux-amd64/

# install tiller server
helm init --upgrade -i registry.cn-hangzhou.aliyuncs.com/google_containers/tiller:v2.8.0

# Role-based Access Control
kubectl create serviceaccount --namespace kube-system tiller
kubectl create clusterrolebinding tiller-cluster-rule --clusterrole=cluster-admin --serviceaccount=kube-system:tiller
kubectl patch deploy --namespace kube-system tiller-deploy -p '{"spec":{"template":{"spec":{"serviceAccount":"tiller"}}}}'
