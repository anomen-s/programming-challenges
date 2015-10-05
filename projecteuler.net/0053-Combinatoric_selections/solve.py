#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
There are exactly ten ways of selecting three from five, 12345:

123, 124, 125, 134, 135, 145, 234, 235, 245, and 345

In combinatorics, we use the notation, 5C3 = 10.

In general,nCr = n! /(r!(n−r)!) ,where r ≤ n, n! = n×(n−1)×...×3×2×1, and 0! = 1.


It is not until n = 23, that a value exceeds one-million: 23C10 = 1144066.

How many, not necessarily distinct, values of  nCr, for 1 ≤ n ≤ 100, are greater than one-million?

observations:
* n >= r
* nCr = nC(n-r)
* nC(r+1) > nCr for r < n//2, so "for r" loop can stop when reaching c > MIN
* nC(r) = nC(r-1) * (n-r)/r, so no need to compute huge factorials
'''

import time
import math
DEBUG = True

N=100
MIN=10**6


F = [math.factorial(n) for n in range(N+1)]

def comb(n, r):
    return F[n] // (F[r] * F[n-r])

def main():
    S = 0

    for n in range(1,N+1):
      for r in range(1,(n+1)//2):
        c = comb(n, r)
        if c > MIN:
          d([n,r, c,'l'])
          d([n,n-r, c,'r'])
          S = S + 2
      if n % 2 == 0:
        c = comb(n, n//2)
        if c > MIN:
          d([n,n//2, c,'c'])
          S = S + 1

    print(['result', S])


def d(args):
    global DEBUG
    if DEBUG:
      print(args)

if  __name__ =='__main__':
  tStart = time.time()
  main()
  print(['time[ms]',int((time.time() - tStart)*1000)])

