#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
It was proposed by Christian Goldbach that every odd composite number can be written as the sum of a prime and twice a square.

  9 = 7 + 2×1**2
 15 = 7 + 2×2**2
 21 = 3 + 2×3**2
 25 = 7 + 2×3**2
 27 = 19 + 2×2**2
 33 = 31 + 2×1**2

It turns out that the conjecture was false.

What is the smallest odd composite that cannot be written as the sum of a prime and twice a square?

'''

import math

DEBUG = True
def d(args):
    global DEBUG
    if DEBUG:
      print(args)


def squares2(n):
    res = []
    i = 1
    i2 = 1
    while i2 < n:
       i2 = 2*i*i
       res.append(i2)
       i = i + 1
    return res

def sieve(RANGE):
    primes = [True for x in range(RANGE)]
    # find primes
    for p in range(2, len(primes)//2+1):
      if primes[p]:
        i = p + p
        while i < RANGE:
          primes[i] = False
          i = i + p
    return primes


def main():
    RANGE=10**4
    print('* squares...')
    SQ = squares2(RANGE)
    print('* primes...')
    PRIMES = sieve(RANGE)
    
    print('* search...')
    for n in range(9, RANGE, 2):
      if not PRIMES[n]:
       #print(['check',n])
       found = False
       for sq in SQ:
         if sq >= n:
           break
         if PRIMES[n-sq]:
           found = True
       if not found:
         print(['result',n])
    

if  __name__ =='__main__':main()

