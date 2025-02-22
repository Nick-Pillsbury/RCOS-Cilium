# Set Up a Multi-Cluster with Cilium ClusterMesh with Network Policies

----

### Set Up Multi-Clusters with Minikube
##### Create two separate Kubernetes clusters (cluster1 and cluster2) using Minikube.
- minikube start -p cluster1 --network-plugin=cni --cni=cilium
- minikube start -p cluster2 --network-plugin=cni --cni=cilium

##### Verify both are running with.
- kubectl config get-contexts

---
### Deploy Cilium on Both Clusters
##### Enable ClusterMesh to allow pods in one cluster to talk to pods in the another.
- cilium clustermesh enable --context cluster1 --service-type NodePort
- cilium clustermesh enable --context cluster2 --service-type NodePort


###### Exchange ClusterMesh configuration between clusters
- cilium clustermesh status --context cluster1
- cilium clustermesh status --context cluster2

---
### Deploy a Stateful Application