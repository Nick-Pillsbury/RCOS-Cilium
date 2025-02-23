# Installing Cilium on Ubuntu Using Helm
This guide walks through installing Cilium  Using Helm and all necessary dependencies on an **Ubuntu** system.

---

## Prerequisites
Ensure your system meets the following requirements:
- **Ubuntu 20.04+**
- **CPU: 2+ vCPUs**
- **RAM: 4+ GB**
- **Disk: 20+ GB**
- **Recommended Kernel Version: 5.10+**

---

## Step 1: Update System
```bash
sudo apt update && sudo apt upgrade -y
```

---

## Step 2: Install Required Packages
### Networking & System Tools
These are required for Docker, Minikube, Helm, and Cilium to Run Properly!
- **apt-transport-https** - Enables APT to communicate over HTTPS, allowing secure package downloads from repositories.
- **ca-certificates** - Provides trusted SSL/TLS certificates for validating secure connections
- **curl** - A tool for transferring data with URLs
- **gnupg-agent** - A tool for managing cryptographic keys for GPG
- **software-properties-common** - Provides management utilities for software sources and repositories
```bash
sudo apt install apt-transport-https ca-certificates curl gnupg-agent software-properties-common
```

---

## Step 3: Install Docker
### Set up Dockers apt Repository
```bash
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
```
### Install Docker
```bash
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```
### Verify Install
```bash
sudo docker run hello-world
```

---

## Step 4: Install Kubernetes
### Download the public signing key for the Kubernetes package repositories. The same signing key is used for all repositories so you can disregard the version in the URL:
```bash
# If the folder `/etc/apt/keyrings` does not exist, it should be created before the curl command, read the note below. 
# In releases older than Debian 12 and Ubuntu 22.04, folder /etc/apt/keyrings does not exist by default.
# sudo mkdir -p -m 755 /etc/apt/keyrings

curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.32/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
sudo chmod 644 /etc/apt/keyrings/kubernetes-apt-keyring.gpg
```
### Add the Appropriate Kubernetes apt Repository.
```bash
echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.32/deb/ /' | sudo tee /etc/apt/sources.list.d/kubernetes.list
sudo chmod 644 /etc/apt/sources.list.d/kubernetes.list
```
### Update apt package index, then install kubectl, kubeadm, and kubectl
```bash
sudo apt-get update
sudo apt install -y kubelet kubeadm kubectl
```

---

## Step 5: Install Minikube
```bash
curl -LO https://github.com/kubernetes/minikube/releases/latest/download/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube && rm minikube-linux-amd64
```

---

## Step 6: Install Helm
### Apt:
```bash
curl https://baltocdn.com/helm/signing.asc | gpg --dearmor | sudo tee /usr/share/keyrings/helm.gpg > /dev/null
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/helm.gpg] https://baltocdn.com/helm/stable/debian/ all main" | sudo tee /etc/apt/sources.list.d/helm-stable-debian.list
sudo apt-get update
sudo apt-get install helm
```
### Snap:
```bash
sudo snap install helm --classic
```

---

## Step 7: Install Cilium :)
### Add Cilium Repository To Helm
```bash
helm repo add cilium https://helm.cilium.io/
helm repo update
```

---

## Special Notes
Cilium is not a stand alone app. It must be deployed onto a kubernetes cluster. Once you have cilium in helm you can deploy it onto any clusters you make. The first deployment and star wars demo will show how to deploy clusters, install cilium onto them, and use functionality.

---

## Links
[Cilium Hardware Requirements](https://docs.cilium.io/en/stable/operations/system_requirements/)
[Cilium Network Plugins](https://kubernetes.io/docs/concepts/extend-kubernetes/compute-storage-net/network-plugins/#network-plugin-requirements)
[Docker Install](https://docs.docker.com/engine/install/ubuntu/)
[Kubernetes Install](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/)
[MiniKube Install](https://minikube.sigs.k8s.io/docs/start/?arch=%2Flinux%2Fx86-64%2Fstable%2Fbinary+download)
[Helm Install](https://helm.sh/docs/intro/install/)
[Offical Cilium Install Using Helm](https://docs.cilium.io/en/stable/installation/k8s-install-helm/)