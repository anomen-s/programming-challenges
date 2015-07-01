#!/usr/bin/python
# -*- coding: utf-8 -*-
import gmpy2
import math

# using formula: area = base/2 * height
# and square check using gmpy2 library


def isPerfectRoot(n):
    return gmpy2.is_square(n)

SUM = 0
#for n in xrange(3, 1000**3 / 3 + 1, 2):
for n in xrange(3, 1000**3 / 3 + 1, 2):

#  if not isPerfectRoot(t0):
#    continue

#  if isPerfectRoot(areaN):
  if isPerfectRoot(n*n - (n*n-2*n+1)/4):
#     t0 = (n-1)*(n+1) >> 2
#     areaN = ((3*n - 1) * (n-1)*t0) >> 2#/ 16.0
     print (n, '-1')
     SUM = SUM + n*3-1
     print ('sum', SUM)
     
#  if isPerfectRoot(areaP):
  if isPerfectRoot(n*n - (n*n+2*n+1)/4):
#     t0 = (n-1)*(n+1) >> 2
#     areaP = ((3*n + 1) * (n+1)*t0) >> 2#/ 16.0
     print (n, '+1')
     SUM = SUM + n*3+1
     print ('sum', SUM)

print ('end',n)
print (SUM)
# sum for 1M = 716032
