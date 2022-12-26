#!/usr/bin/env python3

"""
Tetris.

data:
board[y][x]

|..@@@@.| y=3
|.......| y=2
|.......| y=1
|.......| y=0
+-------+ (floor)
 0123456   =x
"""
import hashlib

EMPTY = '.'


def read_input(final):
    if final:
        fname = 'input'
    else:
        fname = 'input.sample'
    with open(fname, 'rt') as f:
        return tuple(next(f).strip())


SHAPES = (
    ((0, 0), (1, 0), (2, 0), (3, 0)),
    ((1, 0), (0, -1), (1, -1), (2, -1), (1, -2)),
    ((2, 0), (2, -1), (0, -2), (1, -2), (2, -2)),
    ((0, 0), (0, -1), (0, -2), (0, -3)),
    ((0, 0), (1, 0), (0, -1), (1, -1))
)


def extend_board(board, height):
    if len(board) < (height + 10):
        board.extend([[EMPTY] * 7 for _ in range(100)])

    for y in range(height + 9, -1, -1):
        if '@' in board[y]:
            return y + 1

    return height


def sum(point1, point2, point3=(0, 0)):
    return point1[0] + point2[0] + point3[0], point1[1] + point2[1] + point3[1]


def try_move(board, shape, pos, direction):
    for piece in shape:
        new_pos = sum(piece, pos, direction)
        if new_pos[0] < 0 or new_pos[0] > 6:
            return None
        if new_pos[1] < 0:
            return None
        if board[new_pos[1]][new_pos[0]] != EMPTY:
            return None

    return sum(pos, direction)


def place_shape(board, shape, pos):
    for piece in shape:
        piece_pos = sum(piece, pos)
        board[piece_pos[1]][piece_pos[0]] = '@'


def print_board(board, height):
    for y in range(height, -1, -1):
        print('|' + ''.join(board[y]) + '|')
    print('-' * 9)


def array_to_byte(row):
    r = 0
    for i in row:
        r = (r * 2 + int(i != EMPTY))
    return r


def dump_state(board, height, shape, jet_move):
    ROWS = 40
    if height <= ROWS:
        return None

    m = hashlib.sha1()
    m.update(bytes((shape, jet_move >> 8, jet_move & 0xFF)))

    b = bytes(array_to_byte(board[y]) for y in range(height - ROWS, height))
    m.update(b)
    return m.digest()


def solve(final, rocks, hashing=False):
    jet_moves = read_input(final)
    # print(jet_moves)
    height = 0
    board = []
    rock = 0
    jet_move = 0
    states = dict()
    while rock < rocks:
        height = extend_board(board, height)
        # print_board(board, height)
        shape_id = rock % len(SHAPES)
        shape = SHAPES[shape_id]
        shape_h = -min(y for _, y in shape)
        pos = (2, height + shape_h + 3)

        if hashing:
            state = dump_state(board, height, shape_id, jet_move % len(jet_moves))
            if rock in (85, 2755) and state in states:
                print(f"rock {rock}, height {height} is eq to state/height {states[state]}, hash: {state}")
            states[state] = (rock, height)

        while True:
            move = (1, 0) if jet_moves[jet_move % len(jet_moves)] == '>' else (-1, 0)
            jet_move += 1
            new_pos = try_move(board, shape, pos, move)
            if new_pos:
                pos = new_pos

            new_pos = try_move(board, shape, pos, (0, -1))
            if new_pos:
                pos = new_pos
            else:
                place_shape(board, shape, pos)
                break

        rock += 1
    if not hashing:
        print(extend_board(board, height))


if __name__ == '__main__':
    print("(expected: 3068, 1514285714288)")
    solve(False, 2022)
    solve(False, 86, True)
    print("""
     rock 50 (h: 78) == rock 85 (50+35) (h: 131)
     delta height = 53
     131 + 28571428569 * 53 == 1514285714288
    """)
    print('*' * 30)
    print("(expected: 3193, 1577650429835)")
    solve(True, 2022)
    solve(True, 2756, True)
    print("""
    rock 1010 (h: 1629) == rock 2755 (1010+1745) (h: 4382)
    delta height = 2753
    4382 + 573065901 * 2753 == 1577650429835
    """)
