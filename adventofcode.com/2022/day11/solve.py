#!/usr/bin/env python3

"""
Simulate monkeys
"""
import copy
import math
import re


def read_monkey(input):
    first_line = next(input)
    while not first_line.strip():
        first_line = next(input)

    m = re.match('Monkey\\s+(\\d+):', first_line)
    r = dict(i=0, id=int(m[1]))

    m = re.match('\\s*Starting items:\\s+([0-9, ]+)$', next(input))
    r['items'] = [int(i) for i in m[1].split(',')]

    m = re.match('\\s*Operation: new = old\\s+([+*])\\s+(\\w+)$', next(input))
    r['op_op'] = m[1]
    r['op_val'] = m[2]
    if m[2].isnumeric():
        op = int(m[2])
        if m[1] == '+':
            r['op'] = lambda old: old + op
        elif m[1] == '*':
            r['op'] = lambda old: old * op
        else:
            raise Exception(f"Unexpected: {first_line}")
    else:
        if m[1] == '+':
            r['op'] = lambda old: old + old
        elif m[1] == '*':
            r['op'] = lambda old: old * old
        else:
            raise Exception(f"Unexpected: {first_line}")

    m = re.match('\\s*Test: divisible by\\s(\\d+)$', next(input))
    r['div_test'] = int(m[1])

    m = re.match('\\s*If true: throw to monkey\\s(\\d+)$', next(input))
    r['true'] = int(m[1])

    m = re.match('\\s*If false: throw to monkey\\s(\\d+)$', next(input))
    r['false'] = int(m[1])

    return r


def read_input(final):
    if final:
        fname = 'input'
    else:
        fname = f'input.sample'
    with open(fname, 'rt') as f:
        result = dict()
        try:
            while True:
                m = read_monkey(f)
                result[m['id']] = m
        except StopIteration:
            return result


def step(monkeys, m_id, part1, modulo):
    m = monkeys[m_id]
    for item in m['items']:
        m['i'] += 1
        wlevel = m['op'](item)
        if part1:
            wlevel = wlevel // 3
        else:
            wlevel = wlevel % modulo
        if (wlevel % m['div_test']) == 0:
            target = m['true']
        else:
            target = m['false']
        monkeys[target]['items'].append(wlevel)
    m['items'] = []


def solve(final):
    monkeys_src = read_input(final)

    # part 1
    monkeys = copy.deepcopy(monkeys_src)
    for _ in range(20):
        for m in monkeys:
            step(monkeys, m, True, 0)

    print(math.prod(sorted([m['i'] for m in monkeys.values()])[-2:]))

    # part 2
    monkeys = copy.deepcopy(monkeys_src)
    modulo = math.prod([m['div_test'] for m in monkeys.values()])

    for _ in range(10000):
        for m in monkeys:
            step(monkeys, m, False, modulo)

    print(math.prod(sorted([m['i'] for m in monkeys.values()])[-2:]))


if __name__ == '__main__':
    print("(expected: 10605, 2713310158)")
    solve(False)
    print('*' * 40)
    print("(expected: 50830, 14399640002)")
    solve(True)
