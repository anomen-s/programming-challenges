#!/usr/bin/env python3
import re

'''
Compute firing trajectory
'''

def read_input(final):
  if (final):
    fname = 'input'
  else:
    fname = 'input.sample'
  with open(fname, 'rt') as f:
    content = [c.strip() for c in f]
    d = [re.findall('-?\\d+', line) for line in content]
    return tuple(map(int, d[0]))

def solve(final):
  (x0, x1, y0, y1) = read_input(final)
  print('target', x0,x1,y0,y1)
  result = (-1e9,0)
  for x in range(1, x1):
    if x*x+x >= 2*x0:
      for y in range(y0, 410):
         steps = []
         hit = None
         maxy = -1e9
         dx, dy, px, py = x, y, 0, 0
         while (dx > 0 or px >=x0) and px <= x1 and py >= y0:
           px, py = px+dx, py+dy
           steps.append((px,py))
           maxy = max(maxy, py)
           dx = max(0, dx-1)
           dy -= 1
           if (px >= x0 and px <= x1) and (py >= y0 and py <= y1):
              result = max(result, (maxy, x, y))
              hit = (maxy, px,py)
         #print([x,y], hit, steps)
  print('Part1(max_y, x, y)', result)


if __name__ == '__main__':
 solve(False)
 print('*' * 30)
 solve(True)
