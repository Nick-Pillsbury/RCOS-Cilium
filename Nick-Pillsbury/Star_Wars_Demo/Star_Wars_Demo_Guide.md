# Cilium Star Wars Demo

---

## Step 1: Deploy a Kubernetes Cluster with Cilium
- There are mutiple  ways of doing this, anyway is okay. (I use Minikube and Helm)
- You just need a running cluster with cilium as the cni.

---

## Step 2: Install Kubernetes Deployment File

### What it Does?
- This file will create, 1 service with 2 repilcas and 2 clients.
- We have a service (deathstar), with labels: 
  - org: empire 
  - class: deathstar
- We have a pod (tiefighter), with lables:
  - org: empire 
  - class: deathstar
- We have a pod (xwing), with labels:
  - org: alliance
  - class: xwing

### Create File from Github
```bash
kubectl create -f https://raw.githubusercontent.com/cilium/cilium/1.17.0/examples/minikube/http-sw-app.yaml
```

### Yaml File Explanation
```yml
---
apiVersion: v1
kind: Service
metadata:
  name: deathstar
  labels:
    app.kubernetes.io/name: deathstar
spec:
  type: ClusterIP
  ports:
  - port: 80
  selector:
    org: empire
    class: deathstar
---
```
Defines a Kubernetes Service named "deathstar" that routes traffic to Pods labeled org=empire and class=deathstar. It is a ClusterIP service. Traffic sent to this service on port 80 will be forwarded to the matching Pods.
```yml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: deathstar
  labels:
    app.kubernetes.io/name: deathstar
spec:
  replicas: 2
  selector:
    matchLabels:
      org: empire
      class: deathstar
  template:
    metadata:
      labels:
        org: empire
        class: deathstar
        app.kubernetes.io/name: deathstar
    spec:
      containers:
      - name: deathstar
        image: quay.io/cilium/starwars:v2.1@sha256:833d915ec68fca3ce83668fc5dae97c455b2134d8f23ef96586f55b894cfb1e8
---
```
Defines a Kubernetes Deployment named "deathstar", which ensures that two replicas of the Death Star Pod are running at all times. The Deployment uses a selector to manage Pods labeled org=empire and class=deathstar, ensuring they match the template. Each Pod runs a container from the image quay.io/cilium/starwars:v2.1.
```yml
apiVersion: v1
kind: Pod
metadata:
  name: tiefighter
  labels:
    org: empire
    class: tiefighter
    app.kubernetes.io/name: tiefighter
spec:
  containers:
  - name: spaceship
    image: quay.io/cilium/json-mock:v1.3.8@sha256:5aad04835eda9025fe4561ad31be77fd55309af8158ca8663a72f6abb78c2603
---
```
Defines a Kubernetes Pod named "tiefighter", which runs a container named "spaceship". The container is based on the quay.io/cilium/json-mock:v1.3.8 image. The Pod is labeled with org=empire and class=tiefighter.
```yml
apiVersion: v1
kind: Pod
metadata:
  name: xwing
  labels:
    app.kubernetes.io/name: xwing
    org: alliance
    class: xwing
spec:
  containers:
  - name: spaceship
    image: quay.io/cilium/json-mock:v1.3.8@sha256:5aad04835eda9025fe4561ad31be77fd55309af8158ca8663a72f6abb78c2603
```
Defines a Kubernetes Pod named "xwing", which runs a container named "spaceship". The container is based on the quay.io/cilium/json-mock:v1.3.8 image. The Pod is labeled with org=alliance and class=xwing

---

## Step 3: See Pods and Endpoints
shows the pods, status, and Clusters
```Bash
kubectl get pods,svc
```
gets the local cilium agent
```bash
kubectl -n kube-system get pods -l k8s-app=cilium
```
lists all endpoint  
```bash
kubectl -n kube-system exec cilium-<cilium agent id> -- cilium-dbg endpoint list
```

---

## Step 4: Apply an L3/L4 Policy
Currently there are no policies in place, both clients are being accepted by the server.
### Create File from Github
```bash
kubectl create -f https://raw.githubusercontent.com/cilium/cilium/1.17.0/examples/minikube/sw_l3_l4_policy.yaml
```
### Yaml File Explantion
```yml
apiVersion: "cilium.io/v2"
kind: CiliumNetworkPolicy
metadata:
  name: "rule1"
spec:
  description: "L3-L4 policy to restrict deathstar access to empire ships only"
  endpointSelector:
    matchLabels:
      org: empire
      class: deathstar
  ingress:
  - fromEndpoints:
    - matchLabels:
        org: empire
    toPorts:
    - ports:
      - port: "80"
        protocol: TCP
```
A CiliumNetworkPolicy named rule1, that only allows traffic to the deathstar (ord: empire and class: deathsstar) to come from pods with label org: empire. The allowed traffic is restricted to only come through port 80 (HTTP) over TCP to the deathstar.

---

## Step 5: Verify Policy Effect
When running these commands the xwing will be blocked and the tiefighter will go through.
Tiefighter command will get a response and the xwing command will hang.
```bash
kubectl exec tiefighter -- curl -s -XPOST deathstar.default.svc.cluster.local/v1/request-landing
kubectl exec xwing -- curl -s -XPOST deathstar.default.svc.cluster.local/v1/request-landing
```

---

## Step 6: Inspect policies
This is how you can see active Cilium Network Policies and read what each one does.
```bash
kubectl get cnp
kubectl describe cnp rule1
```

## Step 7: L7 Policy
### Update our Network Policy Yaml
Update our rule yaml to include an L7 policy
```bash
kubectl apply -f https://raw.githubusercontent.com/cilium/cilium/1.17.0/examples/minikube/sw_l3_l4_l7_policy.yaml
```
### Yaml File Explaination
```yml
apiVersion: "cilium.io/v2"
kind: CiliumNetworkPolicy
metadata:
  name: "rule1"
spec:
  description: "L7 policy to restrict access to specific HTTP call"
  endpointSelector:
    matchLabels:
      org: empire
      class: deathstar
  ingress:
  - fromEndpoints:
    - matchLabels:
        org: empire
    toPorts:
    - ports:
      - port: "80"
        protocol: TCP
      rules:
        http:
        - method: "POST"
          path: "/v1/request-landing"
```
We added a http rule that requests can only come in from /v1/request-landing. This means that org: empire pods can only access this https and cannot make requestions to other urls.

---

## Step 8: Verify L7 Policy
```bash
kubectl exec tiefighter -- curl -s -XPOST deathstar.default.svc.cluster.local/v1/request-landing
Ship landed
$ kubectl exec tiefighter -- curl -s -XPUT deathstar.default.svc.cluster.local/v1/exhaust-port
Access denied
```
With Cilium L7 security policies, we are able to permit tiefighter to access only the required API resources on deathstar, thereby implementing a “least privilege” security approach for communication between microservices.


---

## Demo Link
[Offical Cilium Star Wars Demo](https://docs.cilium.io/en/stable/gettingstarted/demo/)