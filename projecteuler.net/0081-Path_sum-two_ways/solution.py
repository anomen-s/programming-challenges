#!/usr/bin/python
# -*- coding: utf-8 -*-

def readfile(filename):
    f = open(filename)
    try:
       data = f.readlines()
    finally:
       f.close()
    return [map(int, x.split(',')) for x in data]


M = readfile('p081_matrix.txt')
DIM=len(M)

for y in xrange(DIM):
  for x in xrange(DIM):
    above = 2**30
    left = 2**30
    if x > 0:
      left = M[y][x-1]
    if y > 0:
      above = M[y-1][x]
    elif x == 0:
      above = 0 # [1:1]
    M[y][x] = M[y][x] + min(left,above)

print M[DIM-1][DIM-1]