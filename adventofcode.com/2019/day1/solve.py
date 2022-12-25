#!/usr/bin/env python3

"""
Simple computation
"""


def read_input(final):
    if final:
        fname = 'input'
    else:
        fname = 'input.sample'
    with open(fname, 'rt') as f:
        return [int(line) for line in f]


def part1(m):
    return m // 3 - 2


def part2(m):
    total = 0
    curr = m
    while True:
        curr = part1(curr)
        if curr <= 0:
            return total
        total += curr


def solve(final):
    masses = read_input(final)

    print(sum(part1(m) for m in masses))
    print(sum(part2(m) for m in masses))


if __name__ == '__main__':
    print("(expected: 34241, 51316)")
    solve(False)
    print('*' * 30)
    print("(expected: 3481005, 5218616)")
    solve(True)
