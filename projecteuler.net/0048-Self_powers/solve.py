#!/usr/bin/python3
# -*- coding: utf-8 -*-

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
