#!/usr/bin/env python3

"""
Spread agents across board

Note: Part 2 took 2 hours on rpi4. Using lists instead of a set would probably help.
"""
import copy


def read_input(final):
    if final:
        fname = 'input'
    else:
        fname = 'input.sample'
    with open(fname, 'rt') as f:
        return [list(line.strip()) for line in f]


def create_elfs(board):
    elfs = set()
    for y in range(len(board)):
        for x in range(len(board[y])):
            if board[y][x] == '#':
                elfs.add((x, y))
    return elfs


DIRS = [
    # (x, y), adj. pos. 1, adj. pos. 2
    ((0, -1), (-1, -1), (1, -1)),
    ((0, 1), (-1, 1), (1, 1)),
    ((-1, 0), (-1, 1), (-1, -1)),
    ((1, 0), (1, 1), (1, -1))
]

NEIGHBOURS = ((-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0))


def move(pos, direction):
    return pos[0] + direction[0], pos[1] + direction[1]


def move_elf(elfs, elf, dirs):
    """
    Try to move elf.
    If no neighbour, don't move.
    Otherwise iterate possible four directions and go to the first one which is empty and both its neighbours are empty too.
    """
    other_elf = False
    for d in NEIGHBOURS:
        if move(elf, d) in elfs:
            other_elf = True
            break
    if not other_elf:
        return None
    for d in dirs:
        occup = sum(1 for place in d if move(elf, place) in elfs)
        if occup == 0:
            return move(elf, d[0])
    return None


def filter_collisions(elfs_new, collisions, moved):
    """
    Compute final elf positions.
    If new positioj in collisions, keep original position.
    """
    for new_pos in elfs_new:
        if new_pos in collisions:
            yield elfs_new[new_pos]
        else:
            if new_pos != elfs_new[new_pos]:
                moved.add(True)
            yield new_pos


def print_board(elfs):
    min_x = min(x for x, _ in elfs)
    max_x = max(x for x, _ in elfs)
    min_y = min(y for _, y in elfs)
    max_y = max(y for _, y in elfs)
    for y in range(min_y, max_y + 1):
        print(''.join('#' if (x, y) in elfs else '.' for x in range(min_x, max_x + 1)))
    print('=' * 20)


def solve(final):
    dirs = copy.copy(DIRS)
    board = read_input(final)
    elfs = create_elfs(board)
    collisions = set()

    for step in range(1, 10000):
        # print(f"Step {step}, collisions in prev. step: {len(collisions)}")
        # print_board(elfs)
        moved = set()
        collisions = set()
        elfs_new = dict()
        for elf in elfs:
            new_loc = move_elf(elfs, elf, dirs)
            # print(f"{elf} -> {new_loc}")
            if new_loc is None:
                elfs_new[elf] = elf
            elif new_loc in elfs_new:
                collisions.add(new_loc)
                elfs_new[elf] = elf
            else:
                elfs_new[new_loc] = elf
        elfs = list(filter_collisions(elfs_new, collisions, moved))
        dirs = dirs[1:] + [dirs[0]]

        if True not in moved:
            print(f"part 2: {step}")
            break

        if step == 10:
            min_x = min(x for x, _ in elfs)
            max_x = max(x for x, _ in elfs)
            min_y = min(y for _, y in elfs)
            max_y = max(y for _, y in elfs)

            part1 = (max_x - min_x + 1) * (max_y - min_y + 1) - len(elfs)
            print(f"part 1: {part1}")


if __name__ == '__main__':
    print("(expected: 110, 20)")
    solve(False)
    print('*' * 30)
    print("(expected: 4172, 942)")
    solve(True)
