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

KEY=b"YELLOW SUBMARINE"

F='7.txt'

def main():
    with open(F,'r') as f:
      b64 = f.read()
      enc = tools.fromB64(b64)
    
    cipher=AES.new(KEY, AES.MODE_ECB)
    dec = cipher.decrypt(enc)
    print(tools.stripPadding(dec))

if __name__ =='__main__':
  tools.run(main)

