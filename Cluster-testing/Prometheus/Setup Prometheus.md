# Setting up Prometheus

1. Add instruction
```bash
export PROMETHEUS_CONFIG_DIR=./Prometheus
```

2. Start up docker container using environment variable
``` bash
docker run -d -p 9090:9090 -v $PROMETHEUS_CONFIG_DIR/prometheus.yml:/etc/prometheus/prometheus.yml prom/prometheus
```

3. Create a docker-compose.yml file in your project directory:
``` bash
docker-compose up -d
```
