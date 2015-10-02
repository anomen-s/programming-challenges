#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
Take the number 192 and multiply it by each of 1, 2, and 3:
192 × 1 = 192
 192 × 2 = 384
 192 × 3 = 576

By concatenating each product we get the 1 to 9 pandigital, 192384576. We will call 192384576 the concatenated product of 192 and (1,2,3)

The same can be achieved by starting with 9 and multiplying by 1, 2, 3, 4, and 5, giving the pandigital, 918273645, which is the concatenated product of 9 and (1,2,3,4,5).

What is the largest 1 to 9 pandigital 9-digit number that can be formed as the concatenated product of an integer with (1,2, ... , n) where n > 1?

Observations
1 * (1,...,9)
n>2 => int < 10000
'''

import math


def check(n):
     digits = set(['0'])
     S=''
     r = n
     while len(digits) != 10:
       sr = str(r)
       S = S + sr
       for d in sr:
         if d in digits:
           return 0
         else:
           digits.add(d)
       r = r + n
     return S
       

def main():
    M = 0
    RANGE=10**5
    
    for n in range(1,RANGE):
      ns = int(check(n))
      M = max(M, ns)
      if ns > 0:
        print([n,ns])


    print(['result',M])
    
    
if  __name__ =='__main__':main()
