Kubernetes Multi-Container Single Pod Deployment
This guide demonstrates how to deploy a multi-container pod in Kubernetes, where one container runs a Flask application, and the other container runs MySQL. Both containers are in the same pod, making it easy to run them together.

Steps to Deploy a Multi-Container Pod in Kubernetes
1. Create a YAML File for the Deployment
Create a file named single-pod-deployment.yaml to define a pod with two containers: one for Flask and one for MySQL.

yaml
Copy
apiVersion: apps/v1
kind: Deployment
metadata:
  name: single-pod-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: single-pod-app
  template:
    metadata:
      labels:
        app: single-pod-app
    spec:
      containers:
        - name: flask-container
          image: darshan616/flask.app:latest  # Replace with your Flask image
          ports:
            - containerPort: 5000
          env:
            - name: RDS_HOST
              value: "localhost"  # MySQL in the same pod
            - name: RDS_PORT
              value: "3306"
            - name: RDS_USER
              value: "admin"
            - name: RDS_PASSWORD
              value: "Local_1234567"
            - name: RDS_DB_NAME
              value: "darshan"

        - name: mysql-container
          image: mysql:latest
          ports:
            - containerPort: 3306
          env:
            - name: MYSQL_ROOT_PASSWORD
              value: "my-secret-pw"
            - name: MYSQL_DATABASE
              value: "darshan"
2. Apply the Deployment YAML
Run the following command to apply the deployment to your Kubernetes cluster:

bash
Copy
kubectl apply -f single-pod-deployment.yaml
3. Verify the Pod Status
After deployment, check the status of your pod to ensure both containers are running correctly:

bash
Copy
kubectl get pods
To view logs for each container:

bash
Copy
kubectl logs <pod-name> -c flask-container
kubectl logs <pod-name> -c mysql-container
4. Expose the Pod Using a Service
If you want to make the Flask application accessible externally, expose the pod using a Kubernetes Service. Create a file named service.yaml:

yaml
Copy
apiVersion: v1
kind: Service
metadata:
  name: single-pod-service
spec:
  selector:
    app: single-pod-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 5000
  type: LoadBalancer
Apply the service definition:

bash
Copy
kubectl apply -f service.yaml
5. Access Your Application
Once deployed, you can access the Flask application externally via the Service's external IP.

Get the external IP of the service:

bash
Copy
kubectl get svc single-pod-service
Look for the EXTERNAL-IP in the output. This is the IP address you can use to access your Flask application.
