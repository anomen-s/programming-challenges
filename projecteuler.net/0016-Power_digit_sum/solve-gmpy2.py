#!/usr/bin/python
# -*- coding: utf-8 -*-

#2**15 = 32768 and the sum of its digits is 3 + 2 + 7 + 6 + 8 = 26.

# What is the sum of the digits of the number 2**1000?

from gmpy2 import *
from functools import reduce

r = mpz(2**0)

for i in range(1000):

  r=mul(r,2)

  
print(r.digits())
print(reduce(lambda x,y:x+int(y), r.digits(), 0))

