
# Deploying Jellyfin to a Cilium-enabled Kubernetes Cluster

## What is Jellyfin?
Jellyfin is a free and open-source media server software that enables you to organize, manage, and stream your media. It supports streaming to multiple devices and is fully customizable.

## What are we using Jellyfin for?
We are deploying Jellyfin in a Cilium-enabled Kubernetes cluster to stream media securely with high performance. Cilium provides enhanced networking and security using eBPF, ensuring that Jellyfin is robust and scalable while maintaining high visibility and secure communication across the cluster.

---

## Prerequisites
- A Kubernetes cluster with Cilium installed
- `kubectl` installed and configured
- Docker installed for building custom images
- A Docker Hub account or private container registry

---

## Step 1: Create a Jellyfin Docker Image
If you're using a custom Jellyfin setup, you may need to create a Docker image. Otherwise, you can use the official Jellyfin image.

### Dockerfile
```dockerfile
FROM jellyfin/jellyfin:latest

COPY custom-config /config

EXPOSE 8096
CMD ["jellyfin"]
```

Build and push the Docker image:
```bash
docker build -t yourusername/jellyfin-custom .
docker push yourusername/jellyfin-custom
```

---

## Step 2: Deploy Jellyfin in Kubernetes

### jellyfin-deployment.yaml
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: jellyfin-deployment
  namespace: default
spec:
  replicas: 2
  selector:
    matchLabels:
      app: jellyfin
  template:
    metadata:
      labels:
        app: jellyfin
    spec:
      containers:
      - name: jellyfin
        image: yourusername/jellyfin-custom
        ports:
        - containerPort: 8096
        volumeMounts:
        - name: jellyfin-config
          mountPath: /config
        - name: jellyfin-media
          mountPath: /media
      volumes:
      - name: jellyfin-config
        persistentVolumeClaim:
          claimName: jellyfin-config-pvc
      - name: jellyfin-media
        persistentVolumeClaim:
          claimName: jellyfin-media-pvc
```

Apply the deployment:
```bash
kubectl apply -f jellyfin-deployment.yaml
```

---

## Step 3: Create Persistent Volumes (PVCs)

### jellyfin-config-pvc.yaml
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: jellyfin-config-pvc
  namespace: default
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
```

### jellyfin-media-pvc.yaml
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: jellyfin-media-pvc
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
kubectl apply -f jellyfin-config-pvc.yaml
kubectl apply -f jellyfin-media-pvc.yaml
```

---

## Step 4: Expose Jellyfin Externally

### jellyfin-service.yaml
```yaml
apiVersion: v1
kind: Service
metadata:
  name: jellyfin-service
  namespace: default
spec:
  selector:
    app: jellyfin
  ports:
    - protocol: TCP
      port: 8096
      targetPort: 8096
  type: NodePort
```

Apply the service:
```bash
kubectl apply -f jellyfin-service.yaml
```

---

## Step 5: Access Jellyfin Externally

Get the external IP of a node:
```bash
kubectl get nodes -o wide
```

Then access Jellyfin at:
```
http://<NODE_IP>:<NODE_PORT>
```

For Minikube:
```bash
minikube service jellyfin-service --url
```

---

## Summary
- Optionally created a custom Jellyfin Docker image.
- Deployed Jellyfin to a Kubernetes cluster with persistent storage.
- Used a NodePort service to expose Jellyfin externally.
- Verified access to Jellyfin using the node’s external IP and port.

---

## Resources
- [Jellyfin Documentation](https://jellyfin.org/docs/)
- [Cilium Documentation](https://docs.cilium.io/)
- [Kubernetes PVC Docs](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)
