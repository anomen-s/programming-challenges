#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
Detect single-character XOR

One of the 60-character strings in this file has been encrypted by single-character XOR. 

Find it.
'''

import time
import base64
import sys

sys.path.append("../toolbox")
import tools
import xorcrypto
import scoring

DEBUG = True



T = scoring.initSingleCharTab()

    
    
def main():
    res = []
    with open('4.txt','r') as f:
      for line in f.readlines():
        enc = tools.fromHex(line.strip())
        dec = [[scoring.compute(xorcrypto.xor(enc, i)),i,xorcrypto.xor(enc, i)] for i in range(256)]
        res.extend(dec)
    res = sorted(res)
    for x in res[-20:]: print(x)


def d(args):
    global DEBUG
    if DEBUG:
      print(args)

if  __name__ =='__main__':
  tStart = time.time()
  main()
  print(['time[ms]',int((time.time() - tStart)*1000)])

