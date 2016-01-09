import numpy
import math


def x_cdict(dname, str_dict,num):
    name_len = len(dname)
    i = 0
    while (i <= name_len - num):
        sub_str = dname[i:i+num]
        if str_dict.has_key(sub_str):
            str_dict[sub_str] += 1
        else:
            str_dict[sub_str] = 1
        i += 1

def xchar_feature(str_dict):
    str_clist = [v for v in str_dict.itervalues()]
    total = float(sum(str_clist))
    clist = [float(x) / total for x in str_clist]

    tmp_list = []
    tmp_list.append(numpy.median(clist))
    tmp_list.append(numpy.average(clist))
    tmp_list.append(numpy.std(clist))
    return tmp_list

def calcShannonEnt(dataSet):
    shannonEnt=0.0
    for prob in dataSet:
         shannonEnt-=prob*math.log(prob,2)
    return shannonEnt

def char_entropy(dataSet):
    tmp_list = []
    ent_list = []
    for dname in dataSet:
        char_dict = {}
        char_list = []
        for ch in dname:
            if char_dict.has_key(ch):
                char_dict[ch] += 1
            else:
                char_dict[ch] = 1
        for key in char_dict:
            char_list.append(float(char_dict[key]) / len(char_dict))

        ent_val = calcShannonEnt(char_list)
        ent_list.append(ent_val)

    tmp_list.append(numpy.average(ent_list))
    tmp_list.append(numpy.std(ent_list))
    return tmp_list


def structural(dataSet):
    tmp_list = []

    len_list = []
    level_list = []
    char_dict = {}
    TLD_dict = {}

    for name in dataSet:
        len_list.append(len(name))

        sub_names = name.split('.')
        level_list.append(len(sub_names))

        for ch in name:
            if not char_dict.has_key(ch):
                char_dict[ch] = 1

        if not TLD_dict.has_key(sub_names[-1]):
            TLD_dict[sub_names[-1]] = 1
        else:
            TLD_dict[sub_names[-1]] += 1

    #length
    tmp_list.append(numpy.average(len_list))
    tmp_list.append(numpy.median(len_list))
    tmp_list.append(numpy.std(len_list))
    tmp_list.append(numpy.var(len_list))
    #level
    tmp_list.append(numpy.average(level_list))
    tmp_list.append(numpy.median(level_list))
    tmp_list.append(numpy.std(level_list))
    tmp_list.append(numpy.var(level_list))
    #distinct characters
    tmp_list.append(len(char_dict))
    #TLD count
    tmp_list.append(len(TLD_dict))
    #TLD frequency
    domain_count = float(len(len_list))
    TLD_list = [v / domain_count for v in  TLD_dict.itervalues()]
    tmp_list.append(numpy.average(TLD_list))
    tmp_list.append(numpy.median(TLD_list))
    tmp_list.append(numpy.std(TLD_list))

    return tmp_list


def features_compute(data_file):
    features = []

    one_cdict = {}
    two_cdict = {}
    thr_cdict = {}
    for_cdict = {}

    top_LD = []
    sec_LD = []
    thd_LD = []

    domain_list = []

    reader = open(data_file, 'rb')
    for line in reader:
        domains = line.split('.')
        dname = domains[0]
        x_cdict(dname, one_cdict, 1)
        x_cdict(dname, two_cdict, 2)
        x_cdict(dname, thr_cdict, 3)
        x_cdict(dname, for_cdict, 4)

        count = len(domains)
        if count >= 1:
            top_LD.append(domain_list[count - 1])
        if count >= 2:
            sec_LD.append(domains[count - 2])
        if count >= 3:
            thd_LD.append(domains[count - 3])

        domain_list.append(line.split('\n')[0])

    reader.close()

    features.extend(xchar_feature(one_cdict))
    features.extend(xchar_feature(two_cdict))
    features.extend(xchar_feature(thr_cdict))
    features.extend(xchar_feature(for_cdict))
    features.extend(char_entropy(top_LD))
    features.extend(char_entropy(sec_LD))
    features.extend(char_entropy(thd_LD))
    features.extend(structural(domain_list))

    return features


print features_compute('dn')
