# Deploying an Nginx Deployment Visible Externally

## What is Nginx?
Nginx is a high-performance, open-source web server that can also function as a reverse proxy, load balancer, and API gateway. It is widely used for serving web applications due to its speed, scalability, and low resource consumption.

## What are we suing Nginx for?
we are using Nginx to serve a website to external traffic within a Kubernetes deployment. It acts as a reverse proxy and load balancer, efficiently managing incoming requests and routing them to the appropriate backend services. This setup ensures high availability and scalability for the website.

---
## Prerequisites
- A Kubernetes cluster
- `kubectl` installed and configured
- Node(s) with an external IP (for NodePort access)

---

## Step 1: Deploy Nginx
Create a deployment for Nginx.

### nginx-deployment.yaml
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  namespace: default
spec:
  replicas: 2
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:latest
        ports:
        - containerPort: 80
```
Apply the deployment:
```sh
kubectl apply -f nginx-deployment.yaml
```

---

## Step 2: Expose Nginx Externally
Create a NodePort service to make Nginx accessible externally.

### nginx-service.yaml
```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
  namespace: default
spec:
  selector:
    app: nginx
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
      nodePort: 30080  # Choose a port in the 30000-32767 range
  type: NodePort
```
Apply the service:
```sh
kubectl apply -f nginx-service.yaml
```

---

## Step 3: Access the Nginx Webpage
Find the external IP of a node:
```sh
kubectl get nodes -o wide
```
Use the node's IP and NodePort to access the Nginx web server:
```
http://<NODE_IP>:30080
```

---

## Summary
- Deployed an Nginx web server using Kubernetes.
- Exposed it externally using a **NodePort** service.

---

## Links
[Nginx Webpage](https://nginx.org/)
[Geeks For Geeks Example](https://www.geeksforgeeks.org/how-to-deploy-nginx-in-kubernetes/)
