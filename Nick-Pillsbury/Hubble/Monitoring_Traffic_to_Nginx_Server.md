# Kubernetes Network Policy and Hubble Traffic Monitoring

## Objective
1. Deploy an Nginx web server in Kubernetes and expose it externally.
2. Apply a **NetworkPolicy** to control the traffic to Nginx.
3. Use **Hubble** to monitor and visualize the network traffic.

---

## Prerequisites

- Kubernetes cluster.
- `kubectl` installed and configured.
- **Cilium** installed as the CNI (Container Network Interface).
- **Hubble** installed for traffic monitoring.
- Hubble CNI - winget install --id=Cilium.Hubble  -e
- Running Kubernetes Cluster with Cilium installed.

---

## 1. Deploying Nginx

### 1.1 Create the Nginx Deployment
Define the Nginx deployment manifest:

```yaml
# nginx-deployment.yaml
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
### Apply the deployment:
```bash
kubectl apply -f nginx-deployment.yaml
```

### 1.2 Expose Nginx Externally
Create a NodePort service to make Nginx accessible from outside the cluster.
```yaml
# nginx-service.yaml
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
```bash
kubectl apply -f nginx-service.yaml
```

### 1.3 Get the external ip:
```bash
kubectl get nodes -o wide
# http://<NODE_IP>:<NodePort>
```

Or

```bash
minikube service nginx-service --url
```

## 3. Creating a Network Policy

Let's create a network policy that:
- Allows only pod-to-pod communication from the app: frontend label.
- Blocks external traffic from other namespaces.

```yaml
# nginx-network-policy.yaml
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: nginx-access-policy
  namespace: default
spec:
  endpointSelector:
    matchLabels:
      app: nginx
  ingress:
    - fromEndpoints:
        - matchLabels:
            app: frontend
      toPorts:
        - ports:
            - port: "80"
              protocol: TCP
  egress:
    - toEntities:
        - cluster
```

### Apply the Network Policy
```bash
kubectl apply -f nginx-network-policy.yaml
```

### Test the Policy

#### This Connection should fail, as it is missing the frontend label
```bash
kubectl run busybox --rm -it --image=busybox -- /bin/sh
wget --spider --timeout=1 http://nginx-service.default.svc.cluster.local
```

#### This Connection should succeed, as it has the frontend label
```bash
kubectl run frontend-pod --rm -it --image=busybox --labels="app=frontend" -- /bin/sh
wget --spider --timeout=1 http://nginx-service.default.svc.cluster.local
```


## Monitoring Traffic with Hubble

### Enable Hubble if Needed
```bash
cilium hubble enable
cilium hubble port-forward&
```
Wait for the cluster to be ready, check with **cilium status**

### View Traffic Flows
```bash
hubble observe
```

### Example Output:
```bash
Default/Nginx-service:80 => Default/frontend-pod:  Success
Default/Nginx-service:80 => Default/busybox:       Denied (by network policy)
```


## Summary of the Learning Process
What we did:

- Deployed an Nginx deployment and exposed it externally.
- Applied a NetworkPolicy to restrict traffic to specific pods.
- Installed Hubble and monitored the traffic.
- Validated the policy by testing allowed and blocked connections.


## References

[Hubble](https://docs.cilium.io/en/stable/overview/intro/)