#!/usr/bin/env python3
import re

'''
Compute number of turned on lights
'''

SIZE = 1000

def read_input(final):
  if (final):
    fname = 'input'
  else:
    fname = 'input.sample'
  with open(fname, 'rt') as f:
    lines = [re.match('(.*) (\\d+),(\\d+) through (\\d+),(\\d+)', line.strip()) for line in f]
 
  return [[parsecmd(l[1]),int(l[2]),int(l[3]),int(l[4]),int(l[5])] for l in lines][::-1]

def parsecmd(val):
  if 'turn on' in val:
    return 1
  if 'turn off' in val:
    return 0
  if 'toggle' in val:
    return -1

  raise Exception('invalid command')


def solve(final):
  # read input and append command to set default state to OFF
  ins = read_input(final) + [[0, 0, 0, SIZE, SIZE]]
  # print(ins)
  cnt = 0

  for x in range(SIZE):
    for y in range(SIZE):

      swap = False
      for i in ins:
        if (i[1] <= x <= i[3]) and (i[2] <= y <= i[4]):
          if i[0] < 0:
            swap = not swap
          else:
            if i[0] ^ swap:
              cnt += 1
            break

  return cnt


if __name__ == '__main__':
 print('(expected %i)' % 998996)
 print(solve(False))
 print('*' * 30)
 print('(expected %i)' % 400410)
 print(solve(True))
