#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''

The Hamjet takes off at an angle of θ degrees up and a speed of V meters per second.
V is a fixed value that is determined by the awesome power of the Hamjet engine and the capacity of its fuel tank.
The destination is D meters away. 
Your job is to program the Hamjet's computer to calculate θ given V and D.

Sample:
<sample.txt>

Output:
Case #1: 45.0000000
Case #2: 15.0000000
Case #3: 3.8870928

Solution:

b = v*sin(theta) # speed up
a = v*cos(theta) # speed forward

b = tTOP * g # time to reach zero speed upwards (top point)
tTOP = v/g * sin(theta)

d = 2 * tTOP * a # forward distance

d = 2 * v/g * sin(theta) * v * cos(theta)

d = 2*v*v/g * sin(theta) * cos(theta)

## sin(x)*cos(y) = 1/2*(sin(x-y) + sin(x+y))  # magic formula ...
## sin(x)*cos(x) = 1/2*sin(2*x) # ... gives

d = v*v/g * sin(2*theta)
2*theta = asin(d*g/v**2)
theta = asin(d*g/v**2)/2
'''

import sys
import math


g = 9.8  # m*s**-2

def main():
    if len(sys.argv) < 2:
      print("missing filename")
      exit(1)
    with open(sys.argv[1],'r') as f:
      lines = [x.strip() for x in f.readlines()]
    
    line = iter(lines)
    testcases = int(next(line));
    
    for t in range(1,testcases+1):
      v,d = [float(x) for x in next(line).split()]
      
      a = d*g/(v**2)
      # fix rounding error
      if 1 < a < 1+10e-8:
        a = 1.0
      theta = math.asin(a)/2
      thetaDeg = theta * 180 / math.pi
      
      print('case #%i: %f' % (t, thetaDeg))
     

if  __name__ =='__main__':
  main()


