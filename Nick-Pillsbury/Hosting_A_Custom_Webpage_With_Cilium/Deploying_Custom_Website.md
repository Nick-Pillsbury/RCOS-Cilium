# Deploying an Nginx Deployment Visible Externally

## What is Nginx?
Nginx is a high-performance, open-source web server that can also function as a reverse proxy, load balancer, and API gateway. It is widely used for serving web applications due to its speed, scalability, and low resource consumption.

## What are we using Nginx for?
We are using Nginx to serve a website to external traffic within a Kubernetes deployment. It acts as a reverse proxy and load balancer, efficiently managing incoming requests and routing them to the appropriate backend services. This setup ensures high availability and scalability for the website.

---
## Prerequisites
- A Kubernetes cluster
- `kubectl` installed and configured
- Nodes with an external IP (for NodePort access)
- Docker installed for building custom images
- A Docker Hub account or private container registry

---

## Step 1: Create a Custom Website
First, create an `index.html` file for your website:

### index.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>About Cilium</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            background-color: #eef2f3;
            margin: 0;
            padding: 0;
        }
        .container {
            max-width: 800px;
            margin: 20px auto;
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
        }
        img {
            width: 100%;
            border-radius: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>What is Cilium?</h1>
        <img src="https://cilium.io/img/logos/cilium-logo-title-dark.svg" alt="Cilium Logo">
        <p>Cilium is an open-source networking, observability, and security solution for cloud-native applications running on Kubernetes. It uses eBPF technology to provide high-performance networking and deep visibility into network traffic.</p>
        <h2>Key Features of Cilium</h2>
        <ul>
            <li>eBPF-powered networking for efficient packet processing</li>
            <li>Advanced network security and policy enforcement</li>
            <li>Observability with Hubble for deep network insights</li>
            <li>Multi-cluster networking with ClusterMesh</li>
            <li>Integration with Kubernetes, Istio, and service meshes</li>
        </ul>
        <p>Learn more at the official website: <a href="https://cilium.io" target="_blank">Cilium.io</a></p>
    </div>
</body>
</html>
```

Now, create a `Dockerfile` to serve this custom website:

### Dockerfile
```dockerfile
FROM nginx:latest
COPY index.html /usr/share/nginx/html/index.html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

Build and push the Docker image:
```sh
docker build -t nickpillsbury/custom-nginx .
docker push nickpillsbury/custom-nginx
```

---

## Step 2: Deploy Nginx with the Custom Website
Create a deployment for Nginx using your custom Docker image.

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
        image: nickpillsbury/custom-nginx
        ports:
        - containerPort: 80
```
Apply the deployment:
```sh
kubectl apply -f nginx-deployment.yaml
```

---
## Step 3: Expose Nginx Externally
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
      nodePort: 30080
  type: NodePort
```
Apply the service:
```sh
kubectl apply -f nginx-service.yaml
```

---
## Step 4: Access the Custom Webpage
Find the external IP of a node:
```sh
kubectl get nodes -o wide
```
Use the node's IP and NodePort to access the custom website:
```
http://<NODE_IP>:30080
```

---
## Summary
- Created a custom website with an `index.html` file.
- Built and pushed a custom Nginx image.
- Deployed Nginx in Kubernetes using this custom image.
- Exposed it externally using a **NodePort** service.

---
## Links
- [Nginx Webpage](https://nginx.org/)
- [Geeks for Geeks Example](https://www.geeksforgeeks.org/how-to-deploy-nginx-in-kubernetes/)
