#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
We shall say that an n-digit number is pandigital if it makes use of all the digits 1 to n exactly once. 
For example, 2143 is a 4-digit pandigital and is also prime.

What is the largest n-digit pandigital prime that exists?

Observations about result:
- odd number (prime >2)
- at least 4 digits (example)
- not 5,6,8,9 digits because sum of digits is divisible by 3 => number is also divisible by 3
'''

import math

def comb(digits, res):

      rem = digits[:]
      for d in digits:
        rem.remove(d)
        res.append(d)
        if len(rem) == 0:
          yield res
        else:
          for x in comb(rem,res):
           yield x
        res.pop()
        rem.append(d)

def oddCombinations(digits):
     for d in digits:
       if d % 2 != 0:
         rem = list(digits)
         rem.remove(d)
         for c in comb(rem, []):
           res = 0
           for rdigit in c:
             res = res * 10 + rdigit
           res = res * 10 + d
           yield res

def isPrime(oddN):
    # note: while p*p < oddN: p = p + 2 ..., is suprisingly slower
    for p in range(3, int(math.sqrt(oddN))+1, 2):
      if oddN%p == 0:
        return False
    return True

def main():
    M=0
    
    for Len in [4,7]:
      digits = range(1, Len+1)
      for number in oddCombinations(digits):
        if isPrime(number):
          #print(number)
          M = max(M, number)
      
    print(['max',M])
    
if  __name__ =='__main__': main()
