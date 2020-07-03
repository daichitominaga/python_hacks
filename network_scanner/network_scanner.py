#!/usr/bin/env python

import optparse
import scapy.all as scapy


def get_argments():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target", dest="target", help="Target IP / IP range.")
    (options, argments) = parser.parse_args()    
    if  not options.target:
        parser.error('[-] Please specity an target, use --help for more info.')
    return options

def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answerd_list, _ = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)

    client_list = []
    for element in answerd_list:
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        client_list.append(client_dict)
    return client_list

def print_result(result_list):
        print("IP\t\t\tMAC Address\n---------------------------------")
        for client in result_list:
            print(client["ip"] + "\t\t" + client["mac"])

options = get_argments()
scan_result = scan(options.target)
print_result(scan_result)