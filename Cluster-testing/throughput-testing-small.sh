#!/bin/bash

NAMESPACE="network-cilium-performance-test"
SERVER_POD_NAME="iperf3-server"
CLIENT_POD_NAME="iperf3-client"
EXPORTER_POD_NAME="iperf3-exporter"

# Step 1: Create Namespace
echo "Creating namespace: $NAMESPACE"
kubectl create namespace $NAMESPACE

# Step 1.5: Create Service Account and Bind Permissions
echo "Creating service account for the namespace"
kubectl create serviceaccount default -n $NAMESPACE
kubectl create rolebinding default-sa-binding \
  --clusterrole=edit \
  --serviceaccount=$NAMESPACE:default \
  --namespace=$NAMESPACE

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

# Step 6: Run iPerf3 Test and Save Output in JSON Format
echo "Running iPerf3 test from client to server..."
kubectl exec -it $CLIENT_POD_NAME -n $NAMESPACE -- iperf3 -c $SERVER_IP --json > iperf3-results.json

echo "Network performance test complete."


