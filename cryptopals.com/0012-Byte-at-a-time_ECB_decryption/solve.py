#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
Copy your oracle function to a new function that encrypts buffers under ECB mode using a consistent but unknown key (for instance, assign a single random key, once, to a global variable). 

Now take that same function and have it append to the plaintext, BEFORE ENCRYPTING, the following string: 

<12.txt>


Base64 decode the string before appending it. Do not base64 decode the string by hand; make your code do it. The point is that you don't know its contents. 

What you have now is a function that produces: 
AES-128-ECB(your-string || unknown-string, random-key)

It turns out: you can decrypt "unknown-string" with repeated calls to the oracle function! 

Here's roughly how: 
1. Feed identical bytes of your-string to the function 1 at a time --- start with 1 byte ("A"), then "AA", then "AAA" and so on. Discover the block size of the cipher. You know it, but do this step anyway. 
2. Detect that the function is using ECB. You already know, but do this step anyways. 
3. Knowing the block size, craft an input block that is exactly 1 byte short (for instance, if the block size is 8 bytes, make "AAAAAAA"). Think about what the oracle function is going to put in that last byte position. 
4 Make a dictionary of every possible last byte by feeding different strings to the oracle; for instance, "AAAAAAAA", "AAAAAAAB", "AAAAAAAC", remembering the first block of each invocation. 
5. Match the output of the one-byte-short input to one of the entries in your dictionary. You've now discovered the first byte of unknown-string. 
6. Repeat for the next byte.

This is the first challenge we've given you whose solution will break real crypto.
Lots of people know that when you encrypt something in ECB mode, you can see penguins through it.
Not so many of them can decrypt the contents of those ciphertexts, and now you can.
If our experience is any guideline, this attack will get you code execution in security tests about once a year.
'''

import sys

sys.path.append("../toolbox")
import tools
import crypto


########################################################
###    Crypto function                               ###
########################################################
def _loadUnknownText():
    with open('12.txt','r') as f:
      b64text = f.read()

    return tools.fromB64(b64text)


_SECRET_KEY = crypto.genKey(16)
_UNK = _loadUnknownText()

def ecbOracle(prefix):
    data = prefix + _UNK
    cipherMsg = crypto.encryptECB(_SECRET_KEY, data)
    return cipherMsg
########################################################
########################################################
########################################################


def encryptBlocks(encOracle, partialBlock):
     '''
       Encrypt partial block with all possible values of last byte 
       and return dictionary mnapping: <encryptedBlock> -> <lastByte>
     '''
     idx = len(partialBlock)
     result = {}
     block = bytearray(partialBlock)
     block.append(0)
     for i in range(256):
       block[idx] = i
       curr = bytes(block)
       enc = encOracle(curr)
       result[enc[:idx+1]] = i
     return result

def getBlockLength(encOracle):
    enc = encOracle(b'A'* 64)
    for bl in [8,16,32]:
       if enc[0:bl] == enc[bl:2*bl]:
         return bl
    return 0
    

def getPlaintextLength(encOracle):
    cipherLen = len(encOracle(b''))
    for i in range(1, 64):
      pad = b'X' * i
      l = len(encOracle(pad));
      if l > cipherLen:
        return cipherLen - i
        


def getBlock(data, idx, blockSize):
     blockNum = idx // blockSize
     start = blockNum * blockSize
     return data[start : start + blockSize]

def crack(oracle):
     # get block size
     BLOCK_SIZE = getBlockLength(oracle)
     # get plaintext size (without padding)
     PLAINTEXT_LEN = getPlaintextLength(oracle)
     
     if not BLOCK_SIZE:
       raise Exception("couldn't determine block size")
     
     # add prefix to simplify handling
     result = bytearray(b' '*(BLOCK_SIZE-1))
     for i in range(PLAINTEXT_LEN):

       # use oracle with prefix of size BLOCKSIZE- 1 - number of decoded bytes
       enc = oracle(b' ' * ((BLOCK_SIZE-1-i)%BLOCK_SIZE))

       # cut out correct block from cipher text
       encBlock = getBlock(enc, i, BLOCK_SIZE)

       # try to encrypt prefix with all combinations of last byte
       prefix = bytes(result[-BLOCK_SIZE+1:])
       encMap = encryptBlocks(oracle, prefix)
       if not encBlock in encMap:
         raise Exception("decryption failed. so far: \n" + tools.toStr(result[BLOCK_SIZE-1:]))
       # next decrypted byte found
       decByte = encMap[encBlock]
       result.append(decByte)
       tools.d(['%i/%i l=%i'%(i,PLAINTEXT_LEN, len(enc)), decByte, chr(decByte)])
     
     return result[BLOCK_SIZE-1:]
    
def main():
    tools.setDebug(False)

    dec = crack(ecbOracle)
    
    print(tools.toStr(dec))
    
    

if __name__ =='__main__':
  tools.run(main)
