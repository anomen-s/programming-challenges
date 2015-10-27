#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
It is possible to write five as a sum in exactly six different ways:

 4 + 1
 3 + 2
 3 + 1 + 1
 2 + 2 + 1
 2 + 1 + 1 + 1
 1 + 1 + 1 + 1 + 1

How many different ways can one hundred be written as a sum of at least two positive integers?

Observations:
TAB[n][m] - number of combinations to get sum n with numbers <= m

TAB[n][n] = for i: subtract i and compute number of partitionings (containing only members <=i) for remainder 
eg:
6 :: =11:   6+0    5+1   4+2 4+1+1 3+3 3+2+1 3+1+1+1 2+2+2  2+2+1+1 2+1+1+1+1 1+1+1+1+1+1
[6,6] =   [0,6]| [1,5] | [2,4]    |   [3,3]         |   [4,2]                |  [5,1]

also see:
https://en.wikipedia.org/wiki/Partition_(number_theory)#Partition_function
'''

import time
import math
DEBUG = False


N=100
#N=5
#N=6
#N=10**3


def main():
    d('build table')
    TAB = [[0 for i in range(n+1)] for n in range(N+1)]
    TAB[0][0] = 1

    d('compute values')
    for num in range(1,len(TAB)):
      for maxNum in range(num+1):
        TAB[num][maxNum] = sum([TAB[i][min(i,num-i)] for i in range(num-maxNum, num)])

    

    for x in enumerate(TAB): d(x)
    
    print(['result', TAB[N][N]-1])

def d(args):
    global DEBUG
    if DEBUG:
      print(args)

if  __name__ =='__main__':
  tStart = time.time()
  main()
  print(['time[ms]',int((time.time() - tStart)*1000)])

