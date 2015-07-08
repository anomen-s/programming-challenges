#!/usr/bin/python


import gmpy2
import math
from bitarray import bitarray


MAX = 15499.0 / 94744
# MAX=4.0/10

def get_resilience(n):
    rescount = 0
    for i in xrange(1, n):
        if gmpy2.gcd(i, n) == 1:
            rescount = rescount + 1

    res = 1.0 * rescount / (n - 1)
    return res

for n in xrange(2, 10 ** 6):

#    if n == (10 ** 3):
#        print '1000'
#    elif n == (10 ** 5):
#        print '10000'
#    elif n == (10 ** 6):
#        print '100080'

    if gmpy2.is_prime(n):
        continue

    rescount = 0
    for i in xrange(1, n):
        if gmpy2.gcd(i, n) == 1:
            rescount = rescount + 1

    res = 1.0 * rescount / (n - 1)
    print n, res
    if res < MAX:
        print 'found: ',
        print n, res
        exit()