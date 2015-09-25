#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
The cube, 41063625 (345**3), can be permuted to produce two other cubes: 56623104 (384**3) and 66430125 (405**3). 
In fact, 41063625 is the smallest cube which has exactly three permutations of its digits which are also cube.

Find the smallest cube for which exactly five permutations of its digits are cube.
'''

import math

N=3
N=5
N=20

DEBUG = True
def d(args):
    global DEBUG
    if DEBUG:
      print(args)

   
def key(num):
   snum = str(num)
   k= ''.join(sorted(snum))
   return k

def main():

    minF = 10**9
    end = 10**9
    P = {}
    i = 10
    while i < end:
      p = i*i*i
      k = key(p)
      Pk = P.setdefault(k, [])
      Pk.append(i)
      if len(Pk) >= N:
         end = min(end, 3*i)
         if Pk[0] < minF:
           minF = Pk[0]
           print([i, k, Pk, 'result:', Pk[0]**3, 'test:', len(Pk) == N])
      i = i + 1

if  __name__ =='__main__':main()

