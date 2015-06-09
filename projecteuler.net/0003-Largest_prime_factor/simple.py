#!/usr/bin/python

#The prime factors of 13195 are 5, 7, 13 and 29.

#What is the largest prime factor of the number 600851475143 ?

import math;

#N=50
#N=65537
N=600851475143
#N=6008514751433543
#N=6517514358

#TOP = int(math.sqrt(N))

i = 2

while i <= N:

    if (N % i) == 0:
      N = N / i
      print i, '->', N
    else:
      i = i + 1
