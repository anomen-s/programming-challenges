#!/usr/bin/env python3

"""
Move boxes.
"""
import copy


def read_input(final):
    if final:
        fname = 'input'
    else:
        fname = 'input.sample'
    with open(fname, 'rt') as f:
        schema = []
        cmds = []
        for line in f:
            if '[' in line:
                tokens = line[1::4]
                while len(tokens) > len(schema):
                    schema.append([])
                for i, t in enumerate(tokens):
                    if t.isalpha():
                        schema[i].insert(0, t)
            elif 'move' in line:
                cmds.append([int(x) for x in line.split()[1::2]])

        return schema, cmds


def process(src_schema, cmds, at_once):
    schema = copy.deepcopy(src_schema)
    for cmd in cmds:
        moved = schema[cmd[1] - 1][-cmd[0]:]
        schema[cmd[1] - 1] = schema[cmd[1] - 1][:-cmd[0]]
        if not at_once:
            moved.reverse()
        schema[cmd[2] - 1].extend(moved)
    return schema


def solve(final):
    schema, cmds = read_input(final)

    print(''.join([s[-1] for s in process(schema, cmds, False)]))
    print(''.join([s[-1] for s in process(schema, cmds, True)]))


if __name__ == '__main__':
    print("(expected: CMZ, MCD)")
    solve(False)
    print('*' * 30)
    print("(expected: ZWHVFWQWW, HZFZCCWWV)")
    solve(True)
