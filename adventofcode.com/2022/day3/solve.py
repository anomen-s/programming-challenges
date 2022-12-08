#!/usr/bin/env python3
import re

'''
Search same items in backpacks.
'''


def read_input(final):
    if final:
        fname = 'input'
    else:
        fname = 'input.sample'
    with open(fname, 'rt') as f:
        return [list(line.strip()) for line in f]


def find1(line):
    c1 = set(line[:len(line) // 2])
    c2 = set(line[len(line) // 2:])
    return next(iter(c1 & c2))


def find2(packs):
    p = [set(i) for i in packs]
    return next(iter(p[0] & p[1] & p[2]))


def score(letter):
    if letter >= 'a':
        return ord(letter) - ord('a') + 1
    return ord(letter) - ord('A') + 27


def solve(final):
    packs = read_input(final)

    print(sum([score(find1(g)) for g in packs]))

    groups = [[packs[i], packs[i + 1], packs[i + 2]] for i in range(0, len(packs), 3)]
    print(sum([score(find2(g)) for g in groups]))


if __name__ == '__main__':
    print("(expected:   157,  70)")
    solve(False)
    print('*' * 30)
    print("(expected: 8493, 2552)")
    solve(True)
