#!/bin/bash

set -e

# Configuration
MINIKUBE_MEMORY="8192"
MINIKUBE_CPUS="4"
CILIUM_VERSION="1.17.1"

echo -e "\n\033[1;34m=== Starting Cilium Deployment ===\033[0m"

# Start Minikube cluster
echo -e "\n\033[1;36m[1/5] Creating Minikube cluster...\033[0m"
minikube start --memory=$MINIKUBE_MEMORY --cpus=$MINIKUBE_CPUS

# Install Cilium via Helm
echo -e "\n\033[1;36m[2/5] Installing Cilium ${CILIUM_VERSION}...\033[0m"
helm repo add cilium https://helm.cilium.io/
helm install cilium cilium/cilium --version $CILIUM_VERSION --namespace kube-system

# Restart unmanaged pods
echo -e "\n\033[1;36m[3/5] Restarting unmanaged pods...\033[0m"
kubectl get pods --all-namespaces -o custom-columns=NAMESPACE:.metadata.namespace,NAME:.metadata.name,HOSTNETWORK:.spec.hostNetwork --no-headers=true | grep '<none>' | awk '{print "-n "$1" "$2}' | xargs -L 1 -r kubectl delete pod

# Install Cilium CLI
echo -e "\n\033[1;36m[4/5] Installing Cilium CLI...\033[0m"
CILIUM_CLI_VERSION=$(curl -s https://raw.githubusercontent.com/cilium/cilium-cli/main/stable.txt)
CLI_ARCH="amd64"
if [ "$(uname -m)" = "aarch64" ]; then CLI_ARCH="arm64"; fi
curl -L --fail --remote-name-all https://github.com/cilium/cilium-cli/releases/download/${CILIUM_CLI_VERSION}/cilium-linux-${CLI_ARCH}.tar.gz{,.sha256sum}
sha256sum --check cilium-linux-${CLI_ARCH}.tar.gz.sha256sum
sudo tar xzvfC cilium-linux-${CLI_ARCH}.tar.gz /usr/local/bin
rm cilium-linux-${CLI_ARCH}.tar.gz{,.sha256sum}

# Validate installation
echo -e "\n\033[1;36m[5/5] Validating installation...\033[0m"
cilium status --wait

echo -e "\n\033[1;32m=== Deployment Complete! ===\033[0m"
echo "Your Cilium-enabled Kubernetes cluster is ready."
echo "You can now deploy your applications to the cluster."

# Display cluster info
echo -e "\n\033[1;33mCluster Information:\033[0m"
kubectl cluster-info