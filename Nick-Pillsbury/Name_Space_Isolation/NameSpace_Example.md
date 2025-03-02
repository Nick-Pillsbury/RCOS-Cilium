# Basic Namespace Isolation with Cilium

---

## Prerequisites
- Ensure Cilium is installed and running in your Kubernetes cluster.

---
## Enforce Namespace Isolation Between Teams
We will create two namespaces: `team-a` and `team-b`, and enforce network policies to restrict communication.

### Step 1: **Create Namespaces**
```bash
kubectl create namespace team-a
kubectl create namespace team-b
```

### Step 2: **Block Access from Team A to Team B**
Create the following Cilium Network Policy and save it as `block-team-a-to-team-b.yaml`:
```yaml
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: block-team-a-to-team-b
  namespace: team-b
spec:
  endpointSelector: {}
  ingress:
  - fromEndpoints:
    - matchLabels:
        io.kubernetes.pod.namespace: team-a
```
Apply the policy:
```bash
kubectl apply -f block-team-a-to-team-b.yaml
```
This policy blocks all ingress traffic from `team-a` to `team-b`.

### Step 3: **Verify the Isolation**
```bash
kubectl run test-a --image=busybox --restart=Never -n team-a -- sleep 3600
kubectl run test-b --image=busybox --restart=Never -n team-b -- sleep 3600
kubectl exec -n team-a test-a -- nc -zv test-b.team-b.svc.cluster.local 80
kubectl exec -n team-b test-b -- nc -zv test-a.team-a.svc.cluster.local 80
```
Traffic from Team A to Team B should be blocked, and the command should fail, while traffic from Team B to Team A will go through.

### Step 4: **Block Access from Both Teams to Each Other**
Create another Cilium Network Policy and save it as `block-team-communication.yaml`:
```yaml
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: block-team-communication
  namespace: team-a
spec:
  endpointSelector: {}
  ingress:
  - fromEndpoints:
    - matchLabels:
        io.kubernetes.pod.namespace: team-b
---
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: block-team-communication
  namespace: team-b
spec:
  endpointSelector: {}
  ingress:
  - fromEndpoints:
    - matchLabels:
        io.kubernetes.pod.namespace: team-a
```
Apply the policy:
```bash
kubectl apply -f block-team-communication.yaml
```
This will ensure that **both teams cannot communicate with each other**.

### Step 5: **Verify the Isolation**
Deploy test pods in both namespaces and attempt to communicate between them.
```bash
kubectl run test-a --image=busybox --restart=Never -n team-a -- sleep 3600
kubectl run test-b --image=busybox --restart=Never -n team-b -- sleep 3600
kubectl exec -n team-a test-a -- nc -zv test-b.team-b.svc.cluster.local 80
kubectl exec -n team-b test-b -- nc -zv test-a.team-a.svc.cluster.local 80
```
If isolation is working correctly, **both connection attempts should fail**.

---
## Special Notes
This guide helps you:
- Implement **namespace isolation** between `team-a` and `team-b`.

By default, Kubernetes allows all inter-namespace communication. **Cilium provides fine-grained control over network policies**, ensuring security and isolation in multi-tenant environments.

---
## Links
[Cilium Network Policies](https://docs.cilium.io/en/stable/security/network-policies/)

