# Integrating iper3 tesitng into Graphaa:



1. **Set up Iperf3 output to a json file:**

Small Tests:

Run the command:
```bash
./throughput-testing-small.sh
```

Large Tests:
Run the command:
```bash
./throughput-testing-large.sh
```

2. **Set up Prometheus**

a. Add the Prometheus Helm repository:
```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
```

b. Install Prometheus
```bash
helm install prometheus prometheus-community/prometheus --namespace monitoring --create-namespace
```

3. Convert Json to Prometheus Metrics:

a. Run iperf3Export.py
```python
python iperf3Export.py
```