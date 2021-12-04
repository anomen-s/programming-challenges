#!/usr/bin/env python3

'''
Compute final position of submarine. up/down is depth difference
'''

prev = None
hor = 0
vert = 0

with open('input', 'rt') as f:
    for rawline in f:
      l = rawline.split()
      d = l[0]
      v = int(l[1])
      # print(d, v)
      if d == "forward":
        hor += v
      elif d == "up":
        vert -= v
      elif d == "down":
        vert += v
      else:
        raise ValueError(rawline)

print(hor * vert)
