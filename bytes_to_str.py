def bytes2str(filename):
    reader = open(filename, 'rb')
    writer = open('wh_out.str', 'wb')
    for line in reader:
        dn_ips = line.split(b' ')
        for i, val in enumerate(dn_ips):

            if i < len(dn_ips) - 1:
                writer.write(val[2:len(val)-1])
                writer.write(b' ')
            if i == len(dn_ips) - 1:
                writer.write(val[2:len(val)-2])

        writer.write(b'\n')
    reader.close()
    writer.close()

bytes2str('wh_one.bytes')
