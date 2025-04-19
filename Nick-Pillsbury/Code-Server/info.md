
# Deploying code-server to a Cilium-enabled Kubernetes Cluster

## What is code-server?
code-server is a free and open-source workspace server software that enables you to organize, manage, and stream your workspace. It supports remote development on any device and is fully customizable.

## What are we using code-server for?
We are deploying code-server in a Cilium-enabled Kubernetes cluster to develop securely with high performance remote access. Cilium provides enhanced networking and security using eBPF, ensuring that code-server is robust and scalable while maintaining high visibility and secure communication across the cluster.

---

## Prerequisites
- A Kubernetes cluster with Cilium installed
- `kubectl` installed and configured
- Docker installed for building custom images
- A Docker Hub account or private container registry

---

## Step 1: Create a code-server Docker Image
If you're using a custom code-server setup, you may need to create a Docker image. Otherwise, you can use the official code-server image.

### Dockerfile
```dockerfile
FROM code-server/code-server:latest

COPY custom-config /config

EXPOSE 8096
CMD ["code-server"]
```

Build and push the Docker image:
```bash
docker build -t yourusername/code-server-custom .
docker push yourusername/code-server-custom
```

---

## Step 2: Deploy code-server in Kubernetes

### code-server-deployment.yaml
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: code-server-deployment
  namespace: default
spec:
  replicas: 2
  selector:
    matchLabels:
      app: code-server
  template:
    metadata:
      labels:
        app: code-server
    spec:
      containers:
      - name: code-server
        image: yourusername/code-server-custom
        ports:
        - containerPort: 8080
        volumeMounts:
        - name: code-server-config
          mountPath: /home/coder/.config
        - name: code-server-workspace
          mountPath: /workspace
      volumes:
      - name: code-server-config
        persistentVolumeClaim:
          claimName: code-server-home-pvc
      - name: code-server-workspace
        persistentVolumeClaim:
          claimName: code-server-workspace-pvc
```

Apply the deployment:
```bash
kubectl apply -f code-server-deployment.yaml
```

---

## Step 3: Create Persistent Volumes (PVCs)

### code-server-home-pvc.yaml
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: code-server-home-pvc
  namespace: default
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
```

### code-server-workspace-pvc.yaml
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: code-server-workspace-pvc
  namespace: default
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 20Gi
```

Apply the PVCs:
```bash
kubectl apply -f code-server-home-pvc.yaml
kubectl apply -f code-server-workspace-pvc.yaml
```

---

## Step 4: Expose code-server Externally

### code-server-service.yaml
```yaml
apiVersion: v1
kind: Service
metadata:
  name: code-server-service
  namespace: default
spec:
  selector:
    app: code-server
  ports:
    - protocol: TCP
      port: 8080
      targetPort: 8080
  type: NodePort
```

Apply the service:
```bash
kubectl apply -f code-server-service.yaml
```

---

## Step 5: Access code-server Externally

Get the external IP of a node:
```bash
kubectl get nodes -o wide
```

Then access code-server at:
```
http://<NODE_IP>:<NODE_PORT>
```

For Minikube:
```bash
minikube service code-server-service --url
```

---

## Summary
- Optionally created a custom code-server Docker image.
- Deployed code-server to a Kubernetes cluster with persistent storage.
- Used a NodePort service to expose code-server externally.
- Verified access to code-server using the node’s external IP and port.

---

## Resources
- [code-server Documentation](https://code-server.org/docs/)
- [Cilium Documentation](https://docs.cilium.io/)
- [Kubernetes PVC Docs](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)
