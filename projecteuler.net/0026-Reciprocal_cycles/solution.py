#!/usr/bin/python
# -*- coding: utf-8 -*-
# Work out the first ten digits of the sum of the following one-hundred 50-digit numbers.

# A unit fraction contains 1 in the numerator. The decimal representation of the unit fractions with denominators 2 to 10 are given:1/2	= 	0.5
#1/3	= 	0.(3)
#1/4	= 	0.25
#1/5	= 	0.2
#1/6	= 	0.1(6)
#1/7	= 	0.(142857)
#1/8	= 	0.125
#1/9	= 	0.(1)
#1/10	= 	0.1


#Where 0.1(6) means 0.166666..., and has a 1-digit recurring cycle. It can be seen that 1/7 has a 6-digit recurring cycle.

#Find the value of d < 1000 for which 1/d contains the longest recurring cycle in its decimal fraction part.

TOP=1000

MAX_D = 0
MAX_L = 0

def divide(n):
  d = 10
  rem = 0
  rems = [0 for i in xrange(n)]
  i = 1;
  while True:
    division = d / n 
    reminder = d % n 
    if rems[reminder] > 0: 
      return i - rems[reminder]
    rems[reminder] = i
    d = reminder * 10
    i = i + 1

def divideP(n):
  d = 10
  rem = 0
  rems = [0 for i in xrange(n)]
  i = 1;
  while True:
    division = d / n 
    reminder = d % n
    print reminder, "", 
    if rems[reminder] > 0: 
      return i - rems[reminder]
    rems[reminder] = i # 3 = 1
    d = reminder * 10
    i = i + 1
  print ""    

for i in xrange(2, TOP):
    l = divide(i)
    if l > MAX_L:
      MAX_D = i
      MAX_L = l
    print i, l, 1.0/i
    
print 'max:', MAX_D, MAX_L
divideP(MAX_D)
