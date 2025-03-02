# Setting Up Multiple Kubernetes Clusters with Cilium ClusterMesh

---

## **1. Prerequisites**
Before starting, ensure you have installed:
- **Docker** (for running Kubernetes nodes)
- **kubectl** (to manage Kubernetes clusters)
- **kind** (to create clusters locally)
- **Cilium CLI** (to install Cilium)

Install dependencies if you haven’t:

---
## **2. Create Multiple Clusters Using kind**
Create two clusters (`cluster-a` and `cluster-b`):
```bash
kind create cluster --name cluster-a
kind create cluster --name cluster-b
```
Check the clusters:
```bash
kubectl config get-contexts
```
You should see two contexts: `kind-cluster-a` and `kind-cluster-b`.

---
## **3. Install Cilium in Each Cluster**
Set up Cilium in both clusters.

**Switch to `cluster-a` and install Cilium:**
```bash
kubectl config use-context kind-cluster-a
cilium install --cluster-name cluster-a --cluster-id 1
```

**Switch to `cluster-b` and install Cilium:**
```bash
kubectl config use-context kind-cluster-b
cilium install --cluster-name cluster-b --cluster-id 2
```

Verify that Cilium is running in both clusters:
```bash
kubectl get pods -n kube-system
```
You should see Cilium-related pods running.

---
## **4. Enable Cilium ClusterMesh**
### **Step 1: Enable ClusterMesh**
On each cluster, run:
```bash
cilium clustermesh enable
```
Check ClusterMesh status:
```bash
cilium clustermesh status
```

### **Step 2: Exchange ClusterMesh Secrets**
On `cluster-a`, extract credentials:
```bash
cilium clustermesh extract-service-accounts --output clustermesh-secrets-a.yaml
kubectl config use-context kind-cluster-b
kubectl apply -f clustermesh-secrets-a.yaml
```
On `cluster-b`, extract credentials:
```bash
cilium clustermesh extract-service-accounts --output clustermesh-secrets-b.yaml
kubectl config use-context kind-cluster-a
kubectl apply -f clustermesh-secrets-b.yaml
```

### **Step 3: Connect Clusters**
```bash
cilium clustermesh connect --destination-context kind-cluster-b
cilium clustermesh connect --destination-context kind-cluster-a
```
Check connection:
```bash
cilium clustermesh status
```

---
## **5. Verify Cross-Cluster Communication**
Deploy test pods on both clusters:
```bash
kubectl config use-context kind-cluster-a
kubectl create deployment test-a --image=busybox --restart=Never -- sleep 3600

kubectl config use-context kind-cluster-b
kubectl create deployment test-b --image=busybox --restart=Never -- sleep 3600
```
Test communication:
```bash
kubectl exec test-a -- nc -zv test-b.default.svc.cluster-b.local 80
```
If working correctly, `test-a` should reach `test-b`.

---
## **6. Clean Up**
If you want to delete the clusters:
```bash
kind delete cluster --name cluster-a
kind delete cluster --name cluster-b
```

---
## **Final Notes**
- This setup is for local testing. In production, use **EKS, GKE, or AKS**.
- **Cilium ClusterMesh** is the key component for cross-cluster networking.
- Apply **Cilium policies** to control cluster-to-cluster traffic.

---
## **References**
[Cilium ClusterMesh Documentation](https://docs.cilium.io/en/stable/network/clustermesh/clustermesh/)
[Setup with Kind](https://docs.cilium.io/en/stable/installation/kind/)
