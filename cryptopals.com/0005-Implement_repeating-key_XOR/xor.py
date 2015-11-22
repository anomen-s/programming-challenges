#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
Encrypt a bunch of stuff using your repeating-key XOR function. 
Encrypt your mail. 
Encrypt your password file. Your .sig file. 
Get a feel for it. 
I promise, we aren't wasting your time with this.
'''

import base64
import itertools
import sys


def xorBytes(s1, val):
    '''
      XOR bytes sequence with password
    '''
    nums = [(c1 ^ c2) for (c1, c2) in zip(s1, itertools.cycle(val))]
    asBytes = bytes(nums)
    return asBytes

    
    
def main():
    if len(sys.argv) != 3:
      print("Usage: %s [key] [inputtext]" % sys.argv[0])
      exit(1)
    (key, data) = (sys.argv[1], sys.argv[2])
     
    rawInput = bytes(data, 'utf-8')
    rawKey = bytes(key, 'utf-8')
    
    xorEnc = xorBytes(rawInput, rawKey)
    print("In:  " + str(base64.b16encode(rawInput),'utf-8'))
    print("Key: " + str(base64.b16encode(rawKey)*((len(data)+len(key)-1)//len(key)),'utf-8'))
    print("Out: " + str(base64.b16encode(xorEnc),'utf-8').lower())
    
if  __name__ =='__main__':
  main()

