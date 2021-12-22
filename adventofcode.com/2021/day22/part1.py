#!/usr/bin/env python3
import re

'''
3d power grid sequence
Part1: conut cubes powered up in range (x,y,z) in -50...50
'''

def read_input(inputfile):
  if (inputfile):
    fname = 'input.' + inputfile
  else:
    fname = 'input'
  with open(fname, 'rt') as f:
    return [parseCommand(line) for line in f]

def parseCommand(line):
  p = re.search('(o[nf]+)\\s+x=(-?\\d+)..(-?\\d+),y=(-?\\d+)..(-?\\d+),z=(-?\\d+)..(-?\\d+)', line)
  r = tuple([
      1 if p[1]=='on' else 0, # 0
      int(p[2]), # 1 = x min
      int(p[3]), # 2 = x max
      int(p[4]), # 3 = y min
      int(p[5]), # 4 = y max
      int(p[6]), # 5 = z min
      int(p[7])]) # 6 = z max
  assert r[1] <= r[2], "x: %i > %i" % (r[1], r[2])
  assert r[3] <= r[4], "y: %i > %i" % (r[3], r[4])
  assert r[5] <= r[6], "z: %i > %i" % (r[5], r[6])
  return r

def solve(inputfile):
  seq = read_input(inputfile)[::-1]
  # print(seq)

  total = 0
  for x in range(-50, 50+1):
   for y in range(-50, 50+1):
    for z in range(-50, 50+1):
      for step in seq:
        if (x >= step[1] and x <= step[2]) and (y >= step[3] and y <= step[4]) and (z >= step[5] and z <= step[6]):
          if step[0]:
            total += 1
            # print(x,y,z, sep=',')
          break
  print('Part1', inputfile, total)
      


if __name__ == '__main__':
 print("(expected:     39)", end=' ')
 solve('tiny')
 print("(expected: 590784)", end=' ')
 solve('sample')
 print("(expected: 474140)", end=' ')
 solve('part2')
 print('*' * 30)
 print("(solved:   545118)", end=' ')
 solve('')
