#!/usr/bin/env python3
import math

'''
Find local minimums in given heightmap.
'''

def read_input(final):
  if (final):
    fname = 'input'
  else:
    fname = 'input.sample'
  with open(fname, 'rt') as f:
    return [line.strip() for line in f]


def solve(final):
  hmap = read_input(final)
  w = len(hmap[0])
  h = len(hmap)
  total = 0
  bnum = 0
  bmap = [[(-2 if x == '9' else -1) for x in l] for l in hmap]
  for y in range(h):
    for x in range(w):
     is_low = True
     if x > 0 and hmap[y][x-1] <= hmap[y][x]:     is_low = False
     if x < (w-1) and hmap[y][x+1] <= hmap[y][x]: is_low = False
     if y > 0 and hmap[y-1][x] <= hmap[y][x]:     is_low = False
     if y < (h-1) and hmap[y+1][x] <= hmap[y][x]: is_low = False
     if is_low:
       total += 1 + int(hmap[y][x])
       bmap[y][x] = bnum
       bnum += 1

  print('Part1', total)
  #print(hmap)
  #print(bmap)

  while sum([1 for l in bmap for p in l if p == -1]) > 0:
    for y in range(h):
      for x in range(w):
       if bmap[y][x] == -1:
         if x > 0 and bmap[y][x-1] > -1:     bmap[y][x] = bmap[y][x-1]
         if x < (w-1) and bmap[y][x+1] > -1: bmap[y][x] = bmap[y][x+1]
         if y > 0 and bmap[y-1][x] > -1:     bmap[y][x] = bmap[y-1][x]
         if y < (h-1) and bmap[y+1][x] > -1: bmap[y][x] = bmap[y+1][x]

  basins = [0] * bnum
  for y in range(h):
    for x in range(w):
      v = bmap[y][x]
      if bmap[y][x] >= 0:
        basins[v] += 1
  basins.sort(reverse=True)
  print('Part2', math.prod(basins[:3]))

if __name__ == '__main__':
 solve(False)
 solve(True)
