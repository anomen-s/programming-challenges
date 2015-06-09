#!/usr/bin/python

#2520 is the smallest number that can be divided by each of the numbers from 1 to 10 without any remainder.

#What is the smallest positive number that is evenly divisible by all of the numbers from 1 to 20?

import math;

n=100

# (a1 + a2 + ... an) * (a1 + a2 + ... an) = a1^2 + 2*a1a2 + ... + an^2

#
#   a11 a12 a13 a14 ...    - 2 3 4 ... N      n*(n+1)/2 - 1**2
#   a21 a22                2 - 6 8 .. 2N    2*n*(n+1)/2 - 2**2
#   a31                    3 6 - 12 .. 3N    3*n*(n+1)/2 - 3**2
#   ..                      
#   an1                    N ..        NN    n**n*(n+1)/2 - N**2
#


SQR_SUM_T=n*(n+1)/2 * n*(n+1)/2

print 'square of sum: %s' % SQR_SUM_T


SUM_SQR_T=(2*n**3 + 3*n**2 + n )/ 6

print 'sum of squares: %s (http://en.wikipedia.org/wiki/Square_pyramidal_number)' % SUM_SQR_T


print 'result: ', (SQR_SUM_T - SUM_SQR_T)
