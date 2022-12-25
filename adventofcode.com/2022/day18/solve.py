#!/usr/bin/env python3

"""
Compute surface area
"""

NEIGHBOURS = (
    (0, 0, 1),
    (0, 0, -1),
    (0, 1, 0),
    (0, -1, 0),
    (1, 0, 0),
    (-1, 0, 0))

BLOCK = 'BLOCK'
INT = 'INT'
EXT = 'EXT'


def read_input(final):
    if final:
        fname = 'input'
    else:
        fname = f'input.sample'
    with open(fname, 'rt') as f:
        return set((int(x), int(y), int(z)) for x, y, z in (line.split(',') for line in f))


def move(pos, direction):
    return pos[0] + direction[0], pos[1] + direction[1], pos[2] + direction[2]


def scan(blocks, internal, external, block, visited):
    if block in blocks:
        return BLOCK
    if block in internal:
        return INT
    if block in external:
        return EXT

    visited.add(block)

    for n in NEIGHBOURS:
        npos = move(block, n)
        if npos not in visited:
            ntype = scan(blocks, internal, external, npos, visited)
            if ntype == EXT:
                external.add(block)
                return ntype
            if ntype == INT:
                internal.add(block)
                return ntype

    return BLOCK


def inspect(blocks, internal, external, block, direction):
    adj = move(block, direction)
    if adj in blocks:
        return BLOCK
    if adj in internal:
        return INT
    if adj in external:
        return EXT

    res = scan(blocks, internal, external, adj, set())
    if res == BLOCK:
        internal.add(adj)
    return inspect(blocks, internal, external, block, direction)


def exterior_blocks(blocks):
    x_range = min(x for x, _, _ in blocks) - 1, max(x for x, _, _ in blocks) + 1
    y_range = min(y for _, y, _ in blocks) - 1, max(y for _, y, _ in blocks) + 1
    z_range = min(z for _, _, z in blocks) - 1, max(z for _, _, z in blocks) + 1

    exterior = set()
    for x in range(x_range[0], x_range[1] + 1):
        for y in range(y_range[0], y_range[1] + 1):
            exterior.add((x, y, z_range[0]))
            exterior.add((x, y, z_range[1]))
    for y in range(y_range[0], y_range[1] + 1):
        for z in range(z_range[0], z_range[1] + 1):
            exterior.add((x_range[0], y, z))
            exterior.add((x_range[0], y, z))
    for z in range(z_range[0], z_range[1] + 1):
        for x in range(x_range[0], x_range[1] + 1):
            exterior.add((x, y_range[0], z))
            exterior.add((x, y_range[1], z))

    return exterior


def solve(final):
    blocks = read_input(final)
    exterior = exterior_blocks(blocks)
    interior = set()
    c_exterior = 0
    c_interior = 0
    for block in blocks:
        for face in NEIGHBOURS:
            nstate = inspect(blocks, interior, exterior, block, face)
            if nstate == INT:
                c_interior += 1
            if nstate == EXT:
                c_exterior += 1

    print(c_exterior + c_interior)
    print(c_exterior)


if __name__ == '__main__':
    print("(expected: 64, 58)")
    solve(False)
    print('*' * 30)
    print("(expected: 4608, 2652)")
    solve(True)
