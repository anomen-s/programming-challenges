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

Solution:
compute sieve with factors and then search it.
Upper bound must be guessed.
'''

import math

#SEQ=2
#SEQ=3
#SEQ=4
RANGE=10**6

DEBUG = False
def d(args):
    global DEBUG
    if DEBUG:
      print(args)


def sieve(RANGE):
    primes = [set() for x in range(RANGE)]
    # find primes
    for p in range(2, len(primes)//2+1):
      if len(primes[p]) == 0:
        i = p + p
        while i < RANGE:
          primes[i].add(p)
          i = i + p
    return primes


def main():
    P = sieve(RANGE)
    SEQ=2
    print('sieve finished')
    for i in range(SEQ, RANGE):
      found = True
      d([i, P[i]])
      for i2 in range(SEQ):
        d(['test %i'%(i-i2),P[i-i2],SEQ])
        if len(P[i-i2]) != SEQ:
          found = False
 
      if found:
        print (['found', i-SEQ+1,P[i-SEQ+1:i+1]])
        SEQ=SEQ+1
        #exit()

if  __name__ =='__main__':main()
