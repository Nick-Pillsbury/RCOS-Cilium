# Basic Multi-Cluster Isolation with Cilium ClusterMesh

---

## Prerequisites
- Ablity to set-up mutile clusters with Cilium
- Ensure Cilium is installed and running on all clusters.
- Enable ClusterMesh on both clusters.

---
## Enforce Multi-Cluster Isolation Between Teams
We will create two clusters: `cluster-a` and `cluster-b`, and enforce network policies to restrict communication.

---

### Step 1: **Set-Up**
- Create two clusters with Cilium, cluster-a an cluster-b.
- Verify that Both clusters are running correctly with Cilium as their CNI.
- Enable ClusterMesh on both clusters.

### Step 2: **Block Access from Cluster A to Cluster B**
Create the following Cilium Cluster-wide Network Policy and save it as `block-cluster-a-to-cluster-b.yaml`:
```yaml
apiVersion: cilium.io/v2
kind: CiliumClusterwideNetworkPolicy
metadata:
  name: block-cluster-a-to-cluster-b
spec:
  endpointSelector: {}
  ingress:
  - fromEndpoints:
    - matchLabels:
        io.cilium.k8s.policy.cluster: cluster-a
```
Apply the policy:
```bash
kubectl apply -f block-cluster-a-to-cluster-b.yaml
```
This policy blocks all ingress traffic from `cluster-a` to `cluster-b`.

### Step 3: **Verify the Isolation**
```bash
kubectl run test-a --image=busybox --restart=Never -n default -- sleep 3600
kubectl run test-b --image=busybox --restart=Never -n default -- sleep 3600
kubectl exec test-a -- nc -zv test-b.default.svc.cluster-b.local 80
kubectl exec test-b -- nc -zv test-a.default.svc.cluster-a.local 80
```
Traffic from Cluster A to Cluster B should be blocked, and the command should fail, while traffic from Cluster B to Cluster A will go through.

### Step 4: **Block Access Between Both Clusters**
Create another Cilium Cluster-wide Network Policy and save it as `block-cluster-communication.yaml`:
```yaml
apiVersion: cilium.io/v2
kind: CiliumClusterwideNetworkPolicy
metadata:
  name: block-cluster-communication
spec:
  endpointSelector: {}
  ingress:
  - fromEndpoints:
    - matchLabels:
        io.cilium.k8s.policy.cluster: cluster-a
---
apiVersion: cilium.io/v2
kind: CiliumClusterwideNetworkPolicy
metadata:
  name: block-cluster-communication
spec:
  endpointSelector: {}
  ingress:
  - fromEndpoints:
    - matchLabels:
        io.cilium.k8s.policy.cluster: cluster-b
```
Apply the policy:
```bash
kubectl apply -f block-cluster-communication.yaml
```
This ensures **both clusters cannot communicate with each other**.

### Step 5: **Verify the Isolation**
Deploy test pods in both clusters and attempt to communicate:
```bash
kubectl create deployment test-a --image=busybox --restart=Never -n default -- sleep 3600
kubectl create deployment test-b --image=busybox --restart=Never -n default -- sleep 3600
kubectl exec test-a -- nc -zv test-b.default.svc.cluster-b.local 80
kubectl exec test-b -- nc -zv test-a.default.svc.cluster-a.local 80
```
If isolation is working correctly, **both connection attempts should fail**.

---
## Special Notes
This guide helps you:
- Implement **multi-cluster isolation** between `cluster-a` and `cluster-b`.

By default, Cilium ClusterMesh allows cross-cluster communication. **Cilium provides fine-grained control over network policies**, ensuring security and isolation in multi-cluster environments.

---
## Links
[Cilium ClusterMesh](https://docs.cilium.io/en/stable/clustermesh/)