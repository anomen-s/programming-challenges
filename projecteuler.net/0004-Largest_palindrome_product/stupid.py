#!/usr/bin/python
# -*- coding: utf-8 -*-



#A palindromic number reads the same both ways. The largest palindrome made from the product of two 2-digit numbers is 9009 = 91 × 99.

#Find the largest palindrome made from the product of two 3-digit numbers.

import math;

M=0

i1=999
while i1 > 99:
  
  i2 = i1
  
  while i2 > 99:
    N = i1 * i2
    if N > 100000 and (str(N)[::-1] == str(N)):
      print N, '=', i1, '*', i2
      if (N > M):
        M = N
    i2 = i2 - 1

  i1 = i1 - 1

print 'max: ', M
