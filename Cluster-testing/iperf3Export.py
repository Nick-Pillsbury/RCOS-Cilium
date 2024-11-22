from prometheus_client import start_http_server, Gauge
import json
import time

# Prometheus metrics
total_bandwidth = Gauge("iperf_total_bandwidth_bps", "Total bandwidth in bits per second")
total_retransmits = Gauge("iperf_total_retransmits", "Total retransmissions")
max_rtt = Gauge("iperf_max_rtt_ms", "Maximum RTT in milliseconds")
min_rtt = Gauge("iperf_min_rtt_ms", "Minimum RTT in milliseconds")
mean_rtt = Gauge("iperf_mean_rtt_ms", "Mean RTT in milliseconds")
cpu_utilization_host_total = Gauge("iperf_cpu_utilization_host_total", "Total CPU utilization on the host")
cpu_utilization_host_user = Gauge("iperf_cpu_utilization_host_user", "User CPU utilization on the host")
cpu_utilization_host_system = Gauge("iperf_cpu_utilization_host_system", "System CPU utilization on the host")
cpu_utilization_remote_total = Gauge("iperf_cpu_utilization_remote_total", "Total CPU utilization on the remote")
cpu_utilization_remote_user = Gauge("iperf_cpu_utilization_remote_user", "User CPU utilization on the remote")
cpu_utilization_remote_system = Gauge("iperf_cpu_utilization_remote_system", "System CPU utilization on the remote")


def parse_iperf_results(file_path):
    try:
        # Load iPerf3 JSON output
        with open(file_path, "r") as file:
            data = json.load(file)

        # Extract metrics from the "end" section
        end_data = data.get("end", {})
        sum_sent = end_data.get("sum_sent", {})
        cpu_utilization = end_data.get("cpu_utilization_percent", {})
        streams = end_data.get("streams", [{}])[0]

        # Update Prometheus metrics
        total_bandwidth.set(sum_sent.get("bits_per_second", 0))
        total_retransmits.set(sum_sent.get("retransmits", 0))
        max_rtt.set(streams.get("sender", {}).get("max_rtt", 0))
        min_rtt.set(streams.get("sender", {}).get("min_rtt", 0))
        mean_rtt.set(streams.get("sender", {}).get("mean_rtt", 0))

        # CPU utilization
        cpu_utilization_host_total.set(cpu_utilization.get("host_total", 0))
        cpu_utilization_host_user.set(cpu_utilization.get("host_user", 0))
        cpu_utilization_host_system.set(cpu_utilization.get("host_system", 0))
        cpu_utilization_remote_total.set(cpu_utilization.get("remote_total", 0))
        cpu_utilization_remote_user.set(cpu_utilization.get("remote_user", 0))
        cpu_utilization_remote_system.set(cpu_utilization.get("remote_system", 0))

    except Exception as e:
        print(f"Error parsing iPerf3 results: {e}")


if __name__ == "__main__":
    # Start Prometheus metrics server on port 8000
    start_http_server(8000)
    print("Prometheus Exporter started on port 8000")

    # Monitor JSON file and update metrics every 10 seconds
    while True:
        parse_iperf_results("iperf3-results.json")
        time.sleep(10)
