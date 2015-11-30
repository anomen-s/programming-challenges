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

from Crypto import Random
from Crypto.Cipher import AES


F='10.txt'

def genKey(length=16):
 return Random.new().read(length)

def encryptCBC(key, data):
    data = tools.addPadding(data)
    blocks = tools.split(data, 16, False)

    iv = b'\000' * 16
    result = b''
    
    cipher=AES.new(key, AES.MODE_ECB)
    
    for block in blocks:
      inBlock = crypto.xor(block, iv)
      encBlock = cipher.encrypt(inBlock)
      iv = encBlock
      result += encBlock
    
    return result
    
def decryptCBC(key, data):
    encBlocks = tools.split(data, 16, False)

    iv = b'\000' * 16
    result = b''
    
    cipher=AES.new(key, AES.MODE_ECB)
    
    for block in encBlocks:
      decBlock = cipher.decrypt(block)
      dec = crypto.xor(decBlock, iv)
      iv = block
      result += dec
    return tools.stripPadding(result)

HEADER=b"comment1=cooking%20MCs;userdata="
TRAILER=b";comment2=%20like%20a%20pound%20of%20bacon"

def envelope(data):
    
    data = data.replace(b'%', b'%25')
    data = data.replace(b';', b'%3b')
    data = data.replace(b'=', b'%3d')

    data = HEADER + data + TRAILER
    
    return data

def attack(data):

    expectedText = HEADER[16:32]
    injected = b';admin=true;dat='
    b1 = data[0:16]
    b2 = data[16:32]
    
    newB1 = crypto.xor(expectedText, injected)
    newB1 = crypto.xor(newB1, b1)
    
    return newB1 + data[16:]

def adminCheck(data):
    adminStr = b";admin=true;"
    
    return (data.find(adminStr) >= 0)

    
def main():
    print("*** Alice")
    key = genKey()
    #print(key)
    message = envelope(b"this is normal message")
    print(message)
    cipherMsg = crypto.encryptCBC(key, message)
    #print(cipherMsg)

    #decMsg=decryptCBC(key, cipherMsg)
    #print(decMsg)

    print("*** Mitm")
    receivedMsg = attack(cipherMsg)
    #print(receivedMsg)

    print("*** Bob")
    decMsg=crypto.decryptCBC(key, receivedMsg)
    if adminCheck(decMsg):
      print("You are ADMIN")
    else:
      print("You are regular user")
    print(decMsg)


if __name__ =='__main__':
  tools.run(main)

