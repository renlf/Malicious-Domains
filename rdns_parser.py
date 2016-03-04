from __future__ import unicode_literals
import csv

def domain_parser():
    reader = open('md_list', 'rb')

    md_domains = {}
    i = 0
    for line in reader:
        domains = line.split(b'\n')
        domain = domains[0]
        md_domains[domain] = []

    reader.close()

    reader= open("2013-09-21-rdns.csv", 'rb')
    for line in reader:
        dn_ip = line[0:len(line)-1].split(b',')
        if len(dn_ip) <= 1:
            continue
        ip = dn_ip[0]
        domain = dn_ip[1]
        if domain in md_domains:
            md_domains[domain].append(ip)
        prefix = domain[0:4]
        if prefix == 'www.':
            domain = domain[4:len(domain)]
            if domain in md_domains:
                md_domains[domain].append(ip)

    reader.close()

    writer = open('2013-09-21-rdns.out', 'w')
    for key, val in md_domains.items():
        if len(val) == 0:
            continue
        writer.write(str(key))
        for ip in val:
            print(ip)
            writer.write(' ')
            writer.write(str(ip))
        writer.write('\n')
    writer.close()

domain_parser()
