#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
The number, 1406357289, is a 0 to 9 pandigital number because it is made up of each of the digits 0 to 9 in some order, 
but it also has a rather interesting sub-string divisibility property.

Let d1 be the 1st digit, d2 be the 2nd digit, and so on. In this way, we note the following:
d2d3d4=406 is divisible by 2
d3d4d5=063 is divisible by 3
d4d5d6=635 is divisible by 5
d5d6d7=357 is divisible by 7
d6d7d8=572 is divisible by 11
d7d8d9=728 is divisible by 13
d8d9d10=289 is divisible by 17

 Find the sum of all 0 to 9 pandigital numbers with this property.
'''
import math;


def compute_mul_table(n):
     result = {}
     i = n
     while i < 1000:
       if i >= 10:
         result.setdefault(i % 100, []).append(i // 100)
       i = i + n
     return result

def use(l, idx, comb):
      l[idx] = comb[0]
      l[idx+1] = comb[1]
      l[idx+2] = comb[2]
      return True


def comb(l, idx):
     if not DT[idx]:
       yield l
       return
     clower = 10*l[idx+1]+l[idx+2]
     if clower in DT[idx]:
       for v in DT[idx][clower]:
         use(l, idx, [v, l[idx+1], l[idx+2]])
         for x in comb(l, idx-1):
           yield x


def isPandigital(n):
     digits = set(n[1:])
     if len(digits) != 9:
       return False
     lastDigitSet = DIGITS - digits
     ld = list(lastDigitSet)[0]
     
     n[0] = ld
     return True

DT = [None] + [compute_mul_table(x) for x in [2,3,5,7,11,13,17]]
DIGITS = frozenset(range(10))

def main():
    S = 0
    num = [0 for x in range(10)]
    for c in DT[7]:
      use(num, 7, [DT[7][c][0],c//10,c%10]); 
      for c in comb(num, 7):
        if isPandigital(c):
          print(c)
          S = S + int(''.join(map(str,c)))
      
    print(['result', S])


if  __name__ =='__main__':main()
    