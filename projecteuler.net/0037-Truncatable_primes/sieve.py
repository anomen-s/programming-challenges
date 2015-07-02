#!/usr/bin/python

#The prime factors of 13195 are 5, 7, 13 and 29.

#What is the largest prime factor of the number 600851475143 ?

import gmpy2
import math
from bitarray import bitarray

#tip
RANGE=10**6 #00000

primes = bitarray(RANGE)
primes.setall(True)
primes[0] = False
primes[1] = False

def sieve(primes, p):
  global RANGE
  i = p + p
  while i < RANGE:
    primes[i] = False
    i = i + p

def checkIsPrimeG(p):
  return gmpy2.is_prime(p)


def checkTruncPrime(n):
  ns = str(n)
  ns1=ns[1:-1]
  if ns1.find('0') >= 0 or ns1.find('2') >= 0 \
     or  ns1.find('4') >= 0 or ns1.find('6') >= 0 \
     or  ns1.find('8') >= 0:
    return False
  while len(ns) > 0:
#    print('test',ns)
    if not primes[int(ns)]:
      return False
    ns = ns[1:]


  ns = str(n)
  while len(ns) > 0:
#    print('test',ns)
    if not primes[int(ns)]:
      return False
    ns = ns[0:-1]
     
  return True
  

# find primes
for index in xrange(2, len(primes)/2+1):
  if primes[index]:
    sieve(primes, index)
    
print 'Sieve completed'

#print primes

#for index in [70823]:
RES=[]
# search for trunc.primes
for index in xrange(11, RANGE, 2):
  if checkTruncPrime(index):
    RES.append(str(index))
    print (index)



#print(RES)
print(RES)
print sum(map(int, RES))

