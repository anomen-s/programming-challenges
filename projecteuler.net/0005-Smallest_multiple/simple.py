#!/usr/bin/python

#2520 is the smallest number that can be divided by each of the numbers from 1 to 10 without any remainder.

#What is the smallest positive number that is evenly divisible by all of the numbers from 1 to 20?

import math;

TOP=20 + 1

def factors(N):
  f = [0 for i in range(TOP)]
  i = 2
  while N > 1:

    if (N % i) == 0:
      N = N / i
      f[i] = f[i] + 1
    else:
      i = i + 1
  return f


total = [0 for i in range(TOP)]

for i in range(TOP):
   f = factors(i)
   total = [max(total[i], f[i]) for i in range(TOP)]

print total

R=1
for i in range(TOP):
   R = R * (i ** total[i])

print "result", R
