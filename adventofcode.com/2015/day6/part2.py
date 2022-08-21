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
 
  return [[parsecmd(l[1]),int(l[2]),int(l[3]),int(l[4]),int(l[5])] for l in lines]

def parsecmd(val):
  if 'turn on' in val:
    return 1
  if 'turn off' in val:
    return -1
  if 'toggle' in val:
    return 2

  raise Exception('invalid command')


def solve(final):
  ins = read_input(final)
  
  lights = [[0 for y in range(SIZE)] for x in range(SIZE)]

  for i in ins:
    for x in range(i[1], i[3]+1):
      for y in range(i[2], i[4]+1):
        lights[x][y] = max(0, lights[x][y] + i[0]) 

  return sum([sum(l) for l in lights])
  


if __name__ == '__main__':
 print('(expected %i)' % -1)
 print(solve(False))
 print('*' * 30)
 print('(expected %i)' % 15343601)
 print(solve(True))
