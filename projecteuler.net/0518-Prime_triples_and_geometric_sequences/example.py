#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
Let S(n) = a+b+c over all triples (a,b,c) such that:
a, b, and c are prime numbers.
a < b < c < n.
a+1, b+1, and c+1 form a geometric sequence.

For example, S(100) = 1035 with the following triples: 

(2, 5, 11), (2, 11, 47), (5, 11, 23), (5, 17, 53), (7, 11, 17), (7, 23, 71), (11, 23, 47), (17, 23, 31), (17, 41, 97), (31, 47, 71), (71, 83, 97)

Find S(10**8).
'''

import math


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


def main():
    S = 0
    RANGE=10**2
    print("Build sieve")
    primeMask = sieve(RANGE)

    print("collect primes")
    primes = []
    for n in range(RANGE):
      if primeMask[n]:
        primes.append(n)


    print('iterate %i primes' % len(primes))
    for ia in range(len(primes)-2):
#      print(ia)
      for ib in range(ia+1,len(primes)-1):
        a1 = primes[ia] + 1
        b1 = primes[ib] + 1
        b2 = b1*b1
        if b2 % a1 == 0:
         c = b2//a1 - 1
         if c >= RANGE:
           break
         if primeMask[c]:
           a = a1-1
           b = b1-1
           S = S + a+b+c
#           print ([a,b,c])
  
    print(S)
    
    
if  __name__ =='__main__':main()
