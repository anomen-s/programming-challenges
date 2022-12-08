#!/usr/bin/env python3

"""
Search subranges.
"""
import re


def read_input(final):
    if final:
        fname = 'input'
    else:
        fname = 'input.sample'
    with open(fname, 'rt') as f:
        lines = (re.match('(\\d+)-(\\d+),(\\d+)-(\\d+)', line) for line in f)
        return [(int(rec[1]), int(rec[2]), int(rec[3]), int(rec[4])) for rec in lines]


def check_pair(p):
    if (p[0] >= p[2]) and (p[1] <= p[3]):
        #  first range is inside the second
        return 1
    if (p[2] >= p[0]) and (p[3] <= p[1]):
        # second range is inside the first
        return 1
    return 0


def overlap(p):
    s = max(p[0], p[2])
    e = min(p[1], p[3])
    if s <= e:
        return 1
    return 0


def solve(final):
    pairs = read_input(final)

    print(sum([check_pair(p) for p in pairs]))
    print(sum([overlap(p) for p in pairs]))


if __name__ == '__main__':
    print("(expected:   2,  4)")
    solve(False)
    print('*' * 30)
    print("(expected: 532, 854)")
    solve(True)
