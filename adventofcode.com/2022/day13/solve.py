#!/usr/bin/env python3

"""
Compare and sort nested lists
"""
from itertools import chain
from functools import cmp_to_key
from math import prod


def read_pair(i):
    first_line = next(i)
    while not first_line.strip():
        first_line = next(i)
    return eval(first_line), eval(next(i))


def read_input(final):
    if final:
        fname = 'input'
    else:
        fname = f'input.sample'
    with open(fname, 'rt') as f:
        result = []
        try:
            while True:
                p = read_pair(f)
                result.append(p)
        except StopIteration:
            return result


def cmp(m1, m2):
    """
    Return
     >0 if m1 > m2 (wrong order)
     <0 if m1 < m2 (right order)
     0  if equal
    """
    if type(m1) == type(m2) == int:
        return m1 - m2

    if type(m1) == type(m2) == list:
        for m in range(min(len(m1), len(m2))):
            r = cmp(m1[m], m2[m])
            if r != 0:
                return r
        return len(m1) - len(m2)

    if type(m1) == int:
        return cmp([m1], m2)

    if type(m2) == int:
        return cmp(m1, [m2])

    raise Exception(f"Unexpected pair: {m1}, {m2}")


def solve(final):
    pairs = read_input(final)

    print(sum(i for i, r in ((i, cmp(*p)) for i, p in enumerate(pairs, 1)) if r <= 0))

    dividers = ([[2]], [[6]])
    msgs = sorted(chain((m for p in pairs for m in p), dividers), key=cmp_to_key(cmp))
    print(prod(i for i, m in enumerate(msgs, 1) if m in dividers))


if __name__ == '__main__':
    print("(expected: 13, 140)")
    solve(False)
    print('*' * 40)
    print("(expected: 6478, 21922)")
    solve(True)
