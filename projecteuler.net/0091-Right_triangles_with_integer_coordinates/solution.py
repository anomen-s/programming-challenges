#!/usr/bin/python3
# -*- coding: utf-8 -*-

import gmpy2

def main():
  print (solve(50))

def computeRight(x,y, MAX):
  # find how many. how many points on line O-P are ints?
  # then project them from P to Q until reaching MAX x
 
#(2,3) -> each 3 righ -> (2+3,3-2), (2+2*3,3-2*2)
#(4,6) -> [gcd] (2,3) -> each 3 right
#(2,2) -> gcd - 1,1 -> each 1 right/down -> (1+1, 1-1), inv(1+2*1, 1-2*1), ..
#(3,2) -> each 3 down - inv(3+2,2-3), inv(3+2*2, 2-2*3)
#(6,4) -> gcd (3,2)each 3 down - (6+2,4-3), inv(6+2*2,4-2*3),

    # direction to go on second side
    dx = y
    dy = x
    gcd = int(gmpy2.gcd(x,y))
    if gcd > 1:
       dx = dx // gcd
       dy = dy // gcd

    sx = (MAX - x) // dx
    sy = y // dy
    return min(sx, sy)


def solve(MAX):
  # right angle at O:
  # for all P in 1..MAX and Q in 1..MAX
  R0 = MAX*MAX

  # right angle at P(0,y):
  RP0 = (MAX)*(MAX)

  RP1 = 0
  # right angle at P(x,y):
  for x in range(1, MAX+1):
   for y in range(1, MAX+1):
     rr = computeRight(x, y, MAX)
     #print("%i,%i = %i"%(x,y,rr))
     RP1 = RP1 + rr

  print ("%i + 2 * (%i + %i)" % (R0, RP0, RP1))

  # mul 2 to have symmetrical cases
  RESULT = R0 + 2 * (RP0 + RP1)
  return RESULT


if  __name__ =='__main__':main()
