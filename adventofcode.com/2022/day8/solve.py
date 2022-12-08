#!/usr/bin/env python3

"""
2D array search
"""
import math


def read_input(final):
    if final:
        fname = 'input'
    else:
        fname = 'input.sample'
    with open(fname, 'rt') as f:
        return [[int(c) for c in line.strip()] for line in f]


def visibility(field):
    w = len(field[0])
    h = len(field)
    result = [[0] * w for i in range(h)]
    visibility_scan(field, result, [1, 0], [[0, y] for y in range(h)])
    visibility_scan(field, result, [-1, 0], [[w - 1, y] for y in range(h)])
    visibility_scan(field, result, [0, 1], [[x, 0] for x in range(w)])
    visibility_scan(field, result, [0, -1], [[x, h - 1] for x in range(w)])
    return result


def visibility_scan(field, res, dir, start_points):
    for s in start_points:
        last = -1
        pos = s
        while (0 <= pos[0] < len(field[0])) and (0 <= pos[1] < len(field)):
            tree = field[pos[1]][pos[0]]
            if tree > last:
                res[pos[1]][pos[0]] = 1
                last = tree
            pos[0] += dir[0]
            pos[1] += dir[1]


def scenic_score(field):
    w = len(field[0])
    h = len(field)
    r = 0
    for x in range(w):
        for y in range(h):
            sc = math.prod(scan_dir(field, x, y, dx, dy) for dx, dy in [[0, 1], [0, -1], [1, 0], [-1, 0]])
            r = max(r, sc)
    return r


def scan_dir(field, x0, y0, dx, dy):
    t = field[y0][x0]
    w = len(field[0])
    h = len(field)
    i = 0
    x1 = x0 + dx
    y1 = y0 + dy
    while (0 <= x1 < w) and (0 <= y1 < h):
        i += 1
        if field[y1][x1] >= t:
            break
        x1 += dx
        y1 += dy
    return i


def solve(final):
    field = read_input(final)
    print(sum(sum(row) for row in visibility(field)))
    print(scenic_score(field))


if __name__ == '__main__':
    print("(expected: 21, 8)")
    solve(False)
    print('*' * 30)
    print("(expected: 1647, 392080)")
    solve(True)
