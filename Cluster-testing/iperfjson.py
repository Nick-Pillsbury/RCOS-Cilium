import subprocess
import json
import time
import socket
import threading
from prometheus_client import start_http_server, Gauge, generate_latest
from flask import Flask

app = Flask(__name__)

iperf3_client_bitrate = Gauge('iperf3_client_bitrate', 'Client throughput in bits per second')
iperf3_server_bitrate = Gauge('iperf3_server_bitrate', 'Server throughput in bits per second')

# Configuration
SERVER_DNS = "iperf3-server.default.svc.cluster.local"
SERVER_PORT = 5202
IPERF3_INTERVAL = 30  # Interval to run iPerf3 tests (in seconds)

def resolve_server_ip(dns_name):
    """
    Resolve the server IP from DNS name (can be a Kubernetes service or regular DNS name).
    """
    try:
        ip_address = socket.gethostbyname(dns_name)
        return ip_address
    except socket.gaierror as e:
        print(f"Error resolving DNS: {e}")
        return None

def run_iperf3():
    # Resolve the server's IP address
    server_ip = resolve_server_ip(SERVER_DNS)
    if not server_ip:
        print(f"Error: Unable to resolve server IP for {SERVER_DNS}")
        return  # Skip if we can't resolve the IP

    # Run iPerf3 test and get results
    result = subprocess.run(
        ["iperf3", "-c", server_ip, "-p", str(SERVER_PORT), "-t", "10", "-J"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    output = result.stdout
    data = json.loads(output)

    # Extract client and server bitrate
    client_bitrate = data['end']['sum_received']['bits_per_second']
    server_bitrate = data['end']['sum_sent']['bits_per_second']

    # Update Prometheus metrics
    iperf3_client_bitrate.set(client_bitrate)
    iperf3_server_bitrate.set(server_bitrate)

def periodic_iperf3_runner():
    while True:
        run_iperf3()
        time.sleep(IPERF3_INTERVAL)

@app.route('/metrics')
def metrics():
    return generate_latest()

if __name__ == "__main__":
    # Start Prometheus HTTP server
    start_http_server(8020)

    # Start iPerf3 in a background thread
    threading.Thread(target=periodic_iperf3_runner, daemon=True).start()

    # Start Flask server
    app.run(host='0.0.0.0', port=8030)
