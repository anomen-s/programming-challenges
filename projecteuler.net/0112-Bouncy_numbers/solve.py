#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
Working from left-to-right if no digit is exceeded by the digit to its left it is called an increasing number; for example, 134468.

Similarly if no digit is exceeded by the digit to its right it is called a decreasing number; for example, 66420.

We shall call a positive integer that is neither increasing nor decreasing a "bouncy" number; for example, 155349.

Clearly there cannot be any bouncy numbers below one-hundred, but just over half of the numbers below one-thousand (525) are bouncy. In fact, the least number for which the proportion of bouncy numbers first reaches 50% is 538.

Surprisingly, bouncy numbers become more and more common and by the time we reach 21780 the proportion of bouncy numbers is equal to 90%.

Find the least number for which the proportion of bouncy numbers is exactly 99%.
'''

def isBouncy(n):
   last = n % 10
   n = n // 10 
   dec = False
   inc = False
   while n > 0:
     d = n % 10
     n = n // 10
     if d > last: inc = True
     if d < last: dec = True
     if dec and inc: return True
     last = d
   return False

   

R = .99
#R = .9
#R = .5

def main():
   bc = 0
   n = 0
   rate = 0
   while rate < R:
     n = n + 1
     if isBouncy(n):
       bc = bc + 1
     rate = bc / n
   print('%i: %i/%i = %s' %(n, bc, n, rate))

if  __name__ =='__main__':main()
