#!/usr/bin/env python3

"""
Map walk with movable obstacles (blizzards).
"""

EMPTY = '.'


def read_input(final):
    if final:
        fname = 'input'
    else:
        fname = 'input.sample'
    with open(fname, 'rt') as f:
        return [list(line.strip()) for line in f]


def move(pos, direction):
    return pos[0] + direction[0], pos[1] + direction[1]


def print_board(board):
    for row in board:
        print(''.join(row))


def create_blizzards(board):
    result = []
    for y in range(len(board)):
        for x in range(len(board[0])):
            if board[y][x] == 'v':
                result.append((x, y, (0, 1)))
            elif board[y][x] == '^':
                result.append((x, y, (0, -1)))
            elif board[y][x] == '<':
                result.append((x, y, (-1, 0)))
            elif board[y][x] == '>':
                result.append((x, y, (1, 0)))
    return result


def move_blizzards(bliz, w, h):
    result = []
    for b in bliz:
        pos = move(b, b[2])
        if pos[0] == 0:
            result.append((w - 2, pos[1], b[2]))
        elif pos[0] == w - 1:
            result.append((1, pos[1], b[2]))
        elif pos[1] == 0:
            result.append((pos[0], h - 2, b[2]))
        elif pos[1] == h - 1:
            result.append((pos[0], 1, b[2]))
        else:
            result.append((pos[0], pos[1], b[2]))
    return result


def draw_board(bliz, pos_start, pos_end, w, h):
    board = [[EMPTY] * w for _ in range(h)]
    board[0] = ['#'] * w
    board[-1] = ['#'] * w
    for y in range(h):
        board[y][0] = '#'
        board[y][w - 1] = '#'
    board[pos_start[1]][pos_start[0]] = EMPTY
    board[pos_end[1]][pos_end[0]] = EMPTY

    for b in bliz:
        board[b[1]][b[0]] = '@'
    return board


MOVES = (
    (0, 0),
    (1, 0),
    (0, 1),
    (-1, 0),
    (0, -1)
)


def valid_moves(p, board):
    w = len(board[0])
    h = len(board)
    for m in MOVES:
        new_p = move(p, m)
        if 0 <= new_p[0] < w and 0 <= new_p[1] < h and board[new_p[1]][new_p[0]] == EMPTY:
            yield new_p


def solve(final, size):
    start_board = read_input(final)
    w = len(start_board[0])
    h = len(start_board)
    pos_start = (start_board[0].index(EMPTY), 0)
    pos_end = (start_board[-1].index(EMPTY), h - 1)
    bliz = create_blizzards(start_board)
    reachable = {pos_start}
    step = 0

    while pos_end not in reachable:
        bliz = move_blizzards(bliz, w, h)
        board = draw_board(bliz, pos_start, pos_end, w, h)
        reachable = set(np for p in reachable for np in valid_moves(p, board))
        step += 1

    print(step)

    # part 2
    reachable = {pos_end}
    while pos_start not in reachable:
        bliz = move_blizzards(bliz, w, h)
        board = draw_board(bliz, pos_start, pos_end, w, h)
        reachable = set(np for p in reachable for np in valid_moves(p, board))
        step += 1

    # print(step)

    reachable = {pos_start}
    while pos_end not in reachable:
        bliz = move_blizzards(bliz, w, h)
        board = draw_board(bliz, pos_start, pos_end, w, h)
        reachable = set(np for p in reachable for np in valid_moves(p, board))
        step += 1

    print(step)


if __name__ == '__main__':
    print("(expected: 18, 54)")
    solve(False, 4)
    print('*' * 30)
    print("(expected: 240, 717)")
    solve(True, 50)
