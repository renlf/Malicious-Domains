from cymru.ip2asn.dns import DNSClient as Client


def dict_build(filename):
    dns_dict = {}
    reader = open(filename, 'r')
    for line in reader:
        dn_ips = line[0:len(line)-1].split(' ')
        domain = dn_ips[0]
        ips = set(dn_ips[1:])
        dns_dict[domain] = ips
    reader.close()
    return dns_dict

def diff_build(ips_former, ips_backer):
    ips = ips_backer | ips_former
    if len(ips) > 200:
        return [0.0]*5
    print(len(ips))

    asn_former = []
    asn_backer = []
    bgp_former = []
    bgp_backer = []
    cc_former = []
    cc_backer = []
    lir_former = []
    lir_backer = []
    date_former = []
    date_backer = []
    for ip in ips:
        c = Client()
        r = c.lookup(ip, qType='IP')
        if ip in ips_former:
            asn_former.append(r.asn)
            bgp_former.append(r.prefix)
            cc_former.append(r.cc)
            lir_former.append(r.lir)
            date_former.append(r.date)

        if ip in ips_backer:
            asn_backer.append(r.asn)
            bgp_backer.append(r.prefix)
            cc_backer.append(r.cc)
            lir_backer.append(r.lir)
            date_backer.append(r.date)

    ip_count = float(len(ips))
    diff = []
    diff.append(len(set(asn_former) ^ set(asn_backer)))
    diff.append(len(set(bgp_former) ^ set(bgp_backer)))
    diff.append(len(set(cc_former)  ^ set(cc_backer)))
    diff.append(len(set(lir_former) ^ set(lir_backer)))
    diff.append(len(set(date_former) ^ set(date_backer)))
    return [x/ip_count for x in diff]

def change_rate(former, backer):
    change_dict = {}
    backer_dict = dict_build(backer)
    former_dict = dict_build(former)
    writer = open('md_result/md_change_rate2', 'w')
    for key, val in former_dict.items():
        if key in backer_dict:
            backer_val = backer_dict[key]
            d = val ^ backer_val
            if len(d) > 0:
                change_dict[key] = len(d)
                diff = diff_build(val, backer_val)
                print(diff)
                writer.write(key)
                writer.write(' ')
                for i, val in enumerate(diff):
                    writer.write(str(val))
                    if i < len(diff) - 1:
                        writer.write(' ')
                writer.write('\n')
    writer.close()


print(change_rate('md_result/md_2013-11-11-rdns.str','md_result/md_2013-09-21-rdns.str'))
