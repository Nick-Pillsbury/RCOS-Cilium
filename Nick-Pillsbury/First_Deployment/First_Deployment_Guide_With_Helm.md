# First Cilium Deployment Guide

---

## Prerequisites
Before starting, ensure you have completed the following:
- Ubuntu 20.04+ system with at least 4 GB RAM, 2 CPUs cores, and 20 GB of disk space.
- Docker, Minikube, kubectl, Helm, and Cilium repositories installed

---

## Create a Kubernetes Cluster Locally With Minikube
```bash
minikube start --memory=8192 --cpus=4
```

---
## Install Cilium With Helm Onto The Cluster
```bash
helm install cilium cilium/cilium --version 1.17.1 --namespace kube-system
```

---
## Restart Unmanaged Pods
```bash
kubectl get pods --all-namespaces -o custom-columns=NAMESPACE:.metadata.namespace,NAME:.metadata.name,HOSTNETWORK:.spec.hostNetwork --no-headers=true | grep '<none>' | awk '{print "-n "$1" "$2}' | xargs -L 1 -r kubectl delete pod
```

---

## Install The Latest Version Of The Cilium CLI
```bash
CILIUM_CLI_VERSION=$(curl -s https://raw.githubusercontent.com/cilium/cilium-cli/main/stable.txt)
CLI_ARCH=amd64
if [ "$(uname -m)" = "aarch64" ]; then CLI_ARCH=arm64; fi
curl -L --fail --remote-name-all https://github.com/cilium/cilium-cli/releases/download/${CILIUM_CLI_VERSION}/cilium-linux-${CLI_ARCH}.tar.gz{,.sha256sum}
sha256sum --check cilium-linux-${CLI_ARCH}.tar.gz.sha256sum
sudo tar xzvfC cilium-linux-${CLI_ARCH}.tar.gz /usr/local/bin
rm cilium-linux-${CLI_ARCH}.tar.gz{,.sha256sum}
```

---

## Validate The Installation
```bash
cilium status --wait
```

---

## Special Notes
Congratulations! You have a fully functional Kubernetes cluster with Cilium. :)
The Process of creating a cluster with cilium:
- Launch a Cluster
- Install Cilium onto it with Helm
- Restart Nodes without Cilium
- Download Newest Cilium CLI
You must do this everytime to have a functonal cluster with Cilium!

---
## Links
[Cilium Installation With Helm](https://docs.cilium.io/en/stable/installation/k8s-install-helm/)