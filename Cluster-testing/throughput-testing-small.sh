#!/bin/bash

# make sure you run kidn create cluster
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

# Step 2: Deploy iPerf3 Server Pod
echo "Deploying iPerf3 server pod:"
kubectl run $SERVER_POD_NAME --image=networkstatic/iperf3 --namespace=$NAMESPACE --command -- iperf3 -s

# Step 3: Deploy iPerf3 Client Pod
echo "Deploying iPerf3 client pod: "
kubectl run $CLIENT_POD_NAME --image=networkstatic/iperf3 --namespace=$NAMESPACE --command -- sleep infinity

# Step 4: Deploy iPerf3 Exporter
echo "Deploying iPerf3 exporter pod:"
kubectl run $EXPORTER_POD_NAME --image=prom/iperf3-exporter --namespace=$NAMESPACE --port=9100

# Step 5: Wait for Pods to Be Ready
echo "Waiting for server pod to be ready:"
kubectl wait --for=condition=Ready pod/$SERVER_POD_NAME -n $NAMESPACE --timeout=60s

echo "Waiting for client pod to be ready:"
kubectl wait --for=condition=Ready pod/$CLIENT_POD_NAME -n $NAMESPACE --timeout=60s

echo "Waiting for exporter pod to be ready:"
kubectl wait --for=condition=Ready pod/$EXPORTER_POD_NAME -n $NAMESPACE --timeout=60s

# Step 6: Get Server Pod IP
SERVER_IP=$(kubectl get pod $SERVER_POD_NAME -n $NAMESPACE -o jsonpath='{.status.podIP}')
echo "Server pod IP: $SERVER_IP"

# Step 7: Run iPerf3 Test (No need to save results to a JSON file)
echo "Running iPerf3 test from client to server..."
kubectl exec -it $CLIENT_POD_NAME -n $NAMESPACE -- iperf3 -c $SERVER_IP --json

# Step 8: Verify Exporter Metrics
EXPORTER_IP=$(kubectl get pod $EXPORTER_POD_NAME -n $NAMESPACE -o jsonpath='{.status.podIP}')
echo "iPerf3 Exporter IP: $EXPORTER_IP"
echo "Verify metrics at: http://$EXPORTER_IP:9100/metrics"

echo "Network performance test and metric export complete."
