#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
The hex encoded string: 
1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736

 ... has been XOR'd against a single character. Find the key, decrypt the message. 

 You can do this by hand. But don't: write code to do it for you. 

 How? Devise some method for "scoring" a piece of English plaintext. Character frequency is a good metric. Evaluate each output and choose the one with the best score.
'''

import sys

sys.path.append("../toolbox")
import tools
import crypto
import scoring


STR = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"

def main():
    enc = tools.fromHex(STR)
    
    res = [[scoring.compute(crypto.xor(enc, i)),i,crypto.xor(enc, i)] for i in range(256)]
    res = sorted(res)
    for x in res[:-1]:
      if x[0]>0: tools.d(x)
    print(res[-1])
#    for i in range(256):
#      dec = xorBytes(enc, i)
      
#      print([score(dec),dec])
    


if  __name__ =='__main__':
  tools.run(main)
