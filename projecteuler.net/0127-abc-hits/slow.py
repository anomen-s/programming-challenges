#!/usr/bin/python3
# -*- coding: utf-8 -*-

import math
import gmpy2

DEBUG = True

N=120000
N=1000 # thirty-one abc-hits for c < 1000, with ∑c = 12523

def d(args):
    global DEBUG
    if DEBUG:
      print(args)

def gcd(a, b):
    return gmpy2.gcd(a,b)

def rad(fa, b, c):
    fset = fa | factors(b) | factors(c)
    r = 1
    for n in fset:
       r = r * n
    return r

def factors(N):
  f = set()
  i = 3
  while ((N % 2) == 0) and (N > 1):
      N = N / 2
      f.add(2)

  while N > 1:
    if (N % i) == 0:
      N = N / i
      f.add(i)
    else:
      i = i + 2
  return f


def xmain():
    return 0
    
def main():
    s = 0
    for a in range(1, N):
      fa = factors(a)
      for b in range(a+1, N-a+1):
        if gcd(a,b) > 1:
          continue
        c = a + b
        if gcd(a,c) > 1:
          continue
        if gcd(b,c) > 1:
          continue
        if rad(fa,b,c) < c:
          d('found %i,%i,%i' %(a,b,c))
          s = s + c
    print('sum %i' % s)

if  __name__ =='__main__':main()
