#!/bin/sh

# Supposed to be run out of the project repository
kubectl apply -f small_business_ms/k8s/gateway.yml

sleep 5

kubectl apply -f small_business_ms/accounting/k8s/deployment.yml
kubectl apply -f small_business_ms/accounting/k8s/route.yml

kubectl apply -f small_business_ms/sales/k8s/deployment.yml
kubectl apply -f small_business_ms/sales/k8s/route.yml

kubectl apply -f small_business_ms/warehouse/k8s/deployment.yml
kubectl apply -f small_business_ms/warehouse/k8s/route.yml
