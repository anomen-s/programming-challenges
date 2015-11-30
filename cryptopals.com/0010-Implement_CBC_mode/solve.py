#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
CBC mode is a block cipher mode that allows us to encrypt irregularly-sized messages, despite the fact that a block cipher natively only transforms individual blocks. 

In CBC mode, each ciphertext block is added to the next plaintext block before the next call to the cipher core. 

The first plaintext block, which has no associated previous ciphertext block, is added to a "fake 0th ciphertext block" called the initialization vector, or IV. 

Implement CBC mode by hand by taking the ECB function you wrote earlier, making it encrypt instead of decrypt (verify this by decrypting whatever you encrypt to test), and using your XOR function from the previous exercise to combine them. 

The file here is intelligible (somewhat) when CBC decrypted against "YELLOW SUBMARINE" with an IV of all ASCII 0 (\x00\x00\x00 &c)
 
'''

import sys

sys.path.append("../toolbox")
import tools
import crypto

from Crypto.Cipher import AES

KEY=b"YELLOW SUBMARINE"
IV=b'\000' * 8

F='10.txt'

def main():
    with open(F,'r') as f:
      b64 = f.read()
      enc = tools.fromB64(b64)
    
    encBlocks = tools.split(enc, 16, False)

    iv = IV
    result = b''
    
    cipher=AES.new(KEY, AES.MODE_ECB)
    
    for block in encBlocks:
      decBlock = cipher.decrypt(block)
      dec = crypto.xor(decBlock, iv)
      iv = block
      result += dec
    
    print(tools.toStr(tools.stripPadding(result)))

if __name__ =='__main__':
  tools.run(main)

