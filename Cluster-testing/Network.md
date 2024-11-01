
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


## **Larger Data Testing(Calico Testing)**

** Make sure you do this **:
```
kubectl apply -f https://docs.projectcalico.org/manifests/calico.yaml
```

1. **Create a Large Cluster for Calico and Cilium:**
   ```bash
   kind create cluster --config cilium-cluster-config.yaml --name cilium-cluster
   kind create cluster --config calico-cluster-config.yaml --name calico-cluster
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

   C. Deploy iperf3 clinet pod to test throughput:
   ```bash
   kubectl run iperf-client --image=networkstatic/iperf3 --command -- iperf3 -c iperf-server.default.svc.cluster.local
   ```

4. **Testing Beigns:**

   A. Make sure pod are running(iperf-client and ierpf-server status should be RUNNING).
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
   kubectl describe node <node-name>
   ```

   <br>
   Or try examining different different events:
   <br>
   This can check what is stopped the pods from running.

   ``` bash
   kubectl describe pod iperf-client
   kubectl describe pod iperf-server
   ```


Try comparing parallel streams in a heavy load:
```bash
kubectl exec iperf-client -- iperf3 -c iperf-server.default.svc.cluster.local -P 10
```
---

Check logs to get more info on;
```bash
kubectl logs iperf-server

```

---

## **Conclusion**

Calico performed slightly better in terms of throughput, packet retransmissions, and congestion window growth, but the differences were minimal.
