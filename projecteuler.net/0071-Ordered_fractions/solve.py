#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
Consider the fraction, n/d, where n and d are positive integers. If n<d and HCF(n,d)=1, it is called a reduced proper fraction.

If we list the set of reduced proper fractions for d ≤ 8 in ascending order of size, we get:

1/8, 1/7, 1/6, 1/5, 1/4, 2/7, 1/3, 3/8, 2/5, 3/7, 1/2, 4/7, 3/5, 5/8, 2/3, 5/7, 3/4, 4/5, 5/6, 6/7, 7/8

It can be seen that 2/5 is the fraction immediately to the left of 3/7.

By listing the set of reduced proper fractions for d ≤ 1,000,000 in ascending order of size, 
find the numerator of the fraction immediately to the left of 3/7.

Observations:
- in other words: find greates fraction smaller than 3/7.
- for each d1 compute n1 = int(3*d1/7))
'''

import time
import math
DEBUG = True


N=10**6
#N=5
#N=6
#N=10**3

FN=3
FD=7

ND=float(FN)/FD

def gcd(a, b):
    while b != 0:
        (a, b) = (b, a % b)
    return a

def main():
    maxV = 0
    maxF = None
    
    for d1 in range(3,N+1):
       n1 = int(float(FN*d1)/FD)
       f = float(n1) / d1
       #d([n1,d1,f])
       if (maxV < f < ND) and (gcd(n1,d1) == 1):
         d([n1,d1,f, 'new'])
         maxV = f
         maxF = [n1, d1]

    print([maxF, maxV])

def d(args):
    global DEBUG
    if DEBUG:
      print(args)

if  __name__ =='__main__':
  tStart = time.time()
  main()
  print(['time[ms]',int((time.time() - tStart)*1000)])

