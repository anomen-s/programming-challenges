#!/usr/bin/python
# -*- coding: utf-8 -*-
import gmpy2
import math

# using formulas from 
# http://www.had2know.com/academics/nearly-equilateral-heronian-triangles.html

# P: n,n,n+1: V(n+3) = 15V(n+2) - 15V(n+1) + V(n).
# N: n,n+1,n+1: W(n+3) = 15W(n+2) - 15W(n+1) + W(n).

def isPerfectRoot(n):
    return gmpy2.is_square(n)

SUM = 0
S = [5, 65, 901]

while True:
  prev = S[-3:]
  V = 15* prev[2] - 15*prev[1] + prev[0]
  if V > (1000**3 / 3):
#    print 'break'
    break
  S.append(V)
#  print (V)

SUM = SUM + reduce(lambda x,y: x+3*y+1, S, 0)
print ('n,n,n+1',S)
print SUM

print '----------'

S = [17-1, 241-1, 3361-1]

while True:
  prev = S[-3:]
  V = 15* prev[2] - 15*prev[1] + prev[0]
  if V > (1000**3 / 3):
#    print 'break'
    break
  S.append(V)
#  print (V)
  

SUM = SUM + reduce(lambda x,y: x+3*y+3-1, S, 0)
print ('n+1,n+1,n',S)
print (SUM)
# sum for 1M = 716032
