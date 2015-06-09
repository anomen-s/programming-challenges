#!/usr/bin/python

#The prime factors of 13195 are 5, 7, 13 and 29.

#What is the largest prime factor of the number 600851475143 ?

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

