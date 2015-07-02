#!/usr/bin/python

#The prime factors of 13195 are 5, 7, 13 and 29.

#What is the largest prime factor of the number 600851475143 ?

import gmpy2
import math
from bitarray import bitarray

#tip
RANGE=10**7 #00000

ODD = map(str, [1,3,5,7,9])
START = map(str, [2])

def checkTruncPrime(n, found, lprimes, rprimes):

  isPrime= gmpy2.is_prime(int(n))

  good = True
  
  nsl1=n[1:]
  if not rprimes.has_key(nsl1):
    good = False
  else:
    if isPrime:
     rprimes[n] = 0;

  nsr1=n[:-1]
  if not lprimes.has_key(nsr1):
    good = False
  else:
    if isPrime:
      lprimes[n] = 0;

  # is it good both ways?
  if not good:
    return False

  if not isPrime:
    return False

  if result.has_key(nsl1):
    result[nsl1] = 1 # mark as substring of bigger tprime
  if result.has_key(nsr1):
    result[nsr1] = 1 # mark as substring of bigger tprime
  result[n] = 0 # add new item

  return True
 

def generate(len, prev = ''):
  if len == 1:
    for t in ODD:
     yield (prev+t)
  else:
    for t in ODD:
      for s in generate (len-1, prev+t):
        yield s
  
result = {'2':0, '3':0,'5':0,'7':0}

lprimes=result.copy()
rprimes=result.copy()

for l in range(2, 7):
 for n in generate(l):
   checkTruncPrime(n, result, lprimes, rprimes)

  # tprime might start with '2'
 for n in generate(l-1,'2'):
   checkTruncPrime(n, result, lprimes, rprimes)


#for i in result.items(): print i
for i in  result.items():
  print i

r = sorted([int(i[0]) for i in filter(lambda x: int(x[0])>9, result.items())])

print 'result:', sum(r),'=',r

