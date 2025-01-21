import subprocess
from prometheus_client import start_http_server, Gauge

iperf3_metric = Gauge('iperf3_test_metric', 'iPerf3 test metrics', ['type'])

def run_iperf3():
    result = subprocess.run(['iperf3', '-c', 'localhost', '-p', '5201', '-t', '10'], capture_output=True, text=True)

    lines = result.stdout.splitlines()
    for line in lines:
        if "bits/sec" in line:
            throughput = float(line.split()[6])  
            iperf3_metric.labels(type="throughput").set(throughput)

def main():
    start_http_server(9100)
    
    while True:
        run_iperf3()

if __name__ == "__main__":
    main()
