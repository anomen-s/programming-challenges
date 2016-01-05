#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
Secret-prefix SHA-1 MACs are trivially breakable. 

The attack on secret-prefix SHA1 relies on the fact that you can take the ouput of SHA-1 and use it as a new starting point for SHA-1, thus taking an arbitrary SHA-1 hash and "feeding it more data". 

Since the key precedes the data in secret-prefix, any additional data you feed the SHA-1 hash in this fashion will appear to have been hashed with the secret key. 

To carry out the attack, you'll need to account for the fact that SHA-1 is "padded" with the bit-length of the message; your forged message will need to include that padding. 
We call this "glue padding". The final message you actually forge will be: 

SHA1(key || original-message || glue-padding || new-message)

(where the final padding on the whole constructed message is implied) 

Note that to generate the glue padding, you'll need to know the original bit length of the message; the message itself is known to the attacker, but the secret key isn't, so you'll need to guess at it. 

This sounds more complicated than it is in practice. 

To implement the attack, first write the function that computes the MD padding of an arbitrary message and verify that you're generating the same padding that your SHA-1 implementation is using.
This should take you 5-10 minutes. 

Now, take the SHA-1 secret-prefix MAC of the message you want to forge --- this is just a SHA-1 hash --- and break it into 32 bit SHA-1 registers (SHA-1 calls them "a", "b", "c", &c). 

Modify your SHA-1 implementation so that callers can pass in new values for "a", "b", "c" &c (they normally start at magic numbers).
With the registers "fixated", hash the additional data you want to forge. 

Using this attack, generate a secret-prefix MAC under a secret key (choose a random word from /usr/share/dict/words or something) of the string: 
"comment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon"

 Forge a variant of this message that ends with ";admin=true".

'''

import sys
import struct
import hashlib

sys.path.append("../toolbox")
import tools
import sha1

MESSAGE = b"comment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon"

_KEY = b'secret-word'

def sha1mac(data):
 h =  hashlib.sha1()
 h.update(_KEY)
 h.update(data)
 tools.d(['sign data:', _KEY, data])
 #tools.writefile('debug.out', _KEY + data)
 digest = h.digest()
 return struct.unpack('>5I', digest)

def verify_sha1mac(data, digest):

 tools.d(['verify data', data])
 tools.d(['verify digest', digest])
 printsha1(digest)
 d = sha1mac(data)
 tools.d(['exp digest', d])
 printsha1(d)
 return digest == d


def printsha1(h):
    tools.d(sha1.toStr(h))

def checkAdmin(data):
 return b";admin=true" in data


def attackMessage(keylen, msg, msgHash):

    injectedData = b";admin=true"
    msgBlocks = sha1.buildBlocks(0,b'X'*keylen + msg)
    prevLen = ((keylen + len(msg) + 1 + 8 + sha1.BLOCK_LEN-1) // sha1.BLOCK_LEN) * (sha1.BLOCK_LEN)
    blocks = sha1.buildBlocks(prevLen, injectedData)

    aMessage = b''.join(msgBlocks) + injectedData
    tools.d(['attack: append blocks', blocks])
    for block in blocks:
      msgHash = sha1.compute_sha1block(msgHash, block)
      printsha1(msgHash)
    return (aMessage[keylen:], msgHash)


def main():
    baseMessageHash = sha1mac(MESSAGE)
    printsha1(baseMessageHash)

     ### FIXME?: NEED TO KNOW LENGTH OF _KEY
     ### GUESS?
    (aMessage, aHash) = attackMessage(len(_KEY), MESSAGE, baseMessageHash)

    if not verify_sha1mac(aMessage, aHash):
      print("Invalid hash")
      return
    
    if checkAdmin(aMessage):
      print("You are ADMIN")
    else:
      print("You are regular user")
    

if __name__ =='__main__':
  tools.run(main, True)

