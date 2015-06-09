#!/usr/bin/python

# If we list all the natural numbers below 10 that are multiples of 3 or 5, we get 3, 5, 6 and 9. The sum of these multiples is 23.
# Find the sum of all the multiples of 3 or 5 below 1000.

TOP = 1000
S = 0
i = 0

while i < TOP:
    if (i % 5) != 0:
       S = S + i;
    i = i + 3


i = 0
while i < TOP:
    S = S + i
    i = i + 5


print S
