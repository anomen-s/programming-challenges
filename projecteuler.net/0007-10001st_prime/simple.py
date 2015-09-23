#!/usr/bin/python

#By listing the first six prime numbers: 2, 3, 5, 7, 11, and 13, we can see that the 6th prime is 13.

#What is the 10 001st prime number?

import math;

TOP=10001
#TOP=20001
#TOP=20


def isPrime(n):
  if (n % 2) ==0:
    return False
  
  i=3
  s = int(math.sqrt(n))
  while i <= s:
    if (n % i) == 0:
      return False
    i = i + 2
    
  return True;

#print 2

idx = 3
cnt = 1
while cnt < TOP:

  if isPrime(idx):
    cnt = cnt + 1
  
  idx = idx + 1

print (idx-1)
