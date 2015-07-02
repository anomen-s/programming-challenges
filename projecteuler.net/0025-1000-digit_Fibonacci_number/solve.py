#!/usr/bin/python

import gmpy2
import math

DIGITS = 1000

def fib():
  f1, f2 = 0, 1
  c = 1
  yield (1,f2)
  while True:
    t = f1 + f2
    f1 = f2
    f2 = t
    c = c + 1
    yield (c,t)
 
for (c,f) in fib():
  if f >= (10**(DIGITS-1)):
    print 'F(' + str(c) + ')'
    print(f)
    break
