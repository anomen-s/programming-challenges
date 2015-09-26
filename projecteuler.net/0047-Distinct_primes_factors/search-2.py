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
compute number of factors (use table of primes to check)
'''

import math

SEQ=2
SEQ=3
SEQ=4
PRIMERANGE=10**5

DEBUG = False
def d(args):
    global DEBUG
    if DEBUG:
      print(args)


def sieve(RANGE):
    primes = [True for x in range(RANGE)]
    primes[0] = False
    primes[1] = False
    # find primes
    for p in range(2, len(primes)//2+1):
      if primes[p]:
        i = p + p
        while i < RANGE:
          primes[i] = False
          i = i + p
    return primes


def primes():
    primeMask = sieve(PRIMERANGE)
    primes = []
    for n in range(PRIMERANGE):
      if primeMask[n]:
        primes.append(n)
    return primes

def factors(n, P):
  ns = n//SEQ
  r = 0
  
  for p in P:
    if p > ns:
      break
    if n % p == 0:
      r = r+1
  return r

def main():
    P = primes()
    n = SEQ
    fl = [factors(x+1,P) for x in range(SEQ)]
    while True:
      fn = factors(n, P)
      fl.append(fn)
      d([n, fn])
      n = n + 1
      found = True

      for i in range(1, SEQ+1):
        prevf = fl[-i]
        #d(['test', prevf])
        if prevf != SEQ:
          found = False
   
      if (len(fl) > 100):
        print(n)
        fl = fl[-SEQ:]
      if found:
        print (['found', n-SEQ,fl[-SEQ:]])
        exit()

if  __name__ =='__main__':main()
