
# Cilium Setup Scripts

This guide explains what the two key scripts do in your GitHub repo and how to use them to set up a Kubernetes cluster with **Cilium** as the CNI (Container Network Interface).

---

## Script 1: `install_cilium.sh`

**Purpose:**  
This script prepares an Ubuntu environment by installing all the dependencies needed to run a Kubernetes cluster with Minikube and Cilium.

### What it does:

1. **System Updates**
   - Updates the package list and upgrades installed packages:
     ```bash
     sudo apt update && sudo apt upgrade -y
     ```

2. **Installs Docker**
   - Installs Docker and its CLI tools so Kubernetes can run containers.

3. **Installs Kubernetes Tools**
   - Installs `kubeadm`, `kubelet`, and `kubectl`, the core tools to initialize and manage clusters.

4. **Installs Minikube**
   - Downloads and installs Minikube, a local Kubernetes distribution that runs in a VM or container.

5. **Installs Helm**
   - Adds the Helm package manager for Kubernetes so you can install Cilium easily.

6. **Adds the Cilium Helm Repository**
   - Prepares the system to install Cilium via Helm:
     ```bash
     helm repo add cilium https://helm.cilium.io/
     ```
---

## Script 2: `deploy_cluster.sh`

**Purpose:**  
This script actually spins up the Kubernetes cluster and installs Cilium as the CNI.

### What it does:

1. **Starts Minikube with Cilium**
   - Starts a local Kubernetes cluster using Minikube and sets Cilium as the network plugin:
     ```bash
     minikube start --cpus 4 --memory 8192 --cni=cilium
     ```

2. **Installs Cilium via Helm**
   - Uses Helm to install Cilium in the `kube-system` namespace with a predefined configuration:
     ```bash
     helm install cilium cilium/cilium --namespace kube-system ...
     ```

3. **Restarts Unmanaged Pods**
   - Restarts pods that were running before Cilium was installed so that they are managed by the new CNI.

4. **Installs Cilium CLI**
   - Installs the command-line tool to interact with Cilium (optional but helpful for debugging and monitoring).

5. **Verifies Installation**
   - Runs `cilium status` to confirm that the Cilium agent is up and running correctly.

---

## How to Use These Scripts

### 1. Clone the Repository
```bash
git clone https://github.com/Nick-Pillsbury/RCOS-Cilium.git
cd RCOS-Cilium/Nick-Pillsbury/Auto_Setup/
```

### 2. Make Scripts Executable
```bash
chmod +x install_cilium.sh deploy_cluster.sh
```

### 3. Run the Setup
Run on a clean Ubuntu server:
```bash
./install_cilium.sh
./deploy_cluster.sh
```

---

## After Setup

Check that everything is working:
```bash
kubectl get nodes
kubectl get pods -A
cilium status
```