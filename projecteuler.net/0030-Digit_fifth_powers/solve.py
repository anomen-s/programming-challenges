#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
Surprisingly there are only three numbers that can be written as the sum of fourth powers of their digits:
 1634 = 14 + 64 + 34 + 44
 8208 = 84 + 24 + 04 + 84
 9474 = 94 + 44 + 74 + 44

As 1 = 14 is not a sum it is not included.

The sum of these numbers is 1634 + 8208 + 9474 = 19316.

Find the sum of all the numbers that can be written as the sum of fifth powers of their digits.

Observation:
- cannot have 7 (or more) digits, because 7*(9**5) has only 6 digits
'''
TOP=6*(9**5)

DEBUG = True
def d(args):
    global DEBUG
    if DEBUG:
      print(args)


def pow5sum(n):
    fs = 0
    while n > 0:
      r = n % 10
      n = n // 10
      fs = fs + (r**5)
    return fs

def main():
  s = 0
  for i in range(10, TOP):
    fs = pow5sum(i)
    if i == fs: 
      s = s + i
      print(i)


  print(['sum',s])

if  __name__ =='__main__':main()
