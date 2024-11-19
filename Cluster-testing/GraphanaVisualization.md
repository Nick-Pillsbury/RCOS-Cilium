# Integrating iper3 tesitng into Graphaa:



1. **Set up Iperf3 output to a json file:**

Small Tests:

Run the command:
```bash
kubectl exec -it iperf3-client -- iperf3 -c <server-ip> --json > iperf3-results.json
```

2.