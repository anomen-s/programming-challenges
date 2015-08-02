#!/usr/bin/python3
# -*- coding: utf-8 -*-

import gmpy2

DEBUG = False

LOOPS=50
MAX=10000+100

def d(args):
    global DEBUG
    if DEBUG:
      print(args)

def revAdd(num, check):
    n = num
    rev = 0
    while n > 0:
      rev = (rev * 10) + (n % 10)
      n = n // 10
    if check and (num == rev):
      d('paindrome %i'% num)
      # palindrome
      return -1

    return num + rev

def isLychrel(n, loops):
    num = n
    c = False
    for i in range(loops):
      num = revAdd(num, c)
      c = True
      d('res:' + str(num))
      if num == -1:
        return False
    return revAdd(num, True) != -1


def xmain():
    print(isLychrel(10677, 50))
    
    
def main():
    global LOOPS
    global MAX
    SUM = 0
    
    for i in range(MAX):
      if isLychrel(i, LOOPS):
        SUM = SUM + 1
        print('found[%i] %i' % (SUM, i))
        
    print('result %i' % (SUM))
    return SUM


if  __name__ =='__main__':main()
