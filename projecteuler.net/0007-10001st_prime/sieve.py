#!/usr/bin/python

#The prime factors of 13195 are 5, 7, 13 and 29.

#What is the largest prime factor of the number 600851475143 ?

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
