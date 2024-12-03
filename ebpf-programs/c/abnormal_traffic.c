#include <linux/bpf.h>
#include <linux/if_ether.h>
#include <linux/ip.h>
#include <linux/udp.h>
#include <linux/tcp.h>
#include <linux/ptrace.h>
#include <linux/skbuff.h>
#include <bpf_helpers.h>

struct bpf_map_def SEC("maps") anomalies = {
    .type = BPF_MAP_TYPE_PERF_EVENT_ARRAY,
    .key_size = sizeof(__u32),
    .value_size = sizeof(__u32),
    .max_entries = 1024,
};

SEC("xdp_prog")
int detect_anomalies(struct xdp_md *ctx) {
    void *data = (void *)(long)ctx->data;
    void *data_end = (void *)(long)ctx->data_end;

    struct ethhdr *eth = data;
    if ((void *)(eth + 1) > data_end)
        return XDP_PASS;

    if (eth->h_proto != htons(ETH_P_IP))
        return XDP_PASS;

    struct iphdr *iph = data + sizeof(*eth);
    if ((void *)(iph + 1) > data_end)
        return XDP_PASS;

    // Detect fragmented packets
    if (iph->frag_off & htons(IP_MF)) {
        __u32 key = 0;
        bpf_perf_event_output(ctx, &anomalies, BPF_F_CURRENT_CPU, &key, sizeof(key));
        return XDP_DROP; // Drop the packet
    }

    return XDP_PASS;
}

char _license[] SEC("license") = "GPL";
