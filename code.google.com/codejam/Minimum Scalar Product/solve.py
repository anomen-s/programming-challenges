#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
You are given two vectors v1=(x1,x2,...,xn) and v2=(y1,y2,...,yn).
The scalar product of these vectors is a single number, calculated as x1y1+x2y2+...+xnyn. 

Suppose you are allowed to permute the coordinates of each vector as you wish.
Choose two permutations such that the scalar product of your two new vectors is the smallest possible, and output that minimum scalar product.
 
Sample:
<sample.txt>

Output:
Case #1: -25
Case #2: 6

Solution:
sort:
[Xmax, ..., 0, ..., Xmin]
[Ymin, ..., 0, ..., Ymax]

'''

import sys
import math


def main():
    if len(sys.argv) < 2:
      print("missing filename")
      exit(1)
    with open(sys.argv[1],'r') as f:
      lines = [x.strip() for x in f.readlines()]
    
    line = iter(lines)
    testcases = int(next(line))
    
    for t in range(1,testcases+1):
      dim = int(next(line))
      x = [int(i) for i in next(line).split()]
      y = [int(i) for i in next(line).split()]
      
      xs = sorted(x)
      ys = sorted(y)[::-1]
      res = sum([(xn*yn) for (xn,yn) in zip(xs,ys)])
      
      print('case #%i: %i' % (t, res))
     

if  __name__ =='__main__':
  main()


