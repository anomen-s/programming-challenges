#!/usr/bin/python3
# -*- coding: utf-8 -*-

import math

DEBUG = True

N=100

def d(args):
    global DEBUG
    if DEBUG:
      print(args)

def digitsum(n):
    s = 0
    while n > 0:
      d = n % 10
      n = n // 10
      s = s + d
    return s

def fac(n):
    r = 1
    for i in range(1,n+1):
       r = r * i
    return r

def xmain():
    return 0
    
def main():
    f = fac(N)
    d('factorial(%i)=%i' %(N, f))
    #s = digitsum(f)
    s = sum([int(i) for i in str(f)])
    print(s)
    
if  __name__ =='__main__':main()
