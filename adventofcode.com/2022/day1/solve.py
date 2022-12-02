#!/usr/bin/env python3

'''
Find highest sum in array.
Find sum of 3 highest sums in array.
'''

def read_input(final):
  if (final):
    fname = 'input'
  else:
    fname = 'input.sample'
  with open(fname, 'rt') as f:
    i = 0
    r = []
    for l in f:
      ls = l.strip()
      if ls:
        i += int(ls)
      else:
        r.append(i)
        i = 0
    if i > 0:
      r.append(i)
    return r


def solve(final):
  vals = sorted(read_input(final), reverse=True)
  print(vals[0])
  print(sum(vals[:3]))

if __name__ == '__main__':
 print("(expected: 24000, 45000)")
 solve(False)
 print('*'*30)
 print("(expected: 74711, 209481)")
 solve(True)
