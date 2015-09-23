#!/usr/bin/python

#By listing the first six prime numbers: 2, 3, 5, 7, 11, and 13, we can see that the 6th prime is 13.

#What is the 10 001st prime number?

import math;

TOP=10001
#TOP=20001

#tip
RANGE=300000

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
for index in xrange(2, RANGE):
  if primes[index] == 1:
    cnt = cnt + 1
    if cnt == TOP:
      print '%sth prime = %s' % (cnt, index)
      exit
