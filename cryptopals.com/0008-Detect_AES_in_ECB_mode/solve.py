#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
The Base64-encoded content in this file has been encrypted via AES-128 in ECB mode under the key 
"YELLOW SUBMARINE".

(case-sensitive, without the quotes; exactly 16 characters; I like "YELLOW SUBMARINE" because it's exactly 16 bytes long, and now you do too). 

Decrypt it. You know the key, after all. 

Easiest way: use OpenSSL::Cipher and give it AES-128-ECB as the cipher.
 
'''

import sys

sys.path.append("../toolbox")
import tools

from Crypto.Cipher import AES


F='8.txt'

def getDuplicateBlocks(data, blockSize):
      blocks=tools.split(data, blockSize)
      
      dupes = set()
      blset = set()
      cnt = 0
      for bl in blocks:
        if bl in blset:
          cnt += 1
        blset.add(bl)

      if cnt:
        return (cnt, dupes)
      else:
        return None

def main():
    with open(F,'r') as f:
      encList = f.readlines()
    
    for (idx,encHex) in enumerate(encList, 1):
#      print(['*' * 16, idx, '*'*16])
      enc = tools.fromHex(encHex.strip())
      
      dupes = tools.getDuplicateBlocks(enc, 16)
      if dupes:
        print('Found on line #%i' % idx)
        print(dupes)
        print(tools.toHex(enc, blockSize=16))


if __name__ =='__main__':
  tools.run(main)

