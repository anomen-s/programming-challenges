#!/usr/bin/python
# -*- coding: utf-8 -*-

#2**15 = 32768 and the sum of its digits is 3 + 2 + 7 + 6 + 8 = 26.

# What is the sum of the digits of the number 2**1000?

num = [-10 for i in range(400)]
num[0] = 1
for Index in range(1000):

  carry = 0
  for n in range(len(num)):
    if num[n] == -10 and carry == 0:
       break
    if num[n] == -10:
       num[n] = 1
       carry = 0
       break
    t = 2*num[n]+carry
    if t > 9:
      t = t - 10
      carry = 1
    else:
      carry = 0
    num[n] = t

num = list(map(lambda x: max(0,x), num))

print(num)
print(sum(num))
