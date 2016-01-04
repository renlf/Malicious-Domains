from collections import Counter

def char_seq(data_file, num, out_file):
    str_dict = {}
    f = open(data_file, 'rb')
    total = 0
    for line in f:
        domains = line.split('.')
        dname = domains[0]
        if dname == 'www':
            dname = domains[1]
        name_len = len(dname)
        i = 0
        while (i <= name_len - num):
            sub_str = dname[i:i+num]
            if str_dict.has_key(sub_str):
                str_dict[sub_str] += 1
            else:
                str_dict[sub_str] = 1
            total += 1
            i += 1
    f.close()

    writer = open(out_file, 'w+')
    for key in str_dict:
        writer.write(key + ' ' + str(str_dict[key]) + '\n')
    writer.close()

char_seq('dn', 1, 'seq')
