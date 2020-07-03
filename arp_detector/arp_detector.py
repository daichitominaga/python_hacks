#!/usr/bin/env python

import scapy.all as scapy
from scapy.layers import http

def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answerd_list, _ = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)
    return answerd_list[0][1].hwsrc

def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=proess_sniffed_packet)


def proess_sniffed_packet(packet):
    if packet.haslayer(scapy.ARP) and packet[scapy.ARP].op == 2:
        try:
            real_mac = get_mac(packet[scapy.ARP].psrc)
            response_mac = packet[scapy.ARP].hwsrc

            if real_mac != response_mac:
                print("[+] You are under attack!!")
        except IndexError:
            pass


sniff("eth0")