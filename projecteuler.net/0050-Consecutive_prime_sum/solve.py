#!/usr/bin/python3
# -*- coding: utf-8 -*-


#The prime 41, can be written as the sum of six consecutive primes:
#41 = 2 + 3 + 5 + 7 + 11 + 13
#
#This is the longest sum of consecutive primes that adds to a prime below one-hundred.
#
#The longest sum of consecutive primes below one-thousand that adds to a prime, contains 21 terms, and is equal to 953.
#
#Which prime, below one-million, can be written as the sum of the most consecutive primes?

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
    maxSum = 0
    maxCount = 0
    maxStart = 0
    RANGE=10**6
    primeMask = sieve(RANGE)
    primes = []
    for n in range(RANGE):
      if primeMask[n]:
        primes.append(n)

    for n in range(len(primes)):
       c = 0
       s = 0
       while s < RANGE and (n+c) < len(primes):
         s = s + primes[n + c]
         c = c + 1
         if s < RANGE and primeMask[s] and (c > maxCount):
             maxCount = c
             maxSum = s
             maxStart = n
    print(maxSum, maxCount, maxStart)
    
if  __name__ =='__main__':main()
