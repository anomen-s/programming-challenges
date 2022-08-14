#!/usr/bin/env python3

'''
Elevator (up/down)
'''

def read_input(final):
  if (final):
    fname = 'input'
  else:
    fname = 'input.sample'
  with open(fname, 'rt') as f:
    c = [line.strip() for line in f]
    return c[0]


def solve(final):
  r = read_input(final)
  return r.count('(') - r.count(')')


if __name__ == '__main__':
 print("(expected: -3)")
 print(solve(False))
 print('*'*30)
 print("(expected: 280)")
 print(solve(True))
