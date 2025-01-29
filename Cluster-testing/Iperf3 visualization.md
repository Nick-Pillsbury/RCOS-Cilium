Iperf3 visaulziation on Prometheus with Grafana as visaulziation


Prequisties:
- Kind: creating cluster
- kubectl: manage kubernetes
- Helm: manage Kubernets clusters
- Cilium
- Docker: to run kind

Cilium is a networking and security layer for Kubernetes by using EBPF:
- network visibility
- High-performance networking 

** 1. Run custom configuraito of kubernetes cluster: **
```bash 
kind create cluster --name cilium-cluster --config kind-config.yaml
```

- Add Cilium Helm repostiory and deploy Cilium
```bash
helm repo add cilium https://helm.cilium.io/
helm repo update
```

- Deploy Cilium as CNI:
```bash
helm install cilium cilium/cilium --namespace kube-system
```

- Verify Cilium Insstallation:
```bash
kubectl get pods -n kube-system | grep cilium
```

- Customize the Cilium configuration during installation:
```bash
helm upgrade cilium cilium/cilium -f values.yaml
```

- Enable External IP Traffic in Cilium
```bash
helm upgrade cilium cilium/cilium \
  --namespace kube-system \
  --set enableIPv4Masquerade=true \
  --set enableExternalIPs=true \
  --set metrics.enabled=true \
  --set metrics.prometheus.enabled=true
```

** 2. Deploy Prometheus and Grafana: **

1. Add Helm Repository for Prometheus and Grafana:
```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
```
2. Install Prometheus:
```bash
helm install prometheus prometheus-community/prometheus --namespace monitoring --create-namespace
```

3. Verify Prometheus Installation:
```bash
kubectl get pods -n monitoring
```

4. Install Grafana:
```bash
helm install grafana grafana/grafana --namespace monitoring
```

5. Forward Grafana to your local machine:
```bash
kubectl port-forward svc/grafana 3000:80 -n monitoring
#Username should be admin
```
6. Retrieve Password:
```bash
kubectl get secret --namespace monitoring grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo

```

** 3. Scrape Cilium Metrics into Prometheus **
1. Verify Cilium is running and exposing metrics:
```bash
kubectl get pods -n kube-system | grep cilium
```

2. Access metrics with Kubernetes service:
```bash
kubectl apply -f cilium-agent-metrics-service.yaml
kubectl apply -f cilium-operator-metrics-service.yaml
```

3. Port-Forward to Access the Metrics:
Cilium-agent:
```bash
kubectl port-forward -n kube-system svc/cilium-agent-metrics 9190:9190
```
Cilium-operator:
```bash
kubectl port-forward -n kube-system svc/cilium-operator-metrics 9091:9091
```

4. Allow Prometheus to scrape metrics:
```bash
kubectl apply -f prometheus-config.yaml
```

5. Verify Prometheus Scraping:
```bash
# kubectl port-forward -n monitoring svc/prometheus-server 9092:9090
kubectl port-forward -n monitoring svc/prometheus-server 9090:9090
```

6. Visit http://localhost:9092/targets to see targets and make sure the operator and agents are on the "UP" state 

Query: {__name__=~"cilium_.*"}

** 4. Vlsualize Metrics with Grafana ** 

1. Access Grafana Dashboard:
```bash
kubectl port-forward svc/grafana 3000:80 -n monitoring (CHNAGE TO 9090???)
```
2. Add Prometheus as a Data Source:
Set URL to :
http://prometheus-server.monitoring.svc.cluster.local:80

3. Import Prebuilt Dashboard:
Click new and import and create take a json file(operator, agent, or take an ID)

https://grafana.com/grafana/dashboards/16611-cilium-metrics/
Pull from here (agent):

Pull from here (operator):
https://github.com/cilium/cilium/blob/main/install/kubernetes/cilium/files/cilium-operator/dashboards/cilium-operator-dashboard.json
**check why some are unkown**

<!-- 1.  Setting up Kubernetes Environment with Cilium
2.  Deploy Prometheus and Grafana
3. Set Up iPerf3 Testing Pods
4. Modify iPerf3 Test Scripts for Metrics Collection
5.  Scrape iPerf3 Metrics into Prometheus **
6. Visualize iPerf3 Metrics in Grafana
 -->

1.  Setting up Kubernetes Environment with Cilium
2.  Deploy Prometheus and Grafana
3. Scrape CIlium Metrics into Prometheus
4. Visualize cilium Metrics in Grafana

kubectl get pods -n kube-system | grep cilium
helm upgrade cilium cilium/cilium --namespace kube-system -f values.yaml

(kubectl get pods -n monitoring) crashloopbackoff for iperf3-lcient-server
Resume
Implemented Prometheus and Grafana to monitor and visualize Cilium metrics, enabling detailed insights into cluster networking performance and security policies.
Configured and optimized Prometheus to scrape metrics from Cilium agents and operators, ensuring real-time monitoring and diagnostics.
Built and deployed end-to-end observability solutions, leveraging Helm for seamless management of Kubernetes resources and efficient troubleshooting.

1. Setting up Kubernetes Environment with Cilium

Create a Kind cluster and deploy Cilium as a CNI plugin with Helm.
Verify Cilium installation with kubectl.
2. Deploy Prometheus and Grafana

Use Helm to deploy Prometheus and Grafana into the cluster.
Configure Grafana for local access via port forwarding.
3. Scrape Cilium Metrics into Prometheus

Expose Cilium metrics with cilium-agent-metrics-service.yaml and cilium-operator-metrics-service.yaml.
Add Prometheus scrape configurations using prometheus-config.yaml.
Verify Prometheus is scraping Cilium metrics by visiting http://localhost:9092/targets.
4. Visualize Metrics in Grafana

Access the Grafana dashboard via http://localhost:3000.
Add Prometheus as a data source in Grafana.
Import prebuilt dashboards for Cilium (links provided for agent and operator dashboards).
Query metrics like {__name__=~"cilium_.*"} to visualize network performance and policy enforcement.