#!/usr/bin/env python3

'''
1) Find two number which have sum 2020.
2) Find three number which have sum 2020.
'''

def read_input(final):
  if (final):
    fname = 'input'
  else:
    fname = 'input.sample'
  with open(fname, 'rt') as f:
    return [int(line.strip()) for line in f]


def solve(final):
  lines = read_input(final)
  values = set(lines)
  
  for v in lines:
    v2 = 2020-v
    if v2 in values:
      print('Part1', v*v2)
      break

  for v in lines:
    for v2 in lines:
      v3 = 2020-v-v2
      if v != v2 and v2 != v3 and v != v3 and v3 in values:
        print('Part2', v*v2*v3)
        return


if __name__ == '__main__':
 solve(False)
 print('*'*40)
 solve(True)
