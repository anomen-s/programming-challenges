#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
In England the currency is made up of pound, £, and pence, p, and there are eight coins in general circulation:
1p, 2p, 5p, 10p, 20p, 50p, £1 (100p) and £2 (200p).

It is possible to make £2 in the following way:
1×£1 + 1×50p + 2×20p + 1×5p + 1×2p + 3×1p

How many different ways can £2 be made using any number of coins?
'''

import math

N=2

DEBUG = True
def d(args):
    global DEBUG
    if DEBUG:
      print(args)

COINS=[1, 2, 5, 10, 20, 50, 100, 200][::-1]
SUM=200

def search(selected, idx, sumCurr, results):
    global SUM, COINS
    for i in range(0, SUM//COINS[idx]+1):
      currCoin = COINS[idx]*i
      newSum = sumCurr + currCoin
      if newSum == SUM:
         results.append(selected+[i])
         return
      elif newSum < SUM:
         if len(COINS) > (idx+1):
           search(selected+[i], idx+1, newSum, results)
      else:
         return  

def main():

    R = []
    search([], 0, 0, R) 
    for r in R: print (r)
    print(len(R))
    



if  __name__ =='__main__':main()

