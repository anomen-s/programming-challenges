#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
The first two consecutive numbers to have two distinct prime factors are:

14 = 2 × 7
15 = 3 × 5

The first three consecutive numbers to have three distinct prime factors are:

644 = 2² × 7 × 23
645 = 3 × 5 × 43
646 = 2 × 17 × 19.

Find the first four consecutive integers to have four distinct prime factors. What is the first of these numbers?

Solution::
compute number of factors for each number

'''

import math

SEQ=2
SEQ=3
SEQ=4

DEBUG = False
def d(args):
    global DEBUG
    if DEBUG:
      print(args)


def factors(n):
  N = n
  ns = n//SEQ
  r = set()
  while  N % 2 == 0:
      N = N / 2
      r.add(2)
  i = 3
  while i <= N and (i < ns):
    if (N % i) == 0:
      N = N / i
      r.add(i)
    else:
      i = i + 2
#  if (N != 1):
#    r.clear() # there is factor >N/SEQ, we can ignore this number
  return r

def main():
    
    n = SEQ
    fl = [factors(x+1) for x in range(SEQ)]
    while True:
      fn = factors(n)
      fl.append(fn)
      d([n, fn])
      n = n + 1
      found = True

      for i in range(1, SEQ+1):
        prevf = fl[-i]
        #d(['test', prevf])
        if len(prevf) != SEQ:
          found = False
   
      if (len(fl) > 100):
        print(n)
        fl = fl[-SEQ:]
      if found:
        print (['found', n-SEQ,fl[-SEQ:]])
        exit()
      
          
if  __name__ =='__main__':main()

