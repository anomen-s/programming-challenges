#!/usr/bin/env python3

"""
Base 5 numbers with -2 shift
"""


def read_input(final):
    if final:
        fname = 'input'
    else:
        fname = 'input.sample'
    with open(fname, 'rt') as f:
        return [line.strip() for line in f]


DIGITS = {'0': 0, '1': 1, '2': 2, '-': -1, '=': -2}


def toDec(number):
    res = 0
    for n in number:
        res = res * 5 + DIGITS[n]
    return res


SNAFU_DIGITS = {0: '0', 1: '1', 2: '2', 3: '=', 4: '-'}


def toSNAFU(number):
    n = number
    res = []
    while n != 0:
        n, digit = divmod(n, 5)
        res.append(SNAFU_DIGITS[digit])
        if digit >= 3:
            n += 1

    res.reverse()
    return ''.join(res)


def solve(final):
    masses = read_input(final)

    masses_int = [toDec(m) for m in masses]

    # print([toSNAFU(m) for m in masses_int])

    print(sum(masses_int))
    print(toSNAFU(sum(masses_int)))


if __name__ == '__main__':
    print("(expected: 4890/2=-1=0, x)")
    solve(False)
    print('*' * 30)
    print("(expected: 34168440432447/2-0-0=1-0=2====20=-2, x)")
    solve(True)
