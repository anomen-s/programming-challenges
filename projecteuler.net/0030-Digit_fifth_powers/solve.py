#!/usr/bin/python3
# -*- coding: utf-8 -*-


# cannot have 7 digits, because 7*(9**5) has only 6 digits
TOP=6*(9**5)

DEBUG = True
def d(args):
    global DEBUG
    if DEBUG:
      print(args)


def pow5sum(n):
    fs = 0
    while n > 0:
      r = n % 10
      n = n // 10
      fs = fs + (r**5)
    return fs

def main():
  s = 0
  for i in range(10, TOP):
    fs = pow5sum(i)
    if i == fs: 
      s = s + i
      print(i)


  print(['sum',s])

if  __name__ =='__main__':main()
