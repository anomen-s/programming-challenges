#!/usr/bin/env python3

"""
Falling sand.
"""
from collections import defaultdict

EMPTY = '.'


def split_line(line):
    return (tuple(int(i) for i in t.split(',')) for t in line.split('->'))


def read_input(final):
    if final:
        fname = 'input'
    else:
        fname = 'input.sample'
    with open(fname, 'rt') as f:
        return [split_line(line) for line in f]


def direction(start, end):
    if start > end:
        return -1
    elif start < end:
        return 1
    return 0


def move(point, d):
    return point[0] + d[0], point[1] + d[1]


def build_wall(wall, board):
    curr = next(wall)
    max_y = 0
    for point in wall:
        max_y = max(max_y, point[1])
        d = (direction(curr[0], point[0]), direction(curr[1], point[1]))
        while curr != point:
            board[curr] = '#'
            curr = move(curr, d)
        board[curr] = '#'
    return max_y


def print_board(board):
    min_x = min(x for x, _ in board)
    max_x = max(x for x, _ in board)
    max_y = max(y for _, y in board)
    for y in range(max_y + 1):
        row = ''.join(board[(x, y)] for x in range(min_x, max_x + 1))
        print(row)


def solve(final, floor):
    walls = read_input(final)
    board = defaultdict(lambda: EMPTY)
    max_y = max(build_wall(wall, board) for wall in walls) + 2
    if floor:
        for x in range(2 * max_y):
            # we should check min/max x to be correct
            board[(500 + x, max_y)] = '='
            board[(500 - x, max_y)] = '='

    r = 0
    while board[(500, 0)] == EMPTY:
        snowflake = (500, 0)
        while snowflake[1] <= max_y:
            down = move(snowflake, [0, 1])
            downleft = move(snowflake, [-1, 1])
            downright = move(snowflake, [1, 1])
            if board[down] == EMPTY:
                snowflake = down
            elif board[downleft] == EMPTY:
                snowflake = downleft
            elif board[downright] == EMPTY:
                snowflake = downright
            else:
                r += 1
                board[snowflake] = '*'
                break
        if snowflake[1] >= max_y:
            break
    # print_board(board)
    print(r)


if __name__ == '__main__':
    print("(expected: 24, 93)")
    solve(False, False)
    solve(False, True)
    print('*' * 40)
    print("(expected: 779, 27426)")
    solve(True, False)
    solve(True, True)
