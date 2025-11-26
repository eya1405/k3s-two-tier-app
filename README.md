Lab 5: Deploying a Two-Tier Web Application on K3s
Overview
This project demonstrates deploying a two-tier application on a K3s Kubernetes cluster.
The architecture consists of:

Frontend: A Flask web application that allows users to submit and view data.
Backend: A PostgreSQL database storing the submitted data.

The application is deployed using Kubernetes Deployments and Services in the namespace lab5.

Architecture
[ User ] ---> [ NodePort Service ] ---> [ Flask Web App Pod ]
                                   |
                                   v
                          [ ClusterIP Service ]
                                   |
                                   v
                          [ PostgreSQL Pod ]


Project Structure
two-tier-app/
├── app/                # Flask application
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── k8s/                # Kubernetes manifests
│   ├── namespace.yaml
│   ├── db-deployment.yaml
│   ├── db-service.yaml
│   ├── web-deployment.yaml
│   └── web-service.yaml
├── scripts/
│   └── install.sh      # Automation script
└── README.md


Prerequisites

A running K3s cluster
kubectl configured to access the cluster
Docker installed and logged in to Docker HubLab 5: Deploying a Two-Tier Web Application on K3s
Overview
This project demonstrates deploying a two-tier application on a K3s Kubernetes cluster.
The architecture consists of:

Deployment Steps
1. Clone the Repository

git clone <your-repo-url>
cd two-tier-app
2. Build and Push the Web App Image

cd app
docker build -t najaheya/lab5-web:v1 .
docker login -u najaheya
docker push najaheya/lab5-web:v1

3. Apply Kubernetes Manifests

cd ../k8s
kubectl apply -f namespace.yaml
kubectl apply -f db-deployment.yaml
kubectl apply -f db-service.yaml
kubectl apply -f web-deployment.yaml
kubectl apply -f web-service.yaml
4. Verify Resources
kubectl -n lab5 get all
You should see:

db-deployment and web-deployment pods running
db-service (ClusterIP)
web-service (NodePort)


Access the Application
Find the NodePort:
kubectl -n lab5 get svc web-service


Default NodePort: 30080
Access via:
http://<node-ip>:30080

Test the Application

Submit a name and email using the form.
Refresh the page to see stored entries.


Validate Database
(Optional) Connect to PostgreSQL pod:
kubectl -n lab5 exec -it $(kubectl -n lab5 get pod -l app=lab5-db -o name) -- psql -U lab5user -d lab5db

Run:

SELECT * FROM entries;


Automation
Run the install script:
cd scripts
chmod +x install.sh
./install.sh
