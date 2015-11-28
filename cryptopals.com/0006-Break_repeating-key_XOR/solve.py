#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
It's been base64'd after being encrypted with repeating-key XOR. 

 Decrypt it. 

 Here's how: 
 Let KEYSIZE be the guessed length of the key; try values from 2 to (say) 40. 
 Write a function to compute the edit distance/Hamming distance between two strings. The Hamming distance is just the number of differing bits. The distance between: 
this is a test
 and 
wokka wokka!!!
 is 37. Make sure your code agrees before you proceed. 
 For each KEYSIZE, take the first KEYSIZE worth of bytes, and the second KEYSIZE worth of bytes, and find the edit distance between them. Normalize this result by dividing by KEYSIZE. 
 The KEYSIZE with the smallest normalized edit distance is probably the key. You could proceed perhaps with the smallest 2-3 KEYSIZE values. Or take 4 KEYSIZE blocks instead of 2 and average the distances. 
 Now that you probably know the KEYSIZE: break the ciphertext into blocks of KEYSIZE length. 
 Now transpose the blocks: make a block that is the first byte of every block, and a block that is the second byte of every block, and so on. 
 Solve each block as if it was single-character XOR. You already have code to do this. 
 For each block, the single-byte XOR key that produces the best looking histogram is the repeating-key XOR key byte for that block. Put them together and you have the key.

 
 This code is going to turn out to be surprisingly useful later on. Breaking repeating-key XOR ("Vigenere") statistically is obviously an academic exercise, a "Crypto 101" thing. But more people "know how" to break it than can actually break it, and a similar technique breaks something much more important.
'''

import sys
import base64
import itertools
import sys

sys.path.append("../toolbox")
import hamming
import tools
import xorcrypto
import scoring

F='6.txt'
#F='test.txt'
#F='6.head.txt'

def decrypt(enc, blocks, hints=[]):
    key = []
    for (idx,block) in enumerate(blocks):
      res = [[scoring.compute(xorcrypto.xor(block, i)),i,xorcrypto.xor(block, i)] for i in range(256)]
      res = sorted(res)
#      for x in res[:-1]: tools.d(x)
      print(res[-5:])
      key.append(res[-1][1])
    print(['key',key])
    dec=xorcrypto.xor(enc, key)#[:80]
    print(dec)
    return (scoring.compute(dec),dec, key)

def main():
    with open(F,'r') as f:
      b64 = f.read()
      enc = base64.b64decode(b64)

#    print(tools.toHex(enc))
    print(['# of bytes >=0x80: ',sum([(x>>7) for x in enc])])
    
    bestScore = 0
    bestDist = 2**30
    for l in range(2,40):
       print('L = ',l)
       bl = tools.transpose(enc, l)
#       for blx in bl:print(tools.toHex(blx))
       
       distances = [hamming.compute(enc[i*l:(i+1)*l], enc[(i+1)*l:(i+2)*l]) for i in range(len(enc)//l - 2)]
       avgDist=sum(distances)/(len(distances)*l)
       print (['dist', l, distances[0]/l,avgDist])
       if bestDist > avgDist:
          bestDist = avgDist
          bestDistL = l
#       print([tools.toHex(x) for x in bl])
       dec = decrypt(enc, bl)
       if (dec[0] > bestScore):
         bestScore = dec[0]
         bestDec = dec[1]
         bestLen = l
         bestKey = dec[2]

    print('*' * 72)
    print(['best[dist=%.3f, keylen=%i]' % (bestDist, bestDistL)])
    print(['best[score,len,key,dec]', bestScore, bestLen, bytes(bestKey), bestDec])
    return 0

if __name__ =='__main__':
  tools.run(main)

