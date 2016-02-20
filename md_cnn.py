import string
import csv
import numpy as np

char_array = [ch for ch in string.ascii_lowercase]
num_array = [str(x) for x in range(0, 10)]
op_array = ['-']
char_array = char_array + num_array + op_array

char_dict = {}
input_dim = 16


def alexa_parser(filename):
    writer = open('top', 'w+')
    csvf = open('top.csv', 'rb')
    reader = csv.reader(csvf)
    for line in reader:
        str = '0.' + line[1]
        writer.write(str + '\n')
    csvf.close()
    writer.close()


def one_hot_encoder():
    array_len = len(char_array)
    for idx, key in enumerate(char_array):
        onehot_array = [0] * array_len
        onehot_array[idx] = 1
        char_dict[key] = onehot_array
    return char_dict


def md_encode(filename):
    data = np.empty((500, 16, 37), dtype="float32")
    label = np.empty((500,), dtype="float32")

    reader = open(filename, 'rb')

    for i, line in enumerate(reader):
        domains = line.split('.')
        d_name = domains[1]
        d_labl = domains[0]
        md_data = []
        for ch in d_name:
            if char_dict.has_key(ch):
                md_data.append(char_dict[ch])
            else:
                md_data.append([0]*len(char_array))
            print ch
            print md_data

        dim_remain = input_dim - len(d_name)
        while dim_remain > 0:
            md_data.append([0] * len(char_array))
            dim_remain -= 1

        data[i,:,:] = md_data

        if d_labl == '1':
            label[i] = 1
        else:
            label[i] = 0

    return data, label


#alexa_parser('top.csv')
one_hot_encoder()
md_encode('dn_train')
