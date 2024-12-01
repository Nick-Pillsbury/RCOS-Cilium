
# Cilium Performance Benchmark

Performance testing is a form of quality assurance, evaluating an application/system's capabilities to meet the expected user demand. Without performance testing various defects can exist unknown threating to disrupt or even stop the application/system's operations. Thus, performance testing is integral for any application/system to succeed.

Cilium is ...

We seek to construct a test suite targeting various Cilium tuning parameters and evaulate the performance and capabilites of each parameter. To accomplish our goals, we utilize Terraform's resource-targeting mechanism allowing the freedom to enable or disable certain tuning parameters. Additionally, we aim to overcome two pitfalls observed from the current Cilium performance benchmark. [1] Firstly, pre-existing Cilium documentation of performance is outdated and no longer holds any value to the existing Cilium user base. We seek to rectify this by replicating Cilium's pre-existing performance test on the updated versions of Cilium. Secondly, Cilium's performance benchmark lacks scope as only 3 metrics are utilized in their testing. By expanding the tested metrics from 3 to 7, we can improve the usability and insight the performance banchmark provides. 

## Metrics Tested

Throughput
    Maximum transfer rate via a single TCP connection and the total transfer rate of 32 accumulated connections. [1]

Request/Response Rate
    The number of request/response messages per second that can be transmitted over a single TCP connection and over 32 parallel TCP connections. [1]

Connections Rate
    The number of connections per second that can be established in sequence with a single request/response payload message transmitted for each new connection. A single process and 32 parallel processes are tested. [1]

Latency
    Measurement of the delay of a packets's arrival to its destination from a single TCP connection.

CPU Utilization
    Percentage of the CPU's processing capacity used by a single TCP connection.

Memory Usage
    The required amount of RAM to faciliate a single TCP connection.

Network Jitter
    The variation of packet delay or latency over a single TCP connection.

## Tuning parameters
See https://docs.cilium.io/en/stable/operations/performance/tuning/ for the tuning parameters to change.
We will only be testing the following parameters:
BIG TCP
MTU
BBR Congestion Control for Pods
XDP Acceleration
eBPF Map Sizing
Hubble Obserbability
Bandwith Manager
Netkit Device Mode
Bypassing Iptables Tracking

<!-- ## Expected Results
BIG TCP
Improved throughput and latency
Increased CPU utilization (more CPU strain) 

MTU
Increased throughput
Increased Jitter and Data corruption / Packets Dropped
Increased CPU utilization

BBR Congestion Control for Pods
Increased bandwidth 
Improved latency
Increased CPU utilization

XDP Acceleration
Better latency and decrease in network jitter

eBPF Map Sizing
Better scaliabiklity
Increased Memory cost

Hubble Obserbability
Increased network performance
Decreased CPU strain

Bandwith Manager
Improved latency and throughput
Increased CPU strain

Netkit Device Mode
Significant latency reductions
Improved throughput

Bypassing Iptables Tracking
Improvements in latency and throughput
Decrease in network jitter -->

## Process


The goal is to be able to do this in a github action.
See for the proposed action
Though first we have to change the parameters through a script
See "SCRIPT" for the script

We will be using "Kernel" for all of our testing


Using bash, a script will run our Cilium infrastructure for varying intervals of times. This script will be ran for each tuning parameters and allows us to mimic usage of contianerized applications for short-term and long-term capabilities. Additionally, through the use of Prometheus and Grafana we can gather and visualize the network and CPU perfomance impact each tuning parameters has. We will then automate this testing process using github actions to test on a daily/weekly schedule. 

## Testing Environment

### Testing Hardware

### Testing Configuration


## Results
To Be Determined...

## Sources

[1] https://docs.cilium.io/en/stable/operations/performance/benchmark/