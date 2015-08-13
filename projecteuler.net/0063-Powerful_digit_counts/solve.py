#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
The 5-digit number, 16807=7**5, is also a fifth power. Similarly, the 9-digit number, 134217728=8**9, is a ninth power.

How many n-digit positive integers exist which are also an nth power?

Observations:
1) x < 10, because len(x**n) = n+1
2) if len(x**n) < n then len(x(n+1) < n+1
'''

DEBUG = True

def d(args):
    global DEBUG
    if DEBUG:
      print(args)

def getPowers(n):
    r = set() # result
    i = n # iterator
    low = 1
    high = 10 # max number with i digits digit limit
    while i < high and i >= low:
      r.add(i)
      i = i * n
      high = high * 10
      low = low * 10

    return r

def main():
    r = set()
    for i in range(1,10):
      ri = getPowers(i)
      d('%i -> %s' %(i, sorted(ri)))
      r = r|ri
    print (sorted(r))
    print ('result = %i' % len(r))

if  __name__ =='__main__':main()
