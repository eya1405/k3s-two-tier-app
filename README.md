Lab 6: Deploying a Two-Tier Web Application with ConfigMaps and Secrets on K3s

✅ Overview
This lab extends Lab 5 by introducing ConfigMaps and Secrets for better configuration management and security.
We deploy a two-tier application on a K3s cluster:

Frontend: Flask web app (form to insert and display data)
Backend: PostgreSQL database


🎯 Objectives

Externalize configuration using ConfigMap for non-sensitive data.
Secure credentials using Secret.
Deploy both components in the lab6 namespace.
Expose the web app via NodePort and keep the database internal via ClusterIP.
Architecture
[ Browser ] ---> [ NodePort Service: web-service ] ---> [ Flask App Pod ]
                                               |
                                               v
                                   [ ClusterIP Service: db-service ]
                                               |
                                               v
                                      [ PostgreSQL Pod ]
Project Structure
two-tier-app/
├── app/                # Flask app + Dockerfile
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── k8s/                # Kubernetes manifests
│   ├── namespace.yaml
│   ├── configmap.yaml
│   ├── secret.yaml
│   ├── db-deployment.yaml
│   ├── db-service.yaml
│   ├── web-deployment.yaml
│   └── web-service.yaml
├── scripts/
│   ├── install.sh      # Automates build, push, and apply
│
└── README.md
Deployment Steps
1. Create Namespace: 
kubectl apply -f k8s/namespace.yaml

2. Build and Push Web App Image


cd app
docker build -t <dockerhub-username>/lab6-web:v1 .
docker push <dockerhub-username>/lab6-web:v1

3. Apply ConfigMap and Secret: 

kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml

4. Deploy Database and Service: 

kubectl apply -f k8s/db-deployment.yaml
kubectl apply -f k8s/db-service.yaml

5. Deploy Web App and Service

kubectl apply -f k8s/web-deployment.yaml
kubectl apply -f k8s/web-service.yaml


6. Verify: 

kubectl -n lab6 get all
kubectl -n lab6 rollout status deploy/web-deployment
kubectl -n lab6 rollout status deploy/db-deployment
Access the App

Find Node IP:
kubectl get nodes -o wide
Open in browser:

http://<node-ip>:30081
Test Instructions

1-Submit a name and email via the form.
2-Refresh the page → Data should appear in the list.
3-Verify in PostgreSQL:

kubectl -n lab6 exec -it $(kubectl -n lab6 get pod -l app=lab6-db -o jsonpath='{.items[0].metadata.name}') -- \
psql -U lab6user -d lab6db -c "SELECT * FROM entries;"
# two-tier-app-lab6
