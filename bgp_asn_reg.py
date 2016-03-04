import socket
from cymru.ip2asn.dns import DNSClient as Client

def lookup():
    reader = open('md_ip_build', 'r')
    writer = open('md_bar.result', 'w')
    for line in reader:
        line = line[0:len(line)-1]
        dn_ips = line.split(' ')
        ips = dn_ips[1:len(dn_ips)]
        asn = []
        prefix = []
        cc = []
        lir = []
        date = []
        owner=[]
        for ip in ips:
            c = Client()
            result = c.lookup(ip, qType='IP')
            asn.append(result.asn)
            prefix.append(result.prefix)
            cc.append(result.cc)
            lir.append(result.lir)
            date.append(result.date)
        asn_num = set(asn)
        print(asn_num)
        for num in asn_num:
            if num == None:
                continue
            c = Client()
            if ' ' not in num:
                result = c.lookup(num[2:], qType='ASN')
                owner.append(result.owner)
            else:
                num = num[2:]
                nums = num.split(' ')
                print(nums)
                for n in nums:
                    result = c.lookup(n, qType='ASN')
                    owner.append(result.owner)

        writer.write(dn_ips[0])
        writer.write(' ')
        writer.write(str(len(set(asn))))
        writer.write(' ')
        writer.write(str(len(set(prefix))))
        writer.write(' ')
        writer.write(str(len(set(cc))))
        writer.write(' ')
        writer.write(str(len(set(lir))))
        writer.write(' ')
        writer.write(str(len(set(date))))
        writer.write(' ')
        writer.write(str(len(set(owner))))
        writer.write('\n')
    reader.close()
    writer.close()

lookup()
