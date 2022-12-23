#!/usr/bin/env python3

"""
Map walk
"""


def parse_trail(trail):
    buffer = ''
    for c in trail:
        if c in 'LR':
            yield int(buffer)
            yield c
            buffer = ''
        else:
            buffer += c
    if buffer:
        yield int(buffer)


def expand(board):
    w = max(len(row) for row in board)
    for row in board:
        if len(row) < w:
            yield row + ('/' * (w - len(row)))
        else:
            yield row


def read_input(final):
    if final:
        fname = 'input'
    else:
        fname = 'input.sample'
    with open(fname, 'rt') as f:
        content = [line.replace(' ', '/').strip() for line in f]
        return tuple(expand(content[:-2])), tuple(parse_trail(content[-1]))


DIRS = (
    (1, 0),
    (0, 1),
    (-1, 0),
    (0, -1)
)


def sum(pos, direction, dim):
    return (pos[0] + direction[0] + dim[0]) % dim[0], (pos[1] + direction[1] + dim[1]) % dim[1], direction


def score(pos):
    return 4 * (pos[0] + 1) + 1000 * (pos[1] + 1) + DIRS.index(pos[2])


def move1(board, pos):
    w = len(board[0])
    h = len(board)
    next_pos = sum(pos, pos[2], (w, h))
    while board[next_pos[1]][next_pos[0]] == '/':
        next_pos = sum(next_pos, next_pos[2], (w, h))
    if board[next_pos[1]][next_pos[0]] == '#':
        return pos
    return next_pos


# def move2(board, pos):
#     w = len(board[0])
#     h = len(board)
#     next_pos = sum(pos, pos[2], (w, h))
#     while board[next_pos[1]][next_pos[0]] == '/':
#         next_pos = sum(next_pos, next_pos[2], (w, h))
#     if board[next_pos[1]][next_pos[0]] == '#':
#         return pos
#     return next_pos


def walk(board, trail, pos, fmove, size):
    for m in trail:
        if m == 'L':
            pos = (pos[0], pos[1], DIRS[(DIRS.index(pos[2]) - 1 + len(DIRS)) % len(DIRS)])
        elif m == 'R':
            pos = (pos[0], pos[1], DIRS[(DIRS.index(pos[2]) + 1 + len(DIRS)) % len(DIRS)])
        else:
            for _ in range(m):
                pos = fmove(board, pos)
    return pos


def solve(final, size):
    board, trail = read_input(final)
    pos = (board[0].index('.'), 0, DIRS[0])

    print(score(walk(board, trail, pos, move1, size)))
    # print(score(walk(board, trail, pos, move2, size)))


if __name__ == '__main__':
    print("(expected: 6032, 5031)")
    solve(False, 4)
    print('*' * 30)
    print("(expected: 30552, x)")
    solve(True, 50)
