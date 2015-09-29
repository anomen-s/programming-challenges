#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
The fraction 49/98 is a curious fraction, as an inexperienced mathematician in attempting to simplify it may incorrectly believe that 49/98 = 4/8, which is correct, is obtained by cancelling the 9s.

We shall consider fractions like, 30/50 = 3/5, to be trivial examples.

There are exactly four non-trivial examples of this type of fraction, less than one in value, and containing two digits in the numerator and denominator.

If the product of these four fractions is given in its lowest common terms, find the value of the denominator.
'''

import math

DEBUG = True
def d(args):
    global DEBUG
    if DEBUG:
      print(args)


def test(numer1, denom1, numer2, denom2, digit, res):

   if numer1 < 10 or denom1 < 10:
     return
   
   if numer1 >= denom1:
     return

   if (numer1*denom2) == (numer2*denom1):
     res.append([numer1, denom1, numer2, denom2,digit])

def gcd(a, b):
    while a != b:
        if a > b:
           a = a - b
        else:
           b = b - a
    return a

def main():
    res = []

    for numer in range(1,10):
      for denom in range(1,10):
        for digit in range(1,10):
         test(numer+10*digit, denom+10*digit, numer, denom, digit, res)
         test(10*numer+digit, denom+10*digit, numer, denom, digit, res)
         test(numer+10*digit, 10*denom+digit, numer, denom, digit, res)
         test(10*numer+digit, 10*denom+digit, numer, denom, digit, res)
    print(res)

    numer = 1
    denom = 1
    for [numer1, denom1, numer2, denom2,digit] in res:
       numer = numer * numer2
       denom = denom * denom2
    
    div = gcd(numer, denom)
    print([numer/div, '/', denom/div])
    

if  __name__ =='__main__':main()

