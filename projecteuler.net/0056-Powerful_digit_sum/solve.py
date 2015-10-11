#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
A googol (10**100) is a massive number: one followed by one-hundred zeros; 
100**100 is almost unimaginably large: one followed by two-hundred zeros. 
Despite their size, the sum of the digits in each number is only 1.

Considering natural numbers of the form, a**b, where a, b < 100, what is the maximum digital sum?
'''
import math
import time
DEBUG=True

RANGE=100



def SLOWdigitsum(n):
  r = 0
  while n > 0:
    r = r + (n%10)
    n = n // 10
  return r

def digitsum(n):
  return sum(map(int, str(n)));


def main():
    maxN = 0
    maxDs = 0
    for a in range(2,RANGE):
      d(a)
      n = 1
      for b in range(1,RANGE):
        n = n * a
        ds = digitsum(n)
        if ds > maxDs:
          maxDs = ds
          maxN = [n,a,b]
        
      
    print(['result', maxN, maxDs])


def d(args):
    global DEBUG
    if DEBUG:
      print(args)

if  __name__ =='__main__':
  tStart = time.time()
  main()
  print(['time[ms]',int((time.time() - tStart)*1000)])

