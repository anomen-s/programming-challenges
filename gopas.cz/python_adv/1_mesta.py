#!/usr/bin/env python3


def nacti():
    result = {}
    with open('mesta.csv', 'rt') as f:
        for line in f:
            mesto = line.strip().split(',')
            cc = mesto[0]
            stat = result.setdefault(cc, [])
            stat.append(mesto)
            # print(line)
    return result


def serad(data):
    sdata = sorted(data, key=lambda x: int(x[2]))
    return map(lambda x: x[1], sdata)


def vypis(cc, data):
    # print(cc, end=': ')
    print(cc, ': ', ','.join(data), sep='')


def vypis_aspon_5(cc, data):
    m = [m for m in data if len(m) > 4]
    if len(m) > 0:
        print(cc, ': ', ', '.join(m), sep='')


mesta = nacti()

for cc in sorted(mesta):
    vypis(cc, serad(mesta[cc]))

print('-' * 20)
for cc in sorted(mesta):
    vypis_aspon_5(cc, serad(mesta[cc]))
