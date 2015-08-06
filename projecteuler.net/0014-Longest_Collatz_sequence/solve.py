#!/usr/bin/python3
# -*- coding: utf-8 -*-

DEBUG = False

N=1000**2

def d(args):
    global DEBUG
    if DEBUG:
      print(args)


def gen(queue, chains):
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
    maxv = 0
    maxi = 0
    for i in range(1,len(chains)):
      if chains[i] > maxv:
        maxv = chains[i]
        maxi = i
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

    for i in range(20): print(chains[i*20:i*20+20])

if  __name__ =='__main__':main()
