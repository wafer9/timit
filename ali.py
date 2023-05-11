#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import glob
import sys
import numpy as np


def load_phone_map(file_):
    phones_map_60to39 = {}
    phones_map_48to39 = {}
    with open(file_, 'r') as f:
        for line in f.readlines():
            tmp = line.strip().split('  ')
            if len(tmp) == 3:
               phones_map_60to39[tmp[0]] = tmp[2]
               phones_map_48to39[tmp[1]] = tmp[2]
            if len(tmp) == 1:
               phones_map_60to39[tmp[0]] = ''
               phones_map_48to39[tmp[0]] = ''
    return phones_map_60to39, phones_map_48to39

def load_phones(file_):
    phones = {}
    with open(file_, 'r') as f:
        for line in f.readlines():
            tmp = line.strip().split()
            phones[int(tmp[1])] = tmp[0]
    return phones


if __name__ == '__main__':
    phones_map_ = sys.argv[1]
    phones_int_ = sys.argv[2]
    phones_map_60to39, phones_map_48to39 = load_phone_map(sys.argv[1])
    phones_int = load_phones(sys.argv[2])

    ali = {}
    left = False
    alignments = {}
    with open(sys.argv[3], 'r') as f:
        for line in f.readlines():
            alignment = []
            line = line.strip()
            key = line.split(maxsplit=1)[0]
            alis = line.split(maxsplit=1)[1].split('[')[1].split(']')[0].split(', ')
            alis = [int(x) for x in alis]
            prev, cur = 0, 0

            if left:
                for i in range(len(alis)):
                    cur = alis[i]
                    if (prev == 0 or prev != cur) and cur != 0:
                        alignment.append([phones_int[cur], i * 10])
                    prev = cur
            else:
                for i in range(len(alis)):
                    cur = alis[i]
                    if prev != 0 and (cur == 0 or cur != prev):
                        alignment.append([phones_int[prev], i * 10])
                    prev = cur
                if prev != 0:
                    alignment.append([prev, len(alis) * 10])
            alignments[key] = alignment
            

    label_alignments = {}
    timit_dir = glob.glob(sys.argv[4] + '/TEST/*/*/*.PHN')
    for file in timit_dir:
        key = "_".join(file.split('.')[0].split('/')[-2:])
        label_alignment = []
        with open(file, 'r') as f:
            for line in f.readlines():
                tmp = line.strip().split()
                phone = phones_map_60to39[tmp[2]]
                if phone != 'sil' and phone:
                    if left:
                        label_alignment.append([phone, int(tmp[0]) / 16.0])
                    else:
                        label_alignment.append([phone, int(tmp[1]) / 16.0])
        label_alignments[key] = label_alignment

    l_mean = []
    for key in alignments.keys():
        assert len(alignments[key]) == len(label_alignments[key])
        l = len(alignments[key])
        a1 = alignments[key]
        a2 = label_alignments[key]

        for i in range(l):
            if abs(a1[i][1] - a2[i][1]) < 2000:
                assert a1[i][0] == a2[i][0]
                l_mean.append(abs(a1[i][1] - a2[i][1]))
            # if key == 'FDHC0_SI1559':
            #     print(a1[i][0], a1[i][1], a2[i][1], a1[i][1] - a2[i][1])
            print(a1[i][1] - a2[i][1])
    
    l_mean.sort()
    l_mean_ = sum(l_mean) / len(l_mean)
    print("+" * 20, len(l_mean))
    print("left mean:%f " % l_mean_)
    print("left median:%f" % l_mean[int(len(l_mean)/2)])
    l_std = 0
    for i in range(len(l_mean)):
        l_std += (l_mean[i] - l_mean_)**2
    print("left std:%f" % (l_std/len(l_mean))**0.5)