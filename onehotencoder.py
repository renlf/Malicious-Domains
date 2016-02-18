import string

def onehotencoder(char_array):
    array_len = len(char_array)
    char_dict = {}
    for idx, key in enumerate(char_array):
        onehot_array = [0] * array_len
        onehot_array[idx] = 1
        char_dict[key] = onehot_array
    return char_dict

char_array = [ch for ch in string.ascii_lowercase]
print onehotencoder(char_array)
