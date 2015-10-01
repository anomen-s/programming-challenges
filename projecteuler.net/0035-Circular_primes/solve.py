#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
The number, 197, is called a circular prime because all rotations of the digits: 197, 971, and 719, are themselves prime.

There are thirteen such primes below 100: 2, 3, 5, 7, 11, 13, 17, 31, 37, 71, 73, 79, and 97.

How many circular primes are there below one million?
'''

import math


def sieve(RANGE):
    primes = list(range(RANGE))
    primes[0] = 0
    primes[1] = 0
    # find primes
    for p in range(2, len(primes)//2+1):
      if primes[p]:
        i = p + p
        while i < RANGE:
          primes[i] = 0
          i = i + p
    return primes


validDigits = frozenset([1,3,7,9])

def rotations(n, order):
    isValid = True
    if n > 10:
      t = n
      while t > 0:
        if not ((t % 10) in validDigits):
          return
        t = t // 10
    #print(['rot',n,order])
    r = n
    while True:
      yield r
      r = (r + order * (r % 10))  // 10
      
      if r == n:
        return
    


def main():
    S = 0
    RANGE=10**6
    print("Build sieve")
    primes = sieve(RANGE)

    print("check primes")
    order=10
    for n in range(1,len(primes)):
      if n >= order:
         order = order * 10
      if primes[n]:
        isCyclical = True
        c = 0
        for rot in rotations(n, order):
          c = c + 1
          if not primes[rot]:
            isCyclical = False
          primes[rot] = 0
        if c>0 and isCyclical:
              print(list(rotations(n, order)))
              S=S+c

    print(['result',S])
    
    
if  __name__ =='__main__':main()
