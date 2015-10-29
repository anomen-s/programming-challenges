#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
The following iterative sequence is defined for the set of positive integers:

n → n/2 (n is even)
n → 3n + 1 (n is odd)

Using the rule above and starting with 13, we generate the following sequence:
13 → 40 → 20 → 10 → 5 → 16 → 8 → 4 → 2 → 1

It can be seen that this sequence (starting at 13 and finishing at 1) contains 10 terms. 
Although it has not been proved yet (Collatz Problem), it is thought that all starting numbers finish at 1.

Which starting number, under one million, produces the longest chain?

NOTE: Once the chain starts the terms are allowed to go above one million.
'''
DEBUG = False

N=1000**2

def d(args):
    global DEBUG
    if DEBUG:
      print(args)


def gen(queue, chains):
    '''
      Compute length of all chains which have members less then N.
    '''
    while len(queue) > 0:
      i = queue.pop(0)
      d('testing %i'%i)
      ci = chains[i]
      i2 = i * 2
      if (i2 < N):
       if chains[i2] == 0:
         d('next i2 %i = %i'%(i2,ci+1))
         queue.append(i2)
         chains[i2] = ci + 1
       else:
         d('existing i2 %i = %i'%(i2,chains[i2]))
         chains[i2] = min(chains[i2], ci + 1)
         raise Exception('unexpected value for i2')
         
      if (i > 9) and ((i-1) % 3) == 0:
       i3 = (i-1)//3
       if (i3 & 1 == 1) and (chains[i3] == 0):
         d('next i3  %i = %i'%(i3, ci+1))
         queue.append(i3)
         chains[i3] = ci + 1
#       else:
#         d('existing i3 %i = %i'%(i3,chains[i3]))
#         chains[i3] = min(chains[i3], ci + 1)
#         raise Exception('unexpected value for i2')
         
def computeLength(start, chains):
    '''
     Compute length of C. sequence.
     Use precomputed values in 'chains' list to avoid useless repeated checks.
    '''
    n = start
    c = 0
    while n > 1:
        if n < N and chains[n] > 0:
          c = c + chains[n]
          return c
          
        if (n & 1) == 0:
          n = n//2
        else:
          n = 3*n+1
        c = c + 1
    raise Exception('didnt find match in table')

def findLongest(chains):
    '''
      Find biggest value in given list.
    '''
    maxv = max(chains)
    maxi = chains.index(maxv)
    return (maxv, maxi)
    
    
    
def main():
    chains = [0 for i in range(N)]
    chains[1] = 1
    # precompute all sequences with members <1M
    gen([1], chains)
    print('done <1M:')
    print(findLongest(chains))
    
    # compute sequences with members >1M
    for i in range(1,N):
      if chains[i] == 0:
       chains[i] = computeLength(i, chains)
    print('done all:')
    print(findLongest(chains))

    for i in range(20): d(chains[i*20:i*20+20])

if  __name__ =='__main__':main()
