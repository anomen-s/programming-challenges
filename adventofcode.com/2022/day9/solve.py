#!/usr/bin/env python3

'''
Move using instructions
'''


def read_input(final, part):
    if final:
        fname = 'input'
    else:
        fname = f'input.sample{part}'
    with open(fname, 'rt') as f:
        return [(x, int(y)) for x, y in (line.split() for line in f)]


def move(start, stepdir):
    dirs = {'U': (0, -1), 'D': (0, 1), 'L': (-1, 0), 'R': (1, 0)}
    d = dirs[stepdir]
    return start[0] + d[0], start[1] + d[1]


def cmp(start, end):
    return (end > start) - (end < start)


def follow(knot, prev):
    return knot[0] + cmp(knot[0], prev[0]), knot[1] + cmp(knot[1], prev[1])


def process(knots, steps):
    p = [(0, 0) for _ in range(knots)]
    trail = set(p)
    for s in steps:
        for c in range(s[1]):
            p[0] = move(p[0], s[0])
            for k in range(1, knots):
                h = p[k - 1]
                t = p[k]
                if (h[0] == t[0]) or (h[1] == t[1]):
                    if (abs(sum(h) - sum(t))) > 1:
                        p[k] = follow(t, h)
                        if k == knots - 1:
                            trail.add(p[k])
                elif abs(h[0] - t[0]) > 1 or abs(h[1] - t[1]) > 1:
                    p[k] = follow(t, h)
                    if k == knots - 1:
                        trail.add(p[k])
    return trail


def solve(final):
    steps = read_input(final, 1)
    print(len(process(2, steps)))

    steps = read_input(final, 2)
    print(len(process(10, steps)))


if __name__ == '__main__':
    print("(expected: 13, 36)")
    solve(False)
    print('*' * 30)
    print("(expected: 6266, 2369)")
    solve(True)
