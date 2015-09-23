#!/usr/bin/python

#The number 3797 has an interesting property. Being prime itself, it is possible to continuously remove digits from left to right, and remain prime at each stage: 3797, 797, 97, and 7. Similarly we can work from right to left: 3797, 379, 37, and 3.

#Find the sum of the only eleven primes that are both truncatable from left to right and right to left.

#NOTE: 2, 3, 5, and 7 are not considered to be truncatable primes.


import gmpy2
import math
from bitarray import bitarray

#tip
RANGE=10**6 #00000


#def sieve(primes, p, RANGE):
#  i = p + p
#  while i < RANGE:
#    primes[i] = False
#    i = i + p

def sieve(RANGE):
    primes = bitarray(RANGE)
    primes.setall(True)
    primes[0] = False
    primes[1] = False
    # find primes
    for p in xrange(2, len(primes)/2+1):
      if primes[p]:
        i = p + p
        while i < RANGE:
          primes[i] = False
          i = i + p
    return primes
    

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
  

primes = sieve(RANGE)
print 'Sieve completed'

# find primes
#for index in xrange(2, len(primes)/2+1):
#  if primes[index]:
#    sieve(primes, index)
#    
#print 'Sieve completed'

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

