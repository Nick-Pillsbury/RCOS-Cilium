# Integrating iPerf3 Testing with Prometheus Monitoring

This guide walks through setting up iPerf3 testing with Prometheus monitoring and Grafana visualization in your environment.

## Prerequisites

- Docker and Docker Compose installed
- Helm package manager
- kubectl configured with your cluster
- Grafana

## 1. Running iPerf3 Tests

### Small-Scale Testing
Execute the small test suite:
```bash
./throughput-testing-small.sh
```

### Large-Scale Testing
Execute the comprehensive test suite:
```bash
./throughput-testing-large.sh
```

## 2. Prometheus Setup

### Adding Prometheus Repository
```bash
# Add the Prometheus Helm repository
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts

# Update Helm repositories
helm repo update
```

### Setting up Pushgateway
Deploy Pushgateway to temporarily store metrics:
```bash
docker run -d -p 9091:9091 prom/pushgateway
```

### Installing Prometheus
Deploy Prometheus in your cluster:
```bash
helm install prometheus prometheus-community/prometheus \
    --namespace monitoring \
    --create-namespace
```

## 3. Docker Compose Configuration

Create a `docker-compose.yml` file in your project directory and start the services:
```bash
docker-compose up -d
```

## 4. Grafana Installation

### macOS
Install via Homebrew:
```bash
brew install grafana
```

### Windows
Download and install from: [Grafana Windows Installer](https://grafana.com/grafana/download?platform=windows)

## 5. Grafana Configuration

### Accessing Grafana
- URL: http://localhost:3000/login
- Default credentials:
  - Username: admin
  - Password: cilium

### Adding Prometheus Data Source ###
1. Navigate to Connections
2. Select Data Sources
3. Click "Add Data Source"
4. Choose "Prometheus"
5. Configure the connection settings

## Next Steps

After completing the setup:
1. Configure your Prometheus scrape configs to collect iPerf3 metrics
2. Create Grafana dashboards to visualize the performance data
3. Set up alerts for performance thresholds



