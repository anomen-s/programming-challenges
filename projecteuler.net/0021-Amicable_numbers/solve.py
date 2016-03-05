#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
Let d(n) be defined as the sum of proper divisors of n (numbers less than n which divide evenly into n).
 If d(a) = b and d(b) = a, where a ≠ b, then a and b are an amicable pair and each of a and b are called amicable numbers.

For example, the proper divisors of 220 are 1, 2, 4, 5, 10, 11, 20, 22, 44, 55 and 110; therefore d(220) = 284. The proper divisors of 284 are 1, 2, 4, 71 and 142; so d(284) = 220.

Evaluate the sum of all the amicable numbers under 10000.


http://mathworld.wolfram.com/AmicablePair.html
'''

DEBUG = True

N=10000

def d(args):
    global DEBUG
    if DEBUG:
      print(args)


# get factors of the number as dictionary
def factors(N):
  f = {}
  i = 2
  while N > 1:

    if (N % i) == 0:
      N = N / i
      if i in f:
        f[i] = f[i] + 1
      else:
        f[i] = 1
    else:
      i = i + 1
  return f


def genDivisors(idx, curr, flist, f, dividers):
   '''
   generate all divisors of number
   idx - current position in flist
   curr - current product
   flist - list of factors
   f - map of cardinality of factors
   dividers - result
   '''
   if idx >= len(flist):
     return
   #d(['R', idx, curr, flist[idx]])
   t = curr
   for i in range(1+f[flist[idx]]):
     #d(['add',t])
     dividers.add(t)
     genDivisors(idx+1, t, flist, f, dividers)
     t = t * flist[idx]
   return

def computeDivisorsSum(n):
   f = factors(n)
   #d(f)
   dividers = {1, n}
   
   genDivisors(0, 1, list(f), f, dividers)
   #d(dividers)
   return sum(dividers) - n


def main():
    divisors = [0 for i in range(N)]
    for i in range(1, N):
      divisors[i] = computeDivisorsSum(i)

    d('divisors computed')
    
    RES = set()
    
    for i in range(1, N):
      apair = divisors[i]
      # d('check %i and %i' % (i, apair))
      if apair < len(divisors) and divisors[apair] == i:
         d('found %i and %i' % (i, apair))
         if (apair != i):
          RES.add(i)
          RES.add(apair)
 
    print(RES)
    print('result: %i' % sum(RES))

#    for i in range(20): d(divisors[i*20:i*20+20])


def tests():
    print(factors(220))
    print(computeDivisorsSum(220))
    print(computeDivisorsSum(284))

if  __name__ =='__main__':
  main()
  #tests()
 