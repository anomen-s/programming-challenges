#!/usr/bin/python

#The sum of the primes below 10 is 2 + 3 + 5 + 7 = 17.

#Find the sum of all the primes below two million.

import math;

RANGE=2000000

primes = [1 for i in xrange(RANGE)]

def check(p):
  global primes
  i = p + p
  while i < RANGE:
    primes[i] = 0
    i = i + p


for index in xrange(2, RANGE):
  if primes[index] == 1:
    check(index)
    

cnt = 0
SUM=0
for index in xrange(2, RANGE):
  if primes[index] == 1:
    cnt = cnt + 1
    SUM = SUM + index
    
print cnt
print SUM
