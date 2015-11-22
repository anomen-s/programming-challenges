#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
Here is the opening stanza of an important work of the English language: 
Burning 'em, if you ain't quick and nimble
I go crazy when I hear a cymbal

 Encrypt it, under the key "ICE", using repeating-key XOR. 

 In repeating-key XOR, you'll sequentially apply each byte of the key; the first byte of plaintext will be XOR'd against I, the next C, the next E, then I again for the 4th byte, and so on. 

It should come out to: 
0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272
a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f

Encrypt a bunch of stuff using your repeating-key XOR function. 
Encrypt your mail. 
Encrypt your password file. Your .sig file. 
Get a feel for it. 
I promise, we aren't wasting your time with this.
'''

import time
import base64
import itertools

DEBUG = True

STR = ["Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"]

KEY = "ICE"


def xorBytes(s1, val):
    '''
      XOR bytes sequence with password
    '''
    nums = [(c1 ^ c2) for (c1, c2) in zip(s1, itertools.cycle(val))]
    asBytes = bytes(nums)
    return asBytes

    
    
def main():
    for S in STR:
     rawInput = bytes(S, 'utf-8')
     rawKey = bytes(KEY, 'utf-8')
    
     xorEnc = xorBytes(rawInput, rawKey)
     print("In:  " + str(base64.b16encode(rawInput),'utf-8'))
     print("Out: " + str(base64.b16encode(xorEnc),'utf-8').lower())
     
     print("Exp: " + "0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f")
     print("Key: " + str(base64.b16encode(rawKey)*25,'utf-8'))
#    print (str(xorEnc, 'utf-8'))
    

def d(args):
    global DEBUG
    if DEBUG:
      print(args)

if  __name__ =='__main__':
  tStart = time.time()
  main()
  print(['time[ms]',int((time.time() - tStart)*1000)])

