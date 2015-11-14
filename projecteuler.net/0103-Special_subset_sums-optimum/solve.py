#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
Let S(A) represent the sum of elements in set A of size n. We shall call it a special sum set if for any two non-empty disjoint subsets, B and C, the following properties are true:
S(B) ≠ S(C); that is, sums of subsets cannot be equal.
If B contains more elements than C then S(B) > S(C).

If S(A) is minimised for a given n, we shall call it an optimum special sum set. The first five optimum special sum sets are given below.

n = 1: {1}
n = 2: {1, 2}
n = 3: {2, 3, 4}
n = 4: {3, 5, 6, 7}
n = 5: {6, 9, 11, 12, 13}

It seems that for a given optimum set, A = {a1, a2, ... , an}, the next optimum set is of the form B = {b, a1+b, a2+b, ... ,an+b}, where b is the "middle" element on the previous row.

By applying this "rule" we would expect the optimum set for n = 6 to be A = {11, 17, 20, 22, 23, 24}, with S(A) = 117. 
However, this is not the optimum set, as we have merely applied an algorithm to provide a near optimum set. 
The optimum set for n = 6 is A = {11, 18, 19, 20, 22, 25}, with S(A) = 115 and corresponding set string: 111819202225.

Given that A is an optimum special sum set for n = 7, find its set string.

Observations:
- A = {a1,a2,...,an}

NOTE: **** near optimum rule gives correct answer for n=7 ****

need to test propertiess:
- a1+a2 > an
- a1+a2+a3 > a(n)+a(n-1)
- a1+a2+a3+a4 > a(n)+a(n-1)+a(n-2)
- these imply all other ax1+...+axn < ay1+...+ay(n-1)

- equal sums of subsets
   - cannot have different size
   - possible sizes are only 2 and 3
   - this test eliminates most of the combinations, but is slower
   - TODO: optimize it, no need to check 4+-member subsets, no need to check subsets where members are all from lower or upper end,...

- a1 might be greater then a1 for any suboptimal set
- a1+a2 > an => a1+a2 > a2+5 => a1 > 5 => a7 > 11
- a1+a2 > an > 11
- a2+a2 > a1+a2 > 11
- a2  > 5
- a1+a2 > a3 >= a2+1

'''

import time
import math
DEBUG = True


#N=7
#N=5

def test(a):
    if not test2(a):
      return False
    sums = {}
    if not test1(a, 1, 0, sums):
      return False
    return True

def test1(a, idx, prevSum, sums):
   
   curr = a[idx]
   currSum = prevSum + curr
   if currSum in sums:
     return False
   else:
     sums[currSum] = currSum
   
   idx1 = idx+1
   if idx1 < len(a):
     if not test1(a, idx1, currSum, sums):
       return False
     if not test1(a, idx1, prevSum, sums):
       return False
   return True
     
   


def test2(a):
  
  L = a[1]+a[2]
  U = a[7]
  if L <= U:
    return False
  L = L + a[3]
  U = U + a[6]
  if L <= U:
    return False
  L = L + a[4]
  U = U + a[5]
  if L <= U:
    return False
  return True

def main():
 cnt = 0
 minSum = 10**10
 minSet = None
 
 for a3 in range(3, 40): # upper limit set after founding solution
  print([a3, cnt])
  for a2 in range(5, a3):
   for a1 in range(2, a2):
    for a7 in range(12, a1+a2):
     for a6 in range(a3+3, a7):
      for a5 in range(a3+2, a6):
       for a4 in range(a3+1, a5):
         a = [0,a1,a2,a3,a4,a5,a6,a7]
         if test(a):
           cnt = cnt + 1
           asum = sum(a)
           if asum < minSum:
             minSum = asum
             minSet = a
             print(['found',asum, a[1:]])



def d(args):
    global DEBUG
    if DEBUG:
      print(args)

if  __name__ =='__main__':
  tStart = time.time()
  main()
  print(['time[ms]',int((time.time() - tStart)*1000)])

