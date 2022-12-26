#!/usr/bin/env python3

"""
Sensors
"""
import re


def read_input(final):
    if final:
        fname = 'input'
    else:
        fname = 'input.sample'
    with open(fname, 'rt') as f:
        pattern = re.compile('^Sensor at x=(-?\\d+), y=(-?\\d+): closest beacon is at x=(-?\\d+), y=(-?\\d+)\\s*$')
        lines = (pattern.match(line) for line in f)
        return [tuple(int(rec[i]) for i in range(1, 5)) for rec in lines]


def distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


def intersect(sensor, y):
    radius = distance(*sensor)
    dx = radius - abs(sensor[1] - y)
    if dx >= 0:
        return sensor[0] - dx, sensor[0] + dx


def merge_ranges(ranges):
    prev = ranges[0]
    for curr in ranges[1:]:
        if curr[0] <= (prev[1] + 1):
            prev = (prev[0], max(prev[1], curr[1]))
        else:
            yield prev
            prev = curr
    yield prev


def count_with_beacons(r, beacons):
    b_count = sum(1 for b in beacons if r[0] <= b <= r[1])
    return r[1] - r[0] + 1 - b_count


def solve(final, row, rowlimit):
    data = read_input(final)

    # part 1
    ranges = sorted(r for r in set(intersect(d, row) for d in data) if r)
    merged = list(merge_ranges(ranges))
    beacons = sorted(set(d[2] for d in data if d[3] == row))
    final_sizes = [count_with_beacons(r, beacons) for r in merged]
    print(f"beacons = {beacons}")
    print(f"ranges  = {ranges} => {merged}")
    print(f"sizes   = {final_sizes} => {sum(final_sizes)}")

    # part 2
    for row in range(rowlimit):
        ranges = sorted(r for r in (intersect(d, row) for d in data) if r)
        merged = list(merge_ranges(ranges))
        if len(merged) > 1:
            print(f"{row}: {merged} => {row + (merged[0][1]+1)*4000000}")


if __name__ == '__main__':
    print("(expected:   26,  56000011)")
    solve(False, 10, 20)
    print('*' * 30)
    print("(expected: 4811413, 13171855019123)")
    solve(True, 2000000, 4000000)
