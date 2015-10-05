#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
It can be seen that the number, 125874, and its double, 251748, contain exactly the same digits, but in a different order.

Find the smallest positive integer, x, such that 2x, 3x, 4x, 5x, and 6x, contain the same digits.

'''

import math

DC = [2,3,7,11,13,17,19,21,23,29]
def digitHash(n):
    r = 1
    while n > 0:
      r = r * DC[n % 10]
      n = n // 10
    return r

def digitHashList(n):
    '''
      Alternative digit checking.
      Seems to be a bit faster even if it's list manipulation.
    '''
    l = list(str(n))
    l.sort()
    return l
    
def main():
    R = range(2,7)
   
    for n in range(10,10**9):
      h=digitHash(n)
      #print([n,h])
      found = True
      for i in R:
        if h != digitHash(n*i):
         found = False
         break
      if found:
         print(['found',n,'...',n*6])
         #print(['found',n])
         exit()

         
       
    

if  __name__ =='__main__':main()

