# Kubernetes Multi-Container Setup

This repo sets up a Flask app and MySQL database on Kubernetes using GKE.

## Prerequisites

- **Google Cloud SDK** and **kubectl** installed.
- A **GKE Cluster** created.

## Setup

### 1. **Create a GKE Cluster**
```bash
gcloud container clusters create <CLUSTER_NAME> --zone <ZONE> --num-nodes=3
2. Configure kubectl
bash
Copy
gcloud container clusters get-credentials <CLUSTER_NAME> --zone <ZONE> --project <PROJECT_ID>
3. Deploy Resources
Deploy Flask and MySQL services:

bash
Copy
kubectl apply -f flask-app-deployment.yaml
kubectl apply -f mysql-db-deployment.yaml
4. Verify Deployment
Check the status of deployments, pods, and services:

bash
Copy
kubectl get deployments
kubectl get pods
kubectl get svc
5. Access Flask App
Get the external IP of the Flask service:

bash
Copy
kubectl get svc flask-app-service
File Structure
flask-app-deployment.yaml: Flask app deployment and service.
mysql-db-deployment.yaml: MySQL deployment, service, and persistent volume.
Flask App Environment Variables
RDS_HOST: MySQL RDS Host.
RDS_PORT: MySQL Port (default: 3306).
RDS_USER: MySQL username.
RDS_PASSWORD: MySQL password.
RDS_DB_NAME: MySQL database name.
yaml
Copy

---

### `flask-app-deployment.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: flask-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: flask-app
  template:
    metadata:
      labels:
        app: flask-app
    spec:
      containers:
        - name: flask-app
          image: darshan616/flask.app:latest
          ports:
            - containerPort: 5000
          env:
            - name: RDS_HOST
              value: "darshan.cj4oqcie8m6x.ap-south-1.rds.amazonaws.com"
            - name: RDS_PORT
              value: "3306"
            - name: RDS_USER
              value: "admin"
            - name: RDS_PASSWORD
              value: "Local_1234567"
            - name: RDS_DB_NAME
              value: "darshan"
---
apiVersion: v1
kind: Service
metadata:
  name: flask-app-service
spec:
  selector:
    app: flask-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 5000
  type: LoadBalancer
mysql-db-deployment.yaml
yaml
Copy
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mysql-db
spec:
  replicas: 1
  selector:
    matchLabels:
      app: mysql-db
  template:
    metadata:
      labels:
        app: mysql-db
    spec:
      containers:
      - name: mysql-db
        image: mysql:latest
        ports:
        - containerPort: 3306
        env:
        - name: MYSQL_ROOT_PASSWORD
          value: "my-secret-pw"
        - name: MYSQL_DATABASE
          value: "mydb"
        volumeMounts:
        - name: mysql-data
          mountPath: /var/lib/mysql
      volumes:
      - name: mysql-data
        persistentVolumeClaim:
          claimName: mysql-data

---
apiVersion: v1
kind: Service
metadata:
  name: mysql-db-service
spec:
  ports:
  - port: 3306
    targetPort: 3306
  selector:
    app: mysql-db
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mysql-data
spec:
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
Key Commands
Create GKE Cluster:

bash
Copy
gcloud container clusters create <CLUSTER_NAME> --zone <ZONE> --num-nodes=3
Configure kubectl:

bash
Copy
gcloud container clusters get-credentials <CLUSTER_NAME> --zone <ZONE> --project <PROJECT_ID>
Deploy App and Database:

bash
Copy
kubectl apply -f flask-app-deployment.yaml
kubectl apply -f mysql-db-deployment.yaml
Check Deployment Status:

bash
Copy
kubectl get deployments
kubectl get pods
kubectl get svc
Get External IP for Flask App:

bash
Copy
kubectl get svc flask-app-service
