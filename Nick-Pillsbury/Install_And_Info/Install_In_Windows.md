# Installing Cilium on Windows Using Helm
This guide walks through installing Cilium using Helm and all necessary dependencies on a **Windows** system.

---

## Prerequisites
Ensure your system meets the following requirements:
- **Windows 10/11**
- **CPU: 2+ vCPUs**
- **RAM: 8+ GB**
- **Disk: 20+ GB**
- **Virtualization Enabled in BIOS**

---

## Step 1: Install Docker Desktop
1. Download the install.exe and follow the steps.
    
    https://docs.docker.com/desktop/setup/install/windows-install/

2.
    Run Docker Desktop and make it opens / runs

---

## Step 2: Install Minikube / Kubernetes
```bash
winget install Kubernetes.minikube
```

---

## Step 3: Install Helm
```bash
winget install Helm.Helm
```

---

## Step 4: Install Cilium CLI
```bash
winget install Cilium.CiliumCLI
```

---

## Step 5: Install Cilium In Helm
```bash
helm repo add cilium https://helm.cilium.io/
helm repo update
```

---

## Step 6: Reboot
Reboot to apply all the changes!

---

## Special Notes
Cilium is not a standalone app. It must be deployed onto a Kubernetes cluster. Once you have Cilium in Helm, you can deploy it onto any clusters you make. The first deployment and Star Wars demo will show how to deploy clusters, install Cilium onto them, and use its functionality.

---

## Links
- [Cilium Hardware Requirements](https://docs.cilium.io/en/stable/operations/system_requirements/)
- [Cilium Network Plugins](https://kubernetes.io/docs/concepts/extend-kubernetes/compute-storage-net/network-plugins/#network-plugin-requirements)
- [Helm Install](https://helm.sh/docs/intro/install/)
- [Official Cilium Install Using Helm](https://docs.cilium.io/en/stable/installation/k8s-install-helm/)
- [Packages Available With Winget](https://winstall.app/)