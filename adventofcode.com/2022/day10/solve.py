#!/usr/bin/env python3

"""
ALU Register
"""


def read_input(final):
    if final:
        fname = 'input'
    else:
        fname = f'input.sample'
    with open(fname, 'rt') as f:
        return [(x, int(y)) for x, y in (pad2(line.split()) for line in f)]


def pad2(row):
    if len(row) < 2:
        return row + [0]
    return row


def compute_pixel(buffer, cycle, reg):
    if abs(((cycle - 1) % 40) - reg) < 2:
        buffer.append('\u2588')
    else:
        buffer.append('\u25e6')


def process(steps, cycles):
    reg = 1
    buffer = []
    result = 0
    cycle = 1
    for s in steps:
        if cycle in cycles:
            result += cycle * reg
        if s[0] == 'noop':
            compute_pixel(buffer, cycle, reg)
            cycle += 1
        elif s[0] == 'addx':
            compute_pixel(buffer, cycle, reg)
            cycle += 1
            if cycle in cycles:
                result += cycle * reg
            compute_pixel(buffer, cycle, reg)
            cycle += 1
            reg += s[1]
        else:
            raise Exception(f'Invalid data: {s}')
    return result, buffer


def solve(final):
    steps = read_input(final)
    cycles = [20, 60, 100, 140, 180, 220]
    result, buffer = process(steps, cycles)
    print(result)
    for row in range(6):
        print(''.join(buffer[row * 40:row * 40 + 40]))


if __name__ == '__main__':
    print("(expected: 13140, x)")
    solve(False)
    print('*' * 40)
    print("(expected: 16880, RKAZAJBR)")
    solve(True)
