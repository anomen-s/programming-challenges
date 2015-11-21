#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
The hex encoded string: 
1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736

 ... has been XOR'd against a single character. Find the key, decrypt the message. 

 You can do this by hand. But don't: write code to do it for you. 

 How? Devise some method for "scoring" a piece of English plaintext. Character frequency is a good metric. Evaluate each output and choose the one with the best score.
'''

import time
import base64

DEBUG = True


STR = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"

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
    enc = decodeHex(STR)
    
    res = [[score(xorBytes(enc, i)),i,xorBytes(enc, i)] for i in range(256)]
    res = sorted(res)
    for x in res: print(x)
#    for i in range(256):
#      dec = xorBytes(enc, i)
      
#      print([score(dec),dec])
    


def d(args):
    global DEBUG
    if DEBUG:
      print(args)

if  __name__ =='__main__':
  tStart = time.time()
  main()
  print(['time[ms]',int((time.time() - tStart)*1000)])

