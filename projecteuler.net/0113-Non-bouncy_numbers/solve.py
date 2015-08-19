#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
Working from left-to-right if no digit is exceeded by the digit to its left it is called an increasing number; for example, 134468.

Similarly if no digit is exceeded by the digit to its right it is called a decreasing number; for example, 66420.

We shall call a positive integer that is neither increasing nor decreasing a "bouncy" number; for example, 155349.

Clearly there cannot be any bouncy numbers below one-hundred, but just over half of the numbers below one-thousand (525) are bouncy. 
In fact, the least number for which the proportion of bouncy numbers first reaches 50% is 538.

As n increases, the proportion of bouncy numbers below n increases such that 
there are only 12951 numbers below one-million that are not bouncy and only 277032 non-bouncy numbers below 10**10.

How many numbers below a googol (10**100) are not bouncy?

Notes:
* compute number of constant numbers
* use table [L][10] to compute increasing numbers
* use table [L][10] to compute decreasing numbers
* result = inc + dec - const

'''

LEN = 100
#LEN=10 # 277032
#LEN=6 # 12951
#LEN=3  # 474
#LEN=2 # 99

def computeInc(tab):
   for d in range(10):
      tab[0][d] = 1

   for l in range(1,LEN):
     for d in range(10):
      s = 0
      for i in range(d+1):
         s = s + tab[l-1][i]
      tab[l][d] = s

def removeZeroes(incTab):
    for i in range(LEN):
      incTab[i][0] = 0
    
def computeDec(tab):
   for d in range(10):
      tab[0][d] = 1

   for l in range(1,LEN):
     for d in range(10):
      s = 0
      for i in range(d, 10):
         s = s + tab[l-1][i]
      tab[l][d] = s

def tableSum(tab):
    s = 0
    for i in range(LEN):
      s = s + sum(tab[i])
    return s
    
def main():
    incTab = [[0 for y in range(10)] for x in range(LEN)]
    decTab = [[0 for y in range(10)] for x in range(LEN)]
    computeInc(incTab)
    removeZeroes(incTab)
    computeDec(decTab)
    removeZeroes(decTab)
    for r in incTab:print(r)
    print('-')
    for r in decTab:print(r)
    si = tableSum(incTab)
    sd = tableSum(decTab)
    md = 9 * (LEN)
    print('%i + %i - %i = %i' % (si, sd, md, si+sd-md))
    

if  __name__ =='__main__':main()
