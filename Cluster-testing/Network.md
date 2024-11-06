
# Network Performance Testing with Cilium and Calico

## **Overview**
This guide provides steps to measure **throughput** and **latency** across cluster nodes using **Cilium** and **Calico** as CNIs. We will deploy test pods using `iperf3` to measure data transfer speeds and the delay between packet transmissions.

---

iperf3 is an open-source tool that measures network bandwidth and throughput between two systems.

Throughput is the rate at which data is delivered over a network connection which canb be measured in Mbps and Gbps.

## **Cilium Network Performance Testing**

### **Steps**

1. **Add the Cilium Helm Repository and Install Cilium**
   ```bash
   helm repo add cilium https://helm.cilium.io/
   helm install cilium cilium/cilium --version 1.12.0 --namespace kube-system
   ```

2. **Create a Namespace for Throughput Testing**
   ```bash
   kubectl create namespace network-cilium-performance-test
   ```

3. **Deploy Testing Pods using iperf3**

   - **Deploy server pod**:
     ```bash
     kubectl run iperf3-server --image=networkstatic/iperf3 --namespace=network-cilium-performance-test --command -- iperf3 -s
     ```

   - **Deploy client pod**:
     ```bash
     kubectl run iperf3-client --image=networkstatic/iperf3 --namespace=network-cilium-performance-test --command -- sleep infinity
     ```

4. **Start the Network Performance Test (Throughput)**

   - **Get the server pod IP**:
     ```bash
     kubectl get pod -o wide -n network-cilium-performance-test iperf3-server
     ```

   - **Run the client test using the server's IP**:
     ```bash
     kubectl exec -it iperf3-client -n network-cilium-performance-test -- iperf3 -c <server-ip>
     ```

### **Analysis**

The throughput test ran for 10 seconds, measuring the data sent between client and server pods. The average throughput was **85.2 Gbps**, with only **9 retransmissions**, indicating a stable network with minimal packet loss.

![Cilium Network Test](/Testing/Cilium-network-test.png)

---

## **Calico Network Performance Testing**

### **Steps**

1. **Create a Namespace for Throughput Testing**
   ```bash
   kubectl create namespace network-calico-performance-test
   ```

2. **Deploy Testing Pods using iperf3**

   - **Deploy server pod**:
     ```bash
     kubectl run iperf3-server --image=networkstatic/iperf3 --namespace=network-calico-performance-test --command -- iperf3 -s
     ```

   - **Deploy client pod**:
     ```bash
     kubectl run iperf3-client --image=networkstatic/iperf3 --namespace=network-calico-performance-test --command -- sleep infinity
     ```

3. **Start the Network Performance Test (Throughput)**

   - **Get the server pod IP**:
     ```bash
     kubectl get pod -o wide -n network-calico-performance-test iperf3-server
     ```

   - **Run the client test using the server's IP**:
     ```bash
     kubectl exec -it iperf3-client -n network-calico-performance-test -- iperf3 -c <server-ip>
     ```

### **Analysis**

The throughput test ran for 10 seconds, measuring the data sent between the client and server pods. The average throughput was **85.8 Gbps**, with only **8 retransmissions**, indicating a stable network with minimal packet loss.

![Calico Network Test](/Testing/Calico-network-test.png)

---

**Deleting Containers on Docker:**

Run "docker ps" to check how many containers are running: 
```bash
docker ps
```
To stop and remove all containers:
```bash
docker rm -f $(docker ps -a -q)
```


## **Larger Data Testing (Calico Testing)**


1. **Create a Large Cluster for Calico:**
   ```bash
   kind create cluster --config calico-cluster-config.yaml --name calico-cluster
   ```
   To delete:
   ```bash
   kind delete cluster --name calico-cluster
   ```

** Make sure you do this **:
```
<!-- kubectl apply -f https://docs.projectcalico.org/manifests/calico.yaml -->
```

2. **Increase the Number of Pods**
   To scale up the workload, first create ngnix deployment then increase the number of pods for throughput testing adn creating high traffic. Example to create 50 NGINX pods:
   ```bash
   kubectl create deployment nginx --image=nginx
   kubectl scale deployment nginx --replicas=50
   ```

3. ***Throughput Testing***

   After deploying the pods, we need to set up a iperf3 server for thorughput testing

   A. Create a headless service for the server:
   ```bash
   kubectl apply -f iperf-server.yaml
   ```

   B. Deply iperf3 server pod:
   ```bash
   kubectl run iperf-server --image=networkstatic/iperf3 --command -- iperf3 -s
   ```

   C. Deploy iperf-client Pod:
   ```bash
   kubectl apply -f iperf-client.yaml
   ```

   C. Run throughput testing
   ```bash
   kubectl exec iperf-client -- iperf3 -c iperf-server.default.svc.cluster.local -P 10
   ```

   ** Make sure you do this **:
```
kubectl apply -f https://docs.projectcalico.org/manifests/calico.yaml
```

4. **Chek Node Status:**

   A. Make sure all pods are running(iperf-client and ierpf-server status should be RUNNING).
   ```
   kubectl get pods
   ```

   Debugging Using Terminal:
   Make sure all nodes are ready.
   ```
   kubectl get nodes
   ```

   For more infomration on why a node is failing use:
   ```
   kubectl describe pod iperf-client
   kubectl describe pod iperf-server
   ```

5. **Run Larger Test**

Try running parallel streams in a heavy load:
```bash
kubectl exec iperf-client -- iperf3 -c iperf-server.default.svc.cluster.local -P 10
```

This will test with 10 parallel streams to simulate a higher load and measure performance more rigorously.

Check logs to get more info on;
```bash
kubectl logs iperf-server

```

6. **View and Analyze Results**

Check for Test Results:
```bash
kubectl logs iperf-server
```
<br>
This will allow you to see detailed output of the iperf test with metrics like transfer size, bitrate, and retransmissions.
<br>

![Cilium Large Test:]( /Testing/CiliumLargeTestResultpt1.png)


![Cilium Large Test:]( /Testing/CiliumLargeTestResultpt2.png)

![Cilium Large Test:]( /Testing/CiliumLargeTestResultpt3.png)

<br>
The iperf3 network large test result for Cilium reveal that the iperf-client successfully connected to the iperf-server on 10 parallel streams, measuring a high network throughput. Throughout the 10 seconds, the client transferred a total of 39.4 GB which averaged a rate of 33.8 GB/sec. The individual streams consistently reached bitrates of around 3.38–4.56 Gbits/sec, with some fluctuation likely due to minor retransmissions (113 in total). This performance test provides a comprehensive look at network stability and bandwidth, demonstrating that the connection can sustain high-speed data transfer with minimal packet loss and congestion.

---
## **Conclusion**

**Small Test Case::**
Calico performed slightly better in terms of throughput, packet retransmissions, and congestion window growth, but the differences were minimal.
