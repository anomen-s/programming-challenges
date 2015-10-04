#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
Starting with the number 1 and moving to the right in a clockwise direction a 5 by 5 spiral is formed as follows:

21 22 23 24 25
 20  7  8  9 10
 19  6  1  2 11
 18  5  4  3 12
17 16 15 14 13

It can be verified that the sum of the numbers on the diagonals is 101.

What is the sum of the numbers on the diagonals in a 1001 by 1001 spiral formed in the same way?
'''

import math


def main():

    N = 1001
    S = 1
    for col in range(1, (N-1)//2 + 1):
      idx = 2*col + 1
      tr = idx**2          # top right
      tr1 = (idx-2)**2     # top right (previous)
      bl = (tr1+tr)//2     # bottom left
      tl = (bl+tr)//2      # top left
      br = (tr1+bl)//2     # bottom right
      S = S + tr + bl + tl + br
      print([tr,bl,tl,br])

    print(['result',S])
    

if  __name__ =='__main__':main()

