#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
It is possible to show that the square root of two can be expressed as an infinite continued fraction.

√ 2 = 1 + 1/(2 + 1/(2 + 1/(2 + ... ))) = 1.414213...

By expanding this for the first four iterations, we get:

1 + 1/2 = 3/2 = 1.5
 1 + 1/(2 + 1/2) = 7/5 = 1.4
 1 + 1/(2 + 1/(2 + 1/2)) = 17/12 = 1.41666...
 1 + 1/(2 + 1/(2 + 1/(2 + 1/2))) = 41/29 = 1.41379...

The next three expansions are 99/70, 239/169, and 577/408, but the eighth expansion, 1393/985, 
is the first example where the number of digits in the numerator exceeds the number of digits in the denominator.

In the first one-thousand expansions, how many fractions contain a numerator with more digits than denominator?

observations:
a[n] = 1 + 1 / (1 + a[n-1])
a0 = 1

a[n-1] = frn / frd
fr[n] =  (frn + 2 * frd) / (frd + frn)

gcd(frn, frd) -- not necessary, how to prove it?
'''
import time
import math
DEBUG = True

N=1000

def gcd(a, b):
    while b != 0:
        (a, b) = (b, a % b)
    return a

def main():
    S = 0
    frn = 1
    frd = 1
    n0 = 0
    for n in range(N):
      (frn, frd) = (frn+frd*2, frd+frn)
      
      g = gcd (frn, frd)
      if g > 1:
        d(['reduce fraction %i / %i' % (frn,frd)])
        frn = frn // g
        frd = frd // g
      if len(str(frn)) > len(str(frd)):
        S = S + 1 
        d([n,n-n0,frn, frd])
        n0 = n
    print(['result', S])

def d(args):
    global DEBUG
    if DEBUG:
      print(args)

if  __name__ =='__main__':
  tStart = time.time()
  main()
  print(['time[ms]',int((time.time() - tStart)*1000)])

