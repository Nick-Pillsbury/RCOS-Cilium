# Integrating iPerf3 Testing with Prometheus Monitoring

This guide walks through setting up iPerf3 testing with Prometheus monitoring and Grafana visualization in your environment.

## Prerequisites
Make sure the following tools are installed:
- Docker and Docker Compose for containerized setup
- helm for package managing in Kubenetes
- kind for creating and manging clusters 
- iperf3 for testing
- Prometheus and Grafana for monitoring and visualization
- Python for executing scripts

## 1. Setup Kubernetes Environemnt with Cilium ##
Deploy cilium enabled cluster:
```bash
kind create cluster --config kind-config.yaml
```

Install Cilium:
```bash
cilium install
```

Verify Cilium deployment:
```bash
cilium status
```

## 2. Deploy Prometheus and Grafana: ##

Add Prometheus Monitoring Stack
```bash
# Add the Prometheus Helm repository
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
# Update Helm repository
helm repo update
# Install Prometheus Monitoring stack
helm install prometheus prometheus-community/kube-prometheus-stack --namespace monitoring --create-namespace
```

Install Grafana
```bash
# Add the Grafana repostiory
helm repo add grafana https://grafana.github.io/helm-charts
# Update the helm repostiory
helm repo update
# Install Grafana Mointorying
helm upgrade --install grafana grafana/grafana -n monitoring
```

Forward a local port on your machine to a port on a service running in your Kubernetes cluster:
```bash
# Access Grafana
kubectl port-forward svc/prometheus-grafana 3000:80 -n monitoring
```
## 2.Setup Grafana ##
Access Grafana UI

``` bash
# Get username and password
kubectl get secret --namespace monitoring grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
```

```bash
# Port forward to access Grafana
export POD_NAME=$(kubectl get pods --namespace monitoring -l "app.kubernetes.io/name=grafana,app.kubernetes.io/instance=grafana" -o jsonpath="{.items[0].metadata.name}")
kubectl --namespace monitoring port-forward $POD_NAME 8080:3000
```
(Keep this opened)

Now open localhost:3000 and use admin as username and password from the command before


### 4. Set Up Prometheus as a Data Source in Grafana ###
1. Go into http://localhost:8080/
2. Go to Connection -> Data Source
3. Select Prometheus
4. Configure Connection Settings to "http://prometheus-operated.monitoring.svc.cluster.local:9090"
5. Click "Save & Test"

## 5. Modify iPerf3 Test Scripts for Metrics Collection ## 
1. Build Docker image for Python app
```bash
docker build -t iperfjson-app .
```

# 3. Load the Docker image into the kind cluster
kind load docker-image "iperfjson-app:latest" --name kind

# 4. Apply the Kubernetes deployment
kubectl apply -f iperfjson-deployment.yaml 

## 6. Deploy iperf3 testing pods ##
```bash
# Create Kubernetes resources 
kubectl apply -f iperf3-server.yaml
kubectl apply -f iperf3-client.yaml
kubectl apply -f iperf3-service.yaml
kubectl apply -f iperfjson-deployment.yaml
kubectl apply -f iperf3-servicemonitor.yaml
# kubectl get pods -n kube-system -l k8s-app=cilium
# ServiceMonitors are required because they tell Prometheus how to discover and scrape metrics from Kubernetes services
kubectl apply -f kubectl cilium.yaml
kubectl apply -f cilium-servicemonitor.yaml
# To expose the Cilium metrics, you need to create a ClusterIP service that targets the Cilium pods.
kubectl apply -f cilium-metrics.yaml
kubectl apply -f iperf3-exporter-deployment.yaml

```

4. Check that the pods are running:
```bash
kubectl get pods
```

## 7. Scrape iperf3 and cilium metrics into Prometheus
1. Create a ConfigMap for Prometheus in your Kubernetes cluster:
```bash
kubectl create configmap prometheus-config --from-file=prometheus.yml -n monitoring --dry-run=client -o yaml | kubectl apply -f -
kubectl create namespace network-cilium-performance-test
```

```bash
kubectl apply -f iperf3exporter.yaml
kubectl apply -f prometheus.yml
kubectl apply -f prometheus-config.yaml
kubectl apply -f prometheus-deployment.yaml 
kubectl apply -f prometheus-role.yaml
kubectl apply -f prometheus-reader-role.yaml
kubectl apply -f prometheus-reader-binding.yaml
```

** Check for iperf3 and Cilium: **
kubectl get pods -n monitoring
kubectl get pods -n network-cilium-performance-test
kubectl apply -f iperf3-exporter-deployment.yaml


 iperf3 -s -p 5202
 iperf3 exporter is fialing check the yaml file

 docker build -t iperf3-exporter:latest .
kind load docker-image iperf3-exporter:latest --name kind

Port forward time:
```bash
kubectl port-forward -n monitoring prometheus-prometheus-kube-prometheus-prometheus-0 9090:9090
```
If its running:
```bash
lsof -i :9090
kill <PID>
```

kubectl logs iperf3-exporter-7cdc449f9d-z8spq -n network-cilium-performance-test? (DEBUG)
Error resolving DNS: [Errno -2] Name or service not known
Error: Unable to resolve server IP for iperf3-server.default.svc.cluster.local
Port:
8030 - Port for external service access (for Prometheus scraping)
9090 - defualt port for prometheus
9093 - exposed within the container (iperf3-exporter or prometheus-exporter), used to expose metrics for Prometheus scraping

## 5. Grafana Configuration

### Accessing Grafana
- URL: http://localhost:3000/login
- Default credentials:
  - Username: admin
  - Password: cilium

Overall Container Architecture:
Cilium + Kubernetes Cluster: Handles network performance and security.
Prometheus Server: Collects metrics from all services.
Grafana: Visualizes Prometheus metrics.
iPerf3 Server + Client: Perform network throughput tests.
Python Script: Collects and formats iPerf3 data for Prometheus.
Kubernetes Services: Ensures communication between iPerf3 client and server.

1.  Setting up Kubernetes Environment with Cilium
2.  Deploy Prometheus and Grafana
3. Set Up iPerf3 Testing Pods
4. Modify iPerf3 Test Scripts for Metrics Collection
5.  Scrape iPerf3 Metrics into Prometheus **
6. Visualize iPerf3 Metrics in Grafana
7. Automate and Scale Testing
8. (enable PVC)

Next steps:
Ensure Prometheus Scrapes Metrics: Check if Prometheus is scraping /metrics from iPerf3 and Cilium.
Configure iPerf3 Metrics Collection: Update Python script to expose metrics at /metrics.
Create Grafana Dashboards: Set up dashboards to visualize throughput, bandwidth, etc.
Automate Testing: Scale iPerf3 using Kubernetes HPA and automate tests with cronjobs.
Monitor & Adjust: Continuously monitor in Grafana and tweak configurations.
