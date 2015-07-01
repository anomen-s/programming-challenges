#!/usr/bin/python
# -*- coding: utf-8 -*-

import math

# using formula: area = base/2 * height

def isPerfectRoot(n):
    return (math.sqrt(n) % 1 == 0)

def isPerfectRoot1(n):
    m10 = n % 10
    if m10 ==  2 or m10 ==  3 or m10 == 7 or m10 == 8:
      return False
    return (math.sqrt(n) % 1 == 0)

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
