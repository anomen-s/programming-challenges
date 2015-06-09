#!/usr/bin/python

#The prime factors of 13195 are 5, 7, 13 and 29.

#What is the largest prime factor of the number 600851475143 ?

import math;

N=600851475143
#N=50
#N=65537
#N=6517514358

#TOP = int(math.sqrt(N))

while  N % 2 == 0:
      N = N / 2
      print 2, '->', N

i = 3
while i <= N:

    if (N % i) == 0:
      N = N / i
      print i, '->', N
    else:
      i = i + 2
