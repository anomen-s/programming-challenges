#!/usr/bin/env python3

def isDiv(a0, b0):
   a = max(a0, b0)
   b = min(a0, b0)
   if (a % b) == 0:
     return a // b
   return None
     
def selDiv(nums):
  if len(nums) < 2:
    return None
  n0 = nums[0]
  nrest = nums[1:]
  for n in nrest:
    d = isDiv(n0, n)
    if d:
      return d
  return selDiv(nrest)


with open('input', 'r') as f:
   data = f.readlines()
   data = [[int(d) for d in l.split()] for l in data]
   sums = [selDiv(l) for l in data]
   print(sum(sums))
