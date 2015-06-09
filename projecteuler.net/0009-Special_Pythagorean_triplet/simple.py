#!/usr/bin/python

#A Pythagorean triplet is a set of three natural numbers, a < b < c, for which,
#a2 + b2 = c2

#For example, 3^2 + 4^2 = 9 + 16 = 25 = 5^2.

#There exists exactly one Pythagorean triplet for which a + b + c = 1000.
#Find the product abc.


# c^2 = a^2 + b^2
# c   = 1000 - a - b
# (1000 - a - b) * (1000 - a - b) = a^2 + b^2

# M - Ka - Kb -Ka + a2 +ab -Kb +ab + b2 = a^2 + b^2
#  - Ka - Kb -Ka  +ab -Kb +ab  =  -M
#  Ka+Ka + Kb+Kb -ab -ab  =  M
# 2000*a + 2000*b - 2*a*b = 1000*1000
# b = (1000*1000 - 2000*a) / (2000 - 2*a)


import math;

SUM=1000

def ok(num):
  if num <= 0:
    return False
  if num >= 1000:
    return False
  if num != int(num):
    return False
  return True

for a in xrange(1, SUM):
 b = (SUM*SUM - 2*SUM*a) / (2.0*SUM - 2*a)
 c = SUM - a - b
 if ok(b) and ok(c):
   print a, b, c 
   print a**2, b**2, a**2+b**2, '=', c**2

   print a*b*c
   print '=========='
