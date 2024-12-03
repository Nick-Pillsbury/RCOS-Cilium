package main

import (
	"log"
	"os"
	"os/signal"
	"syscall"

	"github.com/cilium/ebpf"
	"github.com/cilium/ebpf/link"
	"github.com/cilium/ebpf/rlimit"
)

const xdpProgPath = "~/ebpf-programs/c/abnormal_traffic.o"
const iface = "lo"

func main() {
	if err := rlimit.RemoveMemlock(); err != nil {
		log.Fatalf("Failed to remove memlock limit: %v", err)
	}

	spec, err := ebpf.LoadCollectionSpec(xdpProgPath)
	if err != nil {
		log.Fatalf("Failed to load eBPF program: %v", err)
	}

	coll := new(ebpf.Collection)
	if err := spec.LoadAndAssign(coll, nil); err != nil {
		log.Fatalf("Failed to load and assign eBPF program: %v", err)
	}
	defer coll.Close()

	xdpProg := coll.Programs["xdp_prog"]
	link, err := link.AttachXDP(link.XDPOptions{
		Program:   xdpProg,
		Interface: iface,
	})
	if err != nil {
		log.Fatalf("Failed to attach eBPF program: %v", err)
	}
	defer link.Close()

	log.Printf("eBPF program attached to interface %s", iface)

	sig := make(chan os.Signal, 1)
	signal.Notify(sig, syscall.SIGINT, syscall.SIGTERM)
	<-sig

	log.Println("Detaching eBPF program...")
}
