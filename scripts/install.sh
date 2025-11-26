#!/usr/bin/env bash
set -euo pipefail

# Config
NAMESPACE="lab5"
IMAGE="najaheya/lab5-web:v1"

echo "[1/5] Creating namespace (if not exists)"
kubectl get ns "${NAMESPACE}" >/dev/null 2>&1 || kubectl apply -f k8s/namespace.yaml

echo "[2/5] Building web image"
docker build -t "${IMAGE}" ./app

echo "[3/5] Docker login (Docker Hub)"
if ! docker info | grep -q "Username: najaheya"; then
  echo "Enter Docker Hub password for user 'najaheya':"
  docker login -u "najaheya"
fi

echo "[4/5] Pushing image"
docker push "${IMAGE}"

echo "[5/5] Applying Kubernetes manifests"
kubectl apply -f k8s/db-deployment.yaml
kubectl apply -f k8s/db-service.yaml
kubectl apply -f k8s/web-deployment.yaml
kubectl apply -f k8s/web-service.yaml

echo "Done. Check status with: kubectl -n ${NAMESPACE} get all"
