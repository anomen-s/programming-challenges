#!/usr/bin/python3
# -*- coding: utf-8 -*-


# An irrational decimal fraction is created by concatenating the positive integers:
#
# 0.123456789101112131415161718192021...
#
# It can be seen that the 12th digit of the fractional part is 1.
#
#If dn represents the nth digit of the fractional part, find the value of the following expression.
#
# d1 × d10 × d100 × d1000 × d10000 × d100000 × d1000000

def getDigit(n):
   # skip shorter numbers
   nlen = 1
   nsum = 0
   while True:
    csum = nlen * (10**nlen - 10**(nlen-1))
    if nsum + csum >= n:
      break
    nsum = nsum + csum
    nlen = nlen + 1

   # get number (relative in block of numbers of length nlen)
   rpos = n - nsum - 1
   rnum = rpos // nlen
   rdigit = rpos % nlen
   
   # get correct digit
   number = 10**(nlen-1)  + rnum
   digit = nlen - rdigit - 1
#   print(['n',n,'rpos',rpos,'rnum',rnum,'rdigit',rdigit,'number',number])
   while digit > 0:
     number = number // 10
     digit = digit-1
   return number % 10
     
   


def main():

    pos = [10**x for x in range(7)]
    
    values = map(getDigit, pos)
    print (values)
    res = 1
    for v in values:
     res = res * v
    print(res)

def xmain():
    print(''.join([str(getDigit(n)) for n in range(1,200)]))
    
if  __name__ =='__main__':main()
