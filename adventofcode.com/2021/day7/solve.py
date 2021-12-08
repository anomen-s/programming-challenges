#!/usr/bin/env python3

'''
Find final position which is closest to all given starting position.
Part1: linear fuel consumption
Part2: linear increase of fuel consumption by distance (i.e.: 1, 3, 6, ...)
'''

def read_input(final):
  if (final):
    fname = 'input'
  else:
    fname = 'input.sample'
  with open(fname, 'rt') as f:
    return [int(n) for line in f for n in line.strip().split(',')]

def movecost1(a, b):
 return abs(a - b);

def movecost2(a, b):
 n = abs(a - b)
 return n * (n+1) // 2

def solve(final, move_cost_fn):
  init = read_input(final)
  min_cost = None
  for f in range(min(init), max(init) + 1):
     cost = sum([move_cost_fn(f, i) for i in init])
     if min_cost == None or min_cost[1] > cost:
       min_cost = (f, cost)
  print(min_cost)


if __name__ == '__main__':
 solve(False, movecost1)
 solve(True, movecost1)
 solve(False, movecost2)
 solve(True, movecost2)
