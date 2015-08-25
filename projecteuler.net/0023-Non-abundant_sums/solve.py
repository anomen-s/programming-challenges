#!/usr/bin/python3
# -*- coding: utf-8 -*-

TOP = 28123 + 1
#TOP= 180

DEBUG = True
def d(args):
    global DEBUG
    if DEBUG:
      print(args)


def factors(N):
  f = set()
  i = 3
  while ((N % 2) == 0) and (N > 1):
      N = N / 2
      f.add(2)

  while N > 1:
    if (N % i) == 0:
      N = N / i
      f.add(i)
    else:
      i = i + 2
  return f


def divisors(N):
    f = list(factors(N))
    if len(f) > 0:
      result = set(divisorsIt(1, f, N))
      result.add(1)
      return result
    return set()

def divisorsIt(curr, f, N):
    f0 = f[0]
    f_rest = f[1:]
    fn = 1
    while (curr*fn) < N:
      cf = (curr*fn)
      if fn > 1 and N % cf == 0:
        yield cf
      if len(f_rest) > 0:
        for x in divisorsIt((curr*fn), f_rest, N): 
          yield x
      fn = fn * f0

def main():
    divTable = list(range(TOP))
    for n in range(TOP):
      dl=list(divisors(n))
      sdl = sum(dl)
      if n == sdl:
        divTable[n] = ['P', n,sum(dl)]
      elif n < sdl:
        divTable[n] = ['A', n,sum(dl)]
      elif n > sdl:
        divTable[n] = ['D', n,sum(dl)]
#        print (['N=',n, sdl, dl])
#        print (dl)
#        print
#    for x in divTable: d(x)

    d('divisors computed')

    sumsTable = list(range(TOP))
    for s1 in range(1, TOP):
      if divTable[s1][0] == 'A':
        for s2 in range(1, TOP-s1):
          if divTable[s2][0] == 'A':
            sumsTable[s1+s2] = 0
         
         
    print(sum(sumsTable))
   

    
if  __name__ =='__main__':main()
