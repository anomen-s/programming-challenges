#!/usr/bin/python

from bitarray import bitarray

# tip
PRIMES = 10 ** 5
RANGE = 10 ** 3

primes = bitarray(PRIMES)
primes.setall(True)
primes[0] = False
primes[1] = False


def sieve(primes, p):
    i = p + p
    while i < len(primes):
        primes[i] = False
        i = i + p


for i in xrange(2, len(primes) / 2 + 1):
    if primes[i]:
        sieve(primes, i)

#print primes
print 'Sieve finished'


def compute_n(a, b, max):
    n = 0
    while True:
        res = n * n + a * n + b
        if (a==-61 and b ==971):
            print res, '',
        if check_is_prime(res):
            n = n + 1
        else:
            if n > max[0]:
                max[0] = n
                max[1] = a
                max[2] = b
            return max


def check_is_prime(p):
    global primes, PRIMES
    if p <= 0:
        return False
    if p >= PRIMES:
        raise Exception("out of primes table")
    return primes[p]

MAX = [0, 0, 0]

for a in xrange(RANGE):
    for b in xrange(RANGE):
#        print 'check', a, b
        compute_n(a, b, MAX)
        compute_n(-a, b, MAX)
        compute_n(a, -b, MAX)
        compute_n(-a, -b, MAX)

print ''
print (MAX, '->', MAX[1]*MAX[2])
