#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
145 is a curious number, as 1! + 4! + 5! = 1 + 24 + 120 = 145.

Find the sum of all numbers which are equal to the sum of the factorial of their digits.

Note: as 1! = 1 and 2! = 2 are not sums they are not included.

Notes:
9!=362.880
9.999.999 > 7*9! = 2.540.160

=> max length: 7 digits
-> max curious number < 2.540.160

solution: http://oeis.org/A014080
'''
import math

TOP=7 * math.factorial(9)

DEBUG = True
def d(args):
    global DEBUG
    if DEBUG:
      print(args)

F = [math.factorial(x) for x in range(10)]

def fsum(n):
    global F
    fs = 0
    while n > 0:
      r = n % 10
      n = n // 10
#      d('divided %i: rem %i = F %i'%(n,r,F[r]))
      fs = fs + F[r]
    return fs

def main_simple():
  '''
    this is simple exhaustive test
  '''
  RES = 0
  
  for i in range(10, TOP):
    
    if fsum(i) == i:
      d('%i: [%i]' % (i, RES))
      RES = RES + i

  print(RES)


def main():
  '''
    This is optimized test.
    It first checks numbers nnn9.
    If nnn9 < fsum(nnn9), then immediate 9 lower numbers are also checked.
    Otherwise nnn8, nnn7,...nnn0 can be skipped, because they will have even bigger difference nnnX > fsum(nnnX)
  '''
  RES = 0
  
  for i1 in range(1, TOP//10):
   i9 = i1*10 + 9
   fs_i9 = fsum(i9)
   if fs_i9 >= i9:
     for i in range(i1*10, i1*10+10):
       if i == fsum(i):
         d(i)
         RES = RES + i
  
  print('sum', RES)


if  __name__ =='__main__':main()
