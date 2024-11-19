#!/bin/bash

NAMESPACE="network-cilium-performance-test"
SERVER_POD_NAME="iperf3-server"
CLIENT_POD_NAME="iperf3-client"

# Step 1: Create Namespace
echo "Creating namespace: $NAMESPACE"
kubectl create namespace $NAMESPACE

# Step 2: Deploy Server Pod
echo "Deploying iPerf3 server pod:"
kubectl run $SERVER_POD_NAME --image=networkstatic/iperf3 --namespace=$NAMESPACE --command -- iperf3 -s

# Step 3: Deploy Client Pod
echo "Deploying iPerf3 client pod: "
kubectl run $CLIENT_POD_NAME --image=networkstatic/iperf3 --namespace=$NAMESPACE --command -- sleep infinity

# Step 4: Wait for Pods to Be Ready
echo "Waiting for server pod to be read: "
kubectl wait --for=condition=Ready pod/$SERVER_POD_NAME -n $NAMESPACE --timeout=60s

echo "Waiting for client pod to be ready:"
kubectl wait --for=condition=Ready pod/$CLIENT_POD_NAME -n $NAMESPACE --timeout=60s

# Step 5: Get Server Pod IP
SERVER_IP=$(kubectl get pod $SERVER_POD_NAME -n $NAMESPACE -o jsonpath='{.status.podIP}')
echo "Server pod IP: $SERVER_IP"

# Step 6: Run iPerf3 Test
echo "Running iPerf3 test from client to server..."
kubectl exec -it $CLIENT_POD_NAME -n $NAMESPACE -- iperf3 -c $SERVER_IP

echo "Network performance test complete."
