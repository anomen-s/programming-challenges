#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
Find a SHA-1 implementation in the language you code in. 
Don't cheat. It won't work.
Do not use the SHA-1 implementation your language already provides (for instance, don't use the "Digest" library in Ruby, or call OpenSSL; in Ruby, you'd want a pure-Ruby SHA-1). 

Write a function to authenticate a message under a secret key by using a secret-prefix MAC, which is simply: 
SHA1(key || message)

Verify that you cannot tamper with the message without breaking the MAC you've produced, and that you can't produce a new MAC without knowing the secret key.

'''

import sys
from Crypto.Hash import SHA

sys.path.append("../toolbox")
import tools
import crypto
import sha1


def _native_sha1mac(key, data):
 h = SHA.new()
 h.update(key)
 h.update(data)
 return h.hexdigest()

def sha1mac(key, data):
  return sha1.hexdigest(key+data)

def main():
    
    print('some hashes: ')
    print(sha1mac(b'A'*16, b'sampleText'))
    print(sha1mac(b'A'*15 + b'B', b'sampleText'))
    print(sha1mac(b'A'*16, b'sampleTextLonger'))

if __name__ =='__main__':
  tools.run(main)

