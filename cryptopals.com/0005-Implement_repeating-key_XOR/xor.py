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

sys.path.append("../toolbox")
import tools
import xorcrypto


def main():
    if len(sys.argv) != 3:
      print("Usage: %s [key] [inputtext]" % sys.argv[0])
      exit(1)
    (key, data) = (sys.argv[1], sys.argv[2])
     
    rawInput = bytes(data, 'utf-8')
    rawKey = bytes(key, 'utf-8')
    
    xorEnc = xorcrypto.xor(rawInput, rawKey)
    print("In:  " + tools.toHex(rawInput))
    print("Key: " + tools.toHex(rawKey*((len(data)+len(key)-1)//len(key))))
    print("Out: " + tools.toHex(xorEnc,0,False))
    
if  __name__ =='__main__':
  main()

