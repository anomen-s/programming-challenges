#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
Detect single-character XOR

One of the 60-character strings in this file has been encrypted by single-character XOR. 

Find it.
'''

import time
import base64

DEBUG = True


def decodeHex(s):
    '''
      Convert hex string to bytes
    '''
    return bytes.fromhex(s)
    

def xorBytes(s1, val):
    '''
      XOR bytes sequence with constant value val
    '''
    nums = [(c ^ val) for c in s1]
    asBytes = bytes(nums)
    return asBytes


def initScoreTab():
   T = [0 for x in range(256)]
   for (p,c) in enumerate('ETAOIN SHRDLU CMFYWGPBVKXQJZ'[::-1]):
     T[ord(c)] = p
     T[ord(c.lower())] = p
   return T
  

T = initScoreTab()

def score(s):
    return sum([T[c] for c in s])
    
    
def main():
    res = []
    with open('4.txt','r') as f:
      for line in f.readlines():
        enc = decodeHex(line.strip())
        dec = [[score(xorBytes(enc, i)),i,xorBytes(enc, i)] for i in range(256)]
        res.extend(dec)
    res = sorted(res)
    for x in res: print(x)


def d(args):
    global DEBUG
    if DEBUG:
      print(args)

if  __name__ =='__main__':
  tStart = time.time()
  main()
  print(['time[ms]',int((time.time() - tStart)*1000)])

