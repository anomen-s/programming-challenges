#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
How many ways are there to write the number 1/2 as a sum of inverse squares using distinct integers between 2 and 80 inclusive?
'''

import math

N=45
N=80
N=35 # this is max which can be computed in reasonable time

DEBUG = True
def d(args):
    global DEBUG
    if DEBUG:
      print(args)


def factors(n, N):
  f = [0 for i in range(N)]
  i = 2
  while n > 1:

    if (n % i) == 0:
      n = n / i
      f[i] = f[i] + 1
    else:
      i = i + 1
  return f

def lcd(N):
  N1= N+1
  total = [0 for i in range(N1)]
  for i in range(1, N1):
    f = factors(i, N1)
    total = [max(total[i], f[i]) for i in range(N1)]

  R=1
  for i in range(1,N1):
    R = R * (i ** total[i])

  d(["lcd", R])

  return R

LCD = 0
SUM = 0
PARTIALSUMS = []
FACTORS = []

def search(selected, idx, sumCurr, results):
    global LCD, SUM, PARTIALSUMS, FACTORS
    newSum = sumCurr + FACTORS[idx]
#    d([selected,idx])
    if newSum == SUM:
       results.append(selected + [idx])
       print(results[-1])
    if idx == N:
       return
    if newSum < SUM and (newSum + PARTIALSUMS[idx+1]) >= SUM:
         search(selected+[idx], idx+1, newSum, results)

    if sumCurr < SUM and (sumCurr + PARTIALSUMS[idx+1]) >= SUM:
       search(selected, idx+1, sumCurr, results)

def main():
    global N, LCD, PARTIALSUMS, FACTORS, SUM
    LCD = lcd(N)**2;
    SUM = LCD // 2
    FACTORS = [0 for i in range(N+1)]

    for n in range(1, N+1):
      FACTORS[n] = LCD // (n*n)

    print('factors:');
    print(FACTORS)
    print([x/LCD for x in FACTORS])

    # sum of factors i..N    
    PARTIALSUMS = [0 for i in range(N+1)]
    for i in range(1,N+1):
      PARTIALSUMS[i] = sum(FACTORS[i:])

    print('partialsums:');
    print(PARTIALSUMS)
    print([100*x/LCD for x in PARTIALSUMS])
    
    r = []
    search([], 2, 0, r) 
    print (r)
    


def test():
    global N
    LCD = lcd(N)**2;
    SUM = LCD // 2
    FACTORS = [0 for i in range(N+1)]

    for n in range(1, N+1):
      FACTORS[n] = LCD // (n**2)

    print(FACTORS)
    
    print('lcd/2:   %i ' % (LCD // 2))
    s =0
    for i in [2,3,4,5,7,12,15,20,28,35]:
      s = s + LCD // (i*i)

    print('lcd*sum: %i ' % s)
    

if  __name__ =='__main__':main()

