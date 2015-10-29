#!/usr/bin/python3
# -*- coding: utf-8 -*-

import math

DEBUG = False
N=1000**2


def d(args):
    global DEBUG
    if DEBUG:
      print(args)


         
def computeLength(start):
    n = start
    c = 1
    while n > 1:
        if (n & 1) == 0:
          n = n//2
        else:
          n = 3*n+1
        c = c + 1
    return c

def findLongest(chains):
    maxv = 0
    maxi = 0
    for i in range(1,len(chains)):
      if chains[i] > maxv:
        maxv = chains[i]
        maxi = i
    return (maxv, maxi)
    
    
def xmain():
    return 0
    
def main():
    
    chains = [0 for i in range(1000**2)]
    for i in range(1,N):
#      print(i)
      chains[i] = computeLength(i)
    print('done')
    print(findLongest(chains))
    for i in range(20): print(chains[i*20:i*20+20])

if  __name__ =='__main__':main()
