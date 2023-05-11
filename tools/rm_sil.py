#!/usr/bin/env python3
import sys

with open(sys.argv[1], 'r', encoding="utf-8") as f:
    for line in f.readlines():
        line = line.rstrip()
        res = line.split()
        text = []
        key = res[0]
        for x in res[1:]:
            if x != 'sil':
                text.append(x)
        text = " ".join(text)
        print(key, text)
