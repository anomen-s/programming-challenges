#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
The decimal number, 585 = 1001001001 (binary), is palindromic in both bases.

Find the sum of all numbers, less than one million, which are palindromic in base 10 and base 2.

(Please note that the palindromic number, in either base, may not include leading zeros.)


observations:
- even numbers are not palindomic in base 2

'''

import math

DEBUG = True
def d(args):
    global DEBUG
    if DEBUG:
      print(args)

RANGE=10**6

def isPalind10(n):
   p = 0
   t = n
   while t > 0:
     p = (p * 10) + (t % 10)
     t = t // 10
   return n == p

def isPalind2(n):
   p = 0
   t = n
   while t > 0:
     p = (p << 1) | (t & 1)
     t = t >> 1
   return n == p
    

def main():
    res = 0
    for number in range(1,RANGE, 2):
      if isPalind10(number) and isPalind2(number):
          print(number)
          res = res + number
    print(['result',res])

    

if  __name__ =='__main__':main()

