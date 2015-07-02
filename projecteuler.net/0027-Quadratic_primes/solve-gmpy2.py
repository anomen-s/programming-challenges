#!/usr/bin/python

import gmpy2

# tip
RANGE = 10 ** 3

def compute_n(a, b, max):
    n = 0
    while True:
        res = n * n + a * n + b
        if check_is_prime(res):
            n = n + 1
        else:
            if n > max[0]:
                max[0] = n
                max[1] = a
                max[2] = b
            return max


def check_is_prime(p):
    return gmpy2.is_prime(p)

MAX = [0, 0, 0]

for a in xrange(RANGE):
    for b in xrange(RANGE):
        compute_n(a, b, MAX)
        compute_n(-a, b, MAX)
        compute_n(a, -b, MAX)
        compute_n(-a, -b, MAX)

print (MAX, '->', MAX[1]*MAX[2])
