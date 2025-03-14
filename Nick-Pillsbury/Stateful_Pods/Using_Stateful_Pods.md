# Running Docker Applications with Cilium Example

---

## Prerequisites
- `kubectl` and `helm` installed on your local machine.
- A Kubernetes cluster with **Cilium installed and running**.
- Access to **Docker Hub**.

---

## Deploying Prebuilt Docker Applications
We will deploy some prebuilt Docker applications into Kubernetes and use **Cilium** to enforce network policies.


### **Step 1: Deploy an Nginx Web Server**
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

Expose it using a **Service**:
```sh
kubectl expose deployment nginx-deployment --type=ClusterIP --port=80 --target-port=80
```


### **Step 2: Deploy a Redis Cache**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis-deployment
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      app: redis
  template:
    metadata:
      labels:
        app: redis
    spec:
      containers:
      - name: redis
        image: redis:latest
        ports:
        - containerPort: 6379
```
Apply the deployment:
```sh
kubectl apply -f redis-deployment.yaml
```

Expose it using a **Service**:
```sh
kubectl expose deployment redis-deployment --type=ClusterIP --port=6379 --target-port=6379
```

---

## **Securing Applications with Cilium**
By default, Kubernetes allows unrestricted communication between pods. **Cilium** enables fine-grained **network policies** to restrict access between services.

### **Step 3: Apply a Cilium Network Policy to Secure Redis**
This policy **only allows traffic to Redis from Nginx pods**, blocking all other access.

```yaml
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: restrict-redis-access
  namespace: default
spec:
  endpointSelector:
    matchLabels:
      app: redis
  ingress:
  - fromEndpoints:
    - matchLabels:
        app: nginx
```
Apply the policy:
```sh
kubectl apply -f restrict-redis-access.yaml
```

### **Step 4: Verify Network Policies**
1. **Test allowed traffic:**
   ```sh
   kubectl run test-nginx --image=nginx --restart=Never -it --rm -- curl redis.default.svc.cluster.local:6379
   ```
   This should **succeed** because Nginx is allowed.

2. **Test blocked traffic:**
   ```sh
   kubectl run test-busybox --image=busybox --restart=Never -it --rm -- nc -zv redis.default.svc.cluster.local 6379
   ```
   This should **fail** because BusyBox is not allowed by the policy.

---

## **Summary**
- Deployed prebuilt **Nginx** and **Redis** applications using Kubernetes.
- Used **Cilium Network Policies** to **restrict access** to Redis.
- Verified policies by testing allowed and blocked traffic.

Cilium enables advanced security and observability for Kubernetes workloads, making it easier to manage **network isolation, security enforcement, and visibility.**

---

## **Links**

[Cilium Network Policies](https://docs.cilium.io/en/stable/security/network-policies/)

