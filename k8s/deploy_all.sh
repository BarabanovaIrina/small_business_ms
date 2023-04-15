#!/bin/sh

# 1. Clone the repo and change into the nginx-kubernetes-gateway directory:
git clone https://github.com/nginxinc/nginx-kubernetes-gateway.git
cd nginx-kubernetes-gateway

# 2. Install the Gateway API resources from the standard channel (the CRDs and the validating webhook):
kubectl apply -f https://github.com/kubernetes-sigs/gateway-api/releases/download/v0.6.2/standard-install.yaml

# 3. Create the nginx-gateway Namespace:
kubectl apply -f deploy/manifests/namespace.yaml

# 4. Create the njs-modules ConfigMap:
kubectl create configmap njs-modules --from-file=internal/nginx/modules/src/httpmatches.js -n nginx-gateway

# 5. Create the GatewayClass resource:
kubectl apply -f deploy/manifests/gatewayclass.yaml

# 6. Deploy the NGINX Kubernetes Gateway:
kubectl apply -f deploy/manifests/nginx-gateway.yaml

# 7. Confirm the NGINX Kubernetes Gateway is running in nginx-gateway namespace:
kubectl get pods -n nginx-gateway

# 8. Create a Service with type NodePort:
kubectl apply -f deploy/manifests/service/nodeport.yaml

sleep 5
# 9. deploying our apps
cd ..
sh ./small_business_ms/k8s/deploy_services.sh

# 10. Wait for nginx-gateway pod status Running
sleep 5

# 10. bingind port to ngingx gateway
NGINX_GW_POD_NAME=$(kubectl get pods -n nginx-gateway --no-headers -o custom-columns=":metadata.name")
kubectl -n nginx-gateway port-forward $NGINX_GW_POD_NAME 8080:80 8443:443
