#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
Starting with 1 and spiralling anticlockwise in the following way, a square spiral with side length 7 is formed.

37 36 35 34 33 32 31
 38 17 16 15 14 13 30
 39 18  5  4  3 12 29
 40 19  6  1  2 11 28
 41 20  7  8  9 10 27
 42 21 22 23 24 25 26
43 44 45 46 47 48 49

It is interesting to note that the odd squares lie along the bottom right diagonal, but what is more interesting is that 8 out of the 13 numbers lying along both diagonals are prime; that is, a ratio of 8/13 ≈ 62%.

If one complete new layer is wrapped around the spiral above, a square spiral with side length 9 will be formed. If this process is continued, what is the side length of the square spiral for which the ratio of primes along both diagonals first falls below 10%?

observations:
- square spiral similar to 0028-Number_spiral_diagonals
- number in bottom-right corner is x**2, so not prime
'''

import time
import math
DEBUG = False

N=0.10

def isPrime(n):
    # we can igore 2 for this challenge
    if (n&1) == 0:
      return False
    for d in range(3,int(math.sqrt(n)+1),2):
      if (n%d) == 0:
        return False
    return True

def main():
    col = 1
    primes = 0
    total = 1
    br = 1
    while col < 10**8:
      idx = 2*col + 1      # square width
      br1 = br             # bottom right prev
      br = idx**2          # bottom right
      tl = (br1+br)>>1     # top left
      bl = (tl+br)>>1      # bottom left
      tr = (br1+tl)>>1     # top right
      corners3 = [tl,bl,tr]
      for n in corners3:
        if isPrime(n):
          primes = primes + 1
      total = total + 4
      d([col, primes, total,primes/float(total), corners3])
      if primes <= (N*total):
        print(['result',idx])
        return
      col = col + 1


def d(args):
    global DEBUG
    if DEBUG:
      print(args)

if  __name__ =='__main__':
  tStart = time.time()
  main()
  print(['time[ms]',int((time.time() - tStart)*1000)])

