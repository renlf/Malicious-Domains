from __future__ import unicode_literals
import socket
from cymru.ip2asn.dns import DNSClient as Client

#ip = socket.gethostbyname("www.google.com")
#c = Client()
#print(ip)
#print(c.lookup(ip, qType='IP'))

def domain_parser():
    reader = open('md_list', 'rb')

    md_domains = {}
    i = 0
    for line in reader:
        domains = line.split(b'\n')
        domain = domains[0]
        md_domains[domain] = []
        try:
            ip = socket.gethostbyname(domain)
            md_domains[domain].append(ip)
        except socket.gaierror:
            md_domains[domain] = []

        print(i)
        i+=1
    reader.close()

    print("finish getting ip")

    reader = open('main_118212410.txt', 'rb')
    for line in reader:
        dn_ip = line.split(b',')
        domain = dn_ip[0]
        ip = (dn_ip[1]).split(b'\n')[0]
        if domain in md_domains:
            md_domains[domain].append(ip)
    reader.close()

    reader = open('sub_73633663.txt', 'rb')
    for line in reader:
        dn_ip = line.split(b',')
        domain = dn_ip[0]
        ip = (dn_ip[1]).split(b'\n')[0]
        if domain in md_domains:
            md_domains[domain].append(ip)
    reader.close()

    writer = open('md_ip_result', 'wb')
    for key, val in md_domains.items():
        writer.write(key)
        for ip in val:
            writer.write(b' ')
            writer.write(ip)
        writer.write(b'\n')
    writer.close()


domain_parser()
