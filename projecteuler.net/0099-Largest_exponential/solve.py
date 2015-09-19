#!/usr/bin/python3
# -*- coding: utf-8 -*-

#Comparing two numbers written in index form like 211 and 37 is not difficult, as any calculator would confirm that 211 = 2048 < 37 = 2187.
#
#However, confirming that 632382518061 > 519432525806 would be much more difficult, as both numbers contain over three million digits.
#
#Using base_exp.txt (right click and 'Save Link/Target As...'), a 22K text file containing one thousand lines with a base/exponent pair on each line, determine which line number has the greatest numerical value.
#
#NOTE: The first two lines in the file represent the numbers in the example given above.

# Observation: 
# logarithm can be used to compare values
# log(a**b) = b * log(a)

import math

def readfile(filename):
    f = open(filename)
    try:
       data = f.readlines()
    finally:
       f.close()
    return [list(map(int, x.split(','))) for x in data]

def log(base, exp):
   return exp * math.log10(base)


def main():

    maxNl = 0
    maxLine = 0
    line = 0
    
    numbers = readfile('p099_base_exp.txt')
    for [nbase, nexp] in numbers:
      line = line + 1
      nl = log(nbase, nexp)
#      print ([line, nbase, nexp, nl])
      if abs(maxNl-nl) < ((10**-7)*nl):
        print('warning close: ', line, maxLine, nl, maxNl)
      if (nl > maxNl):
        maxNl = nl
        maxLine = line
        
    print([maxLine, maxNl, numbers[line-1]])
      

    
if  __name__ =='__main__':main()
