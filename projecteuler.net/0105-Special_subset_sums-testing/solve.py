#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
Let S(A) represent the sum of elements in set A of size n. We shall call it a special sum set if for any two non-empty disjoint subsets, B and C, the following properties are true:

S(B) ≠ S(C); that is, sums of subsets cannot be equal.
If B contains more elements than C then S(B) > S(C).

For example, {81, 88, 75, 42, 87, 84, 86, 65} is not a special sum set because 65 + 87 + 88 = 75 + 81 + 84, whereas {157, 150, 164, 119, 79, 159, 161, 139, 158} satisfies both rules for all possible subset pair combinations and S(A) = 1286.

Using sets.txt (right click and "Save Link/Target As..."), a 4K text file with one-hundred sets containing seven to twelve elements (the two examples given above are the first two sets in the file), identify all the special sum sets, A1, A2, ..., Ak, and find the value of S(A1) + S(A2) + ... + S(Ak).

NOTE: This problem is related to Problem 103 and Problem 106.

Observations:
- A = {a1,a2,...,an}


need to test propertiess:
- a1+a2 > an
- a1+a2+a3 > a(n)+a(n-1)
- a1+a2+a3+a4 > a(n)+a(n-1)+a(n-2)
- these imply all other ax1+...+axn < ay1+...+ay(n-1)

- equal sums of subsets
   - cannot have different size
   - possible sizes are only 2 and 3
   - this test eliminates most of the combinations, but is slower

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
    if not test1(a, 0, 0, sums):
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
  L=a[0]
  U=0
  for i in range(1,(len(a)+1)//2):
    L = L + a[i]
    U = U + a[len(a)-i]
    if L <= U:
      return False
  return True
  
def main():
 totalSum = 0
 
 with open('p105_sets.txt', 'r') as f:
    lines = f.readlines() # read all lines from file

 for line in lines:
    a = [int(x) for x in line.strip().split(',')]
    a.sort()
    if test(a):
      aSum = sum(a)
      totalSum = totalSum + aSum
      d(['found', a, aSum, totalSum])
 print(['result',totalSum])

def d(args):
    global DEBUG
    if DEBUG:
      print(args)

if  __name__ =='__main__':
  tStart = time.time()
  main()
  print(['time[ms]',int((time.time() - tStart)*1000)])

