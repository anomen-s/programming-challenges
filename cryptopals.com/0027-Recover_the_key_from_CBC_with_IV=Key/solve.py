#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
Take your code from the CBC exercise and modify it so that it repurposes the key for CBC encryption as the IV. 

 Applications sometimes use the key as an IV on the auspices that both the sender and the receiver have to know the key already, and can save some space by using it as both a key and an IV. 

 Using the key as an IV is insecure; an attacker that can modify ciphertext in flight can get the receiver to decrypt a value that will reveal the key. 

 The CBC code from exercise 16 encrypts a URL string. Verify each byte of the plaintext for ASCII compliance (ie, look for high-ASCII values). Noncompliant messages should raise an exception or return an error that includes the decrypted plaintext (this happens all the time in real systems, for what it's worth). 

 Use your code to encrypt a message that is at least 3 blocks long: 
AES-CBC(P_1, P_2, P_3) -> C_1, C_2, C_3

 Modify the message (you are now the attacker): 
C_1, C_2, C_3 -> C_1, 0, C_1

 Decrypt the message (you are now the receiver) and raise the appropriate error if high-ASCII is found. 

 As the attacker, recovering the plaintext from the error, extract the key: 
P'_1 XOR P'_3
 
'''

import sys

sys.path.append("../toolbox")
import tools
import crypto

HEADER=b"comment1=cooking%20MCs;userdata="
TRAILER=b";comment2=%20like%20a%20pound%20of%20bacon"

def envelope(data):
    
    data = data.replace(b'%', b'%25')
    data = data.replace(b';', b'%3b')
    data = data.replace(b'=', b'%3d')

    data = HEADER + data + TRAILER
    
    return data

def attack(data):
    
    c1 = data[0:16]
    zeroes = b'\000'*16
    rest = data[48:]
    return c1 + zeroes + c1 + rest

def extractKey(message):
    blocks = tools.split(message, 16)

    iv = crypto.xor(blocks[0], blocks[2])
    return iv
 
def validityCheck(data):

    nonascii = [1 for c in data if ((c&0x80) >0)]
    return len(nonascii) == 0


def main():
    print("*** Alice")
    key = crypto.genKey()
    print(['key', tools.toHex(key)])
    #message = envelope(b"this is a regular message")
    message = envelope(b"something long enough")
    print([len(message), message])
    cipherMsg = crypto.encryptCBC(key, message, key)
    #print(cipherMsg)

    #decMsg=decryptCBC(key, cipherMsg)
    #print(decMsg)

    print("*** Mitm")
    receivedMsg = attack(cipherMsg)
      
    #print(receivedMsg)

    print("*** Bob")
    decMsg=crypto.decryptCBC(key, receivedMsg, key)
    if not validityCheck(decMsg):

      print(["Invalid URL: ", decMsg ])
      print("*** Mitm")
      print(['extracted', tools.toHex(extractKey(decMsg))])
    else:
      print("URL OK")



if __name__ =='__main__':
  tools.run(main)
