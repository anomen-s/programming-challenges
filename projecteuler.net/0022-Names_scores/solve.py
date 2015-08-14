#!/usr/bin/python2
# -*- coding: utf-8 -*-


DEBUG = True
def d(args):
    global DEBUG
    if DEBUG:
      print(args)

def nameSum(name):
    s = 0
    for c in name.upper():
       s = s + (ord(c) - ord('A')  + 1)
    return s

def readfile():
  with open('p022_names.txt', 'r') as f:
    lines = f.readlines() # read all lines from file

  nameLine = lines[0].strip()
  names = nameLine.split(',')
  names = [n[1:-1] for n in names]
  d(names)
  return names

def main():
  names = readfile()
  names.sort()
  i = 1
  s = 0
  for n in names:
    d('%i: %s = %i' % (i, n, nameSum(n)))
    s = s + i * nameSum(n)
    i = i + 1

  print(s)
  
if  __name__ =='__main__':main()
