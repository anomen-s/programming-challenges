#!/usr/bin/python
# -*- coding: utf-8 -*-
import gmpy2
import math

# using formulas from 
# https://en.wikipedia.org/wiki/Integer_triangle#Heronian_triangles
# and square check using gmpy2 library

# works for (n,n,n+1), not (n,n,n-1)
# cannot be used. because formula gives rational multiples
# exmples
#      found: 5,5,6
#  not found: 17,17,16

def isPerfectRoot(n):
    return gmpy2.is_square(n)

SUM = 0
#for n in xrange(3, 1000**3 / 3 + 1, 2):
for v in xrange(1, 13000):

  u2 = 3*v*v+1
  if isPerfectRoot(u2):
     v2 = v*v
     b = 2* (u2 - v2)
     a = u2 + v2
     if (a+a+a+1) > 1000**3:
       break
     print (a, '+1')
     SUM = SUM + a*3+1
     print ('sum', SUM)

  # this doesn't work, why?
  u2 = 3*v*v-1
  if isPerfectRoot(u2):
     v2 = v*v
     b = 2* (u2 - v2)
     a = u2 + v2
     print (a, '-1', a, b)
     SUM = SUM + a*3+1
     print ('sum', SUM)


print ('end',v)
print (SUM)
# sum for 1M = 716032
