#!/usr/bin/env python3

"""
Search sequence with different letters
"""


def read_input(final):
    if final:
        fname = 'input'
    else:
        fname = 'input.sample'
    with open(fname, 'rt') as f:
        return next(f)


def find(seq, num):
    for i in range(len(seq) - num):
        if len(set(seq[i:i + num])) == num:
            return i + num
    raise Exception("marker not found")


def solve(final):
    stream = read_input(final)
    print(find(stream, 4))
    print(find(stream, 14))


if __name__ == '__main__':
    print("(expected:   7,  19)")
    solve(False)
    print('*' * 30)
    print("(expected: 1155, 2789)")
    solve(True)
