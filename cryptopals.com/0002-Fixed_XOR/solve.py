#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
Write a function that takes two equal-length buffers and produces their XOR combination. 


 If your function works properly, then when you feed it the string: 
1c0111001f010100061a024b53535009181c

 ... after hex decoding, and when XOR'd against: 
686974207468652062756c6c277320657965

 ... should produce: 
746865206b696420646f6e277420706c6179
'''

import time
import base64

DEBUG = True


STR1 = "1c0111001f010100061a024b53535009181c"
STR2 = "686974207468652062756c6c277320657965"

def decodeHex(s):
    '''
      Convert hex string to bytes
    '''
    return bytes.fromhex(s)
    

def xorBytes(s1, s2):
    '''
      XOR two bytes sequences
    '''
    nums = [(c1 ^ c2) for (c1,c2) in zip(s1, s2)]
    asBytes = bytes(nums)
#    asStr = ''.join([chr(c) for c in nums])
#    print(asBytes)
    return asBytes

def main():
    h1 = decodeHex(STR1)
    h2 = decodeHex(STR2)
    asBytes = xorBytes(h1, h2)
    asHex = base64.b16encode(asBytes)
    print(asHex.decode('utf-8').lower())
    


def d(args):
    global DEBUG
    if DEBUG:
      print(args)

if  __name__ =='__main__':
  tStart = time.time()
  main()
  print(['time[ms]',int((time.time() - tStart)*1000)])

