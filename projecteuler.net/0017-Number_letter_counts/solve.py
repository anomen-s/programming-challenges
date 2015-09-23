#!/usr/bin/python3
# -*- coding: utf-8 -*-

def loadNumbers():
  with open('numbers.txt', 'r') as f:
    lines = f.readlines() # read all lines from file
  result = {}
  for l in lines:
    (num, name) = l.split()
    result[int(num)] = name
  return result

def fixNumbers(nums):
  for i in range(1,100):
    if not i in nums:
      tens = (i // 10)*10
      ones = i % 10
      nums[i] = nums[tens]+nums[ones]


def fixHundreds(nums):
    num100 = nums[100]
    for cent in range(1,10):
      c = nums[cent] + num100
      nums[cent*100] = c
      for n in range(1,100):
        nums[cent*100 + n] = c+'and'+nums[n]
  
def sumNumbers(nums):
    s = 0
    for i in range(1,1001):
      s = s + len(nums[i])
    return s

def main():

  nums = loadNumbers()
  fixNumbers(nums)
  fixHundreds(nums)
#  S = 10 * s0 + lenHundreds(nums) + len(nums[1] + nums[1000])
  print(nums)
  s = sumNumbers(nums)
  print(s)
  

if  __name__ =='__main__':main()
