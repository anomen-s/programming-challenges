#!/usr/bin/env python3
import re

'''
Pathfinding in map with heights
'''


def read_input(final):
    if final:
        fname = 'input'
    else:
        fname = 'input.sample'
    with open(fname, 'rt') as f:
        return [list(line.strip()) for line in f]


def find_node(hills, mark, height):
    for y in range(len(hills)):
        for x in range(len(hills[0])):
            if hills[y][x] == mark:
                hills[y][x] = height
                return x, y
    raise Exception(f"Node not found: {mark}")


def process_node(hills, paths, queue, node, d):
    curr = (node[0] + d[0], node[1] + d[1])
    if not (0 <= curr[0] < len(hills[0]) and 0 <= curr[1] < len(hills)):
        # out of board
        return
    curr_l = paths[curr[1]][curr[0]]
    if curr_l >= 0:
        # already visited
        return
    curr_h = ord(hills[curr[1]][curr[0]])
    node_h = ord(hills[node[1]][node[0]])
    if node_h - curr_h > 1:
        # too steep
        return

    paths[curr[1]][curr[0]] = paths[node[1]][node[0]] + 1
    queue.append(curr)


def a_paths(hills, paths):
    for y in range(len(hills)):
        for x in range(len(hills[0])):
            if hills[y][x] == 'a' and paths[y][x] > 0:
                yield paths[y][x]


def solve(final):
    hills = read_input(final)
    # search from end (because of part2)
    end = find_node(hills, 'S', 'a')
    start = find_node(hills, 'E', 'z')
    paths = [[-1] * len(hills[0]) for _ in range(len(hills))]
    paths[start[1]][start[0]] = 0
    queue = [start]

    while len(queue) > 0:
        node = queue[0]
        queue = queue[1:]
        process_node(hills, paths, queue, node, (1, 0))
        process_node(hills, paths, queue, node, (-1, 0))
        process_node(hills, paths, queue, node, (0, -1))
        process_node(hills, paths, queue, node, (0, 1))

    print(paths[end[1]][end[0]])

    print(min(a_paths(hills, paths)))


if __name__ == '__main__':
    print("(expected:   31,  29)")
    solve(False)
    print('*' * 30)
    print("(expected: 520, 508)")
    solve(True)
