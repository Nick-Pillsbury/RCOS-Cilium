from prometheus_client import start_http_server, Gauge
import json
import time

iperf_bandwidth = Gauge("iperf_bandwidth_bps", "Bandwidth in bits per second")
iperf_retransmits = Gauge("iperf_retransmits", "Number of retransmissions")

def parse_iperf_results(file_path):
    try:
        with open(file_path, "r") as file:
            data = json.load(file)

        # take metrics
        bandwidth = data["end"]["sum_received"]["bits_per_second"]
        retransmits = data["end"]["sum_received"].get("retransmits", 0)

        # Update metrics
        iperf_bandwidth.set(bandwidth)
        iperf_retransmits.set(retransmits)
    except Exception as e:
        print(f"Error parsing iPerf3 results: {e}")

if __name__ == "__main__":
    start_http_server(8000)
    print("Prometheus Exporter started on port 8000")

    while True:
        # Parse every 10 seconds
        parse_iperf_results("iperf3-results.json")
        time.sleep(10)
