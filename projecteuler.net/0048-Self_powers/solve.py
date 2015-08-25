#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
The series, 1**1 + 2**2 + 3**3 + ... + 10**10 = 10405071317.

Find the last ten digits of the series, 1**1 + 2**2 + 3**3 + ... + 1000**1000.
'''

N=1000
DIGITS=10

def powers(n, digits):
    s = 0
    for i in range(1,n+1):
      s = s + (i ** i)

    s = s % (10 ** digits)
    return s

def main():
    s = powers(N, DIGITS)
    print(s)
    
if  __name__ =='__main__':main()
