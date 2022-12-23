#!/usr/bin/env python3

"""
Monkeys - nested expression evaluation
"""


def create_monkey(line):
    data = line.split()
    if len(data) < 2:
        raise Exception(f"Invalid data: {line}")
    name = data[0][:4]
    if data[1].isnumeric():
        return [name, int(data[1]), None]
    else:
        return [name, '@'] + data[1:]


def read_input(final):
    if final:
        fname = 'input'
    else:
        fname = 'input.sample'
    with open(fname, 'rt') as f:
        return {rec[:4]: create_monkey(rec) for rec in f}


ops = {
    '+': lambda x, y: x + y,
    '-': lambda x, y: x - y,
    '*': lambda x, y: x * y,
    '/': lambda x, y: x / y
}


def eval_monkey(monkeys, monkey_name):
    monkey = monkeys[monkey_name]
    if monkey[1] == '@':
        op1 = eval_monkey(monkeys, monkey[2])
        op2 = eval_monkey(monkeys, monkey[4])
        return ops[monkey[3]](op1, op2)
    else:
        return monkey[1]


def part2_test(monkeys, testval):
    monkeys['humn'][1] = testval
    monkey1 = monkeys['root'][2]
    monkey2 = monkeys['root'][4]
    m1rtest = eval_monkey(monkeys, monkey1)
    m2rtest = eval_monkey(monkeys, monkey2)
    test_diff = m2rtest - m1rtest
    print(f"for humn={testval} difference is {test_diff} ({m1rtest}, {m2rtest})")
    return test_diff


def solve(final, human_impact):
    monkeys = read_input(final)
    print(eval_monkey(monkeys, 'root'))

    print('-' * 30)

    # Part 2 - result will probably linearly depend on input,
    # so let's try binary search
    # human_impact was discovered empirically
    part2_test(monkeys, monkeys['humn'][1])

    print('-' * 10)

    result = 0
    for i in range(44, -1, -1):
        testval = result + 2 ** i
        test_diff = part2_test(monkeys, testval)
        if (human_impact * test_diff) < 0:
            result = testval

    print('-' * 10)

    for i in range(result - 5, result + 5):
        testval = i
        part2_test(monkeys, testval)


if __name__ == '__main__':
    print("(expected: 152, 301)")
    solve(False, -1)
    print('*' * 30)
    print("(expected: 78342931359552, 3296135418820)")
    solve(True, 1)
