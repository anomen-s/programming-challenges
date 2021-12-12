#!/usr/bin/env python3
import math

'''
Count octopus flashes
'''

# octopus already flashed this round
FLASHED = int(1e9)

def read_input(final):
  if (final):
    fname = 'input'
  else:
    fname = 'input.sample'
  with open(fname, 'rt') as f:
    return [[int(n) for n in line.strip()] for line in f]

def checkflash(hmap, x, y):
  if hmap[y][x] > 9 and hmap[y][x] < FLASHED:
    flash(hmap, x, y)

def flash(hmap, x, y):
  hmap[y][x] += 1

  if hmap[y][x] > 9 and hmap[y][x] < FLASHED:
     hmap[y][x] += FLASHED
     w = len(hmap[0])
     h = len(hmap)
     if x > 0:
       flash(hmap, x-1, y) # W
       if y > 0:
         flash(hmap, x-1, y-1) # NW
       if y < (h-1):
         flash(hmap, x-1, y+1) # SW

     if x < (w-1):
       flash(hmap, x+1, y) # E
       if y > 0:
         flash(hmap, x+1, y-1) # NW
       if y < (h-1):
         flash(hmap, x+1, y+1) # SE

     if y > 0:
       flash(hmap, x, y-1) # N

     if y < (h-1):
       flash(hmap, x, y+1) # S


def solve(final, cnt1):
  hmap = read_input(final)
  w = len(hmap[0])
  h = len(hmap)
  total = 0

  for r in range(int(1e9)):
    # increase
    for y in range(h):
      for x in range(w):
        hmap[y][x] += 1

    # flash
    for y in range(h):
      for x in range(w):
        checkflash(hmap, x, y)

    # count & reset flashes
    flashes = 0
    for y in range(h):
      for x in range(w):
        if hmap[y][x] >= FLASHED:
          hmap[y][x] = 0
          total += 1
          flashes += 1

    if (flashes == w*h):
       print('Part2', r+1)
       return

    if ((r+1) == 10):
      print('Round(10)', total)

    if ((r+1) == cnt1):
      print('Round('+str(cnt1)+')', total)

if __name__ == '__main__':
 #solve(False, 10)
 solve(False, 100)

 solve(True, 100)
