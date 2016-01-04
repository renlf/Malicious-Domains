#!/usr/bin/env python

import dpkt
import socket
import sys
import os

def dns_parser(pcap_path):
    files = os.listdir(pcap_path)
    writer = open('dn','w+')
    for name in files:
        filename = os.path.join(pcap_path, name)
        f = open(filename, 'rb')
        pcap = dpkt.pcap.Reader(f)

        name_dict = {}

        for ts, buf in pcap:
            # make sure we are dealing with IP traffic
            try: eth = dpkt.ethernet.Ethernet(buf)
            except:
                continue
            if eth.type != 2048:
                continue

            # make sure we are dealing with UDP
            try: ip = eth.data
            except:
                continue
            if ip.p != 17:
                continue

            # filter on UDP assigned ports for DNS
            try: udp = ip.data
            except:
                continue
            if udp.sport != 53 and udp.dport != 53:
                continue

            # make the dns object out of the udp data and check for it being a RR (answer)
            try: dns = dpkt.dns.DNS(udp.data)
            except: continue

            if len(dns.qd) < 1:
                continue
            for query in dns.qd:
                dname = str(query.name)
                if (not name_dict.has_key(dname)) and ('localdomain' not in dname):
                    name_dict[dname] = 1
                    writer.write(dname + '\n')
        f.close()
    writer.close()

pcap_path = 'D:\DNS\DNS_Parser\DNSPCAP'
dns_parser(pcap_path)
