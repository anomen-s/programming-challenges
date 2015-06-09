#!/usr/bin/python

# If we list all the natural numbers below 10 that are multiples of 3 or 5, we get 3, 5, 6 and 9. The sum of these multiples is 23.
# Find the sum of all the multiples of 3 or 5 below 1000.

TOP = 1000

T=TOP-1
def sum(N):
 return N * (N+1) / 2


s3 = 3 * sum(T/3)
s5 =  5 * sum(T/5)
s15 = 15 * sum(T/15)


print s3, s5, s15
print s3 + s5 - s15

