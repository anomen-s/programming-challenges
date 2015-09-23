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
#print 3

idx = 6
cnt = 2

while cnt < TOP:

  if isPrime(idx-1):
    cnt = cnt + 1
#    print (idx-1)
  if isPrime(idx+1):
    cnt = cnt + 1
#    print (idx+1)
  
  idx = idx + 6


if (cnt == TOP):
  print  'result', (idx+1-6)
else:
  print 'result', (idx-1-6)

