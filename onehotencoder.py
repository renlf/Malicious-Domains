import string


char_array = [ch for ch in string.ascii_lowercase]
char_dict = {}


def one_hot_encoder():
    array_len = len(char_array)
    for idx, key in enumerate(char_array):
        onehot_array = [0] * array_len
        onehot_array[idx] = 1
        char_dict[key] = onehot_array
    return char_dict


def md_encode(filename):
    md_data = []
    reader = open(filename, 'rb')
    for line in reader:
        domains = line.split('.')
        d_name = domains[0]
        for ch in d_name:
            if char_dict.has_key(ch):
                md_data.append(char_dict[ch])
            else:
                md_data.append([0]*len(char_array))
        md_data.append([0]*len(char_array))
    md_data.pop()
    return md_data


print one_hot_encoder()
print md_encode('dn')
