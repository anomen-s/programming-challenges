#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
The arithmetic sequence, 1487, 4817, 8147, in which each of the terms increases by 3330, is unusual in two ways:
(i) each of the three terms are prime, and,
(ii) each of the 4-digit numbers are permutations of one another.

There are no arithmetic sequences made up of three 1-, 2-, or 3-digit primes, exhibiting this property, but there is one other 4-digit increasing sequence.

What 12-digit number do you form by concatenating the three terms in this sequence?

'''
import time

RANGE=10000

def sieve(r):
    primes = list(range(r))
    primes[0] = 0
    primes[1] = 0
    # find primes
    for p in range(2, len(primes)//2+1):
      if primes[p]:
        i = p + p
        while i < r:
          primes[i] = 0
          i = i + p
    return primes


def isPerm(n0, n1, n2):
  dn0 = [d for d in str(n0)]
  dn0.sort()
  dn1 = [d for d in str(n1)]
  dn1.sort()
  dn2 = [d for d in str(n2)]
  dn2.sort()
  return dn0 == dn1 == dn2
  
def search(n0, primes):

  maxD = (RANGE - n0) // 2
  for d in range(1,maxD):
    if not primes[n0]:
      continue
    n1 = n0 + d
    n2 = n1 + d
    if (primes[n1] and primes[n2] and isPerm(n0, n1,n2)):
      print(str(n0) + str(n1) + str(n2) + ' d=' + str(d))
    


def main():
    primes = sieve(RANGE)
    print('primes computed.')
    for i in range(RANGE):
      search(i, primes)
    
if  __name__ =='__main__':
  tStart = time.time()
  main()
  print(['time[ms]',int((time.time() - tStart)*1000)])
