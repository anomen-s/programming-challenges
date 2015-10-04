#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
A permutation is an ordered arrangement of objects. For example, 3124 is one possible permutation of the digits 1, 2, 3 and 4. 
If all of the permutations are listed numerically or alphabetically, we call it lexicographic order. 
The lexicographic permutations of 0, 1 and 2 are:

012   021   102   120   201   210

What is the millionth lexicographic permutation of the digits 0, 1, 2, 3, 4, 5, 6, 7, 8 and 9?
'''

import math


def main():

    #SET=list(range(3))
    #N = 3 - 1
    SET=list(range(10))
    N = 10**6 - 1

    for idx in range(len(SET)):
      cCount = math.factorial(len(SET)-1)
      elem = N // cCount
      N = N % cCount
      print(SET.pop(elem), end='')

    print('')
    

if  __name__ =='__main__':main()

