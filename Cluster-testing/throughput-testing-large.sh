#!/bin/bash

CLUSTER_NAME="calico-cluster"
NAMESPACE="network-calico-performance-test"
NGINX_DEPLOYMENT_NAME="nginx"
IPERF_SERVER_POD="iperf-server"
IPERF_CLIENT_POD="iperf-client"

# Step 1: Create a Kind Cluster with Calico
echo "Creating Kind cluster with Calico configuration..."
kind create cluster --config calico-cluster-config.yaml --name $CLUSTER_NAME

echo "Applying Calico:"
kubectl apply -f https://docs.projectcalico.org/manifests/calico.yaml

# Step 2: Create Namespace
echo "Creating namespace: $NAMESPACE"
kubectl create namespace $NAMESPACE

# Step 3: Deploy NGINX and Scale Pods
echo "Deploying NGINX deployment..."
kubectl create deployment $NGINX_DEPLOYMENT_NAME --image=nginx --namespace=$NAMESPACE

echo "Scaling NGINX deployment to 50 replicas..."
kubectl scale deployment $NGINX_DEPLOYMENT_NAME --replicas=50 --namespace=$NAMESPACE

# Step 4: Deploy iPerf3 Server and Client Pods
echo "Creating a headless service for iPerf3 server..."
cat <<EOF | kubectl apply -n $NAMESPACE -f -
apiVersion: v1
kind: Service
metadata:
  name: iperf-server
spec:
  selector:
    run: iperf-server
  ports:
  - protocol: TCP
    port: 5201
    targetPort: 5201
  clusterIP: None 
EOF

echo "Deploying iPerf3 server pod..."
kubectl run $IPERF_SERVER_POD --image=networkstatic/iperf3 --namespace=$NAMESPACE --command -- iperf3 -s

echo "Deploying iPerf3 client pod..."
cat <<EOF | kubectl apply -n $NAMESPACE -f -
apiVersion: v1
kind: Pod
metadata:
  name: $IPERF_CLIENT_POD
spec:
  containers:
  - name: iperf-client
    image: networkstatic/iperf3
    command:
    - sleep
    - infinity
EOF

# Step 5: Wait for Pods to Be Ready
echo "Waiting for pods to be ready..."
kubectl wait --for=condition=Ready pod/$IPERF_SERVER_POD -n $NAMESPACE --timeout=120s
kubectl wait --for=condition=Ready pod/$IPERF_CLIENT_POD -n $NAMESPACE --timeout=120s

# Step 6: Run Throughput Test
echo "Running throughput test with 10 parallel streams..."
kubectl exec -n $NAMESPACE $IPERF_CLIENT_POD -- iperf3 -c iperf-server.default.svc.cluster.local -P 10

# Step 7: View Logs for Analysis
echo "Fetching iPerf3 server logs for analysis..."
kubectl logs -n $NAMESPACE $IPERF_SERVER_POD

# Cleanup
echo "To delete the cluster, run: kind delete cluster --name $CLUSTER_NAME"
