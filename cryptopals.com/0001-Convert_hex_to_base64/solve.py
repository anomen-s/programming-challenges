#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
The string: 
49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d

 Should produce: 
SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t
'''

import time
import base64

DEBUG = True


STR = '49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d'

def hex2b64(s):
   '''
     Convert hex string to string
   '''
#    asBytes = bytes.fromhex(s)
    asBytes = base64.b16decode(STR.upper())
    asB64 = base64.b64encode(asBytes)
    return asB64.decode('utf-8')

def main():
    print(hex2b64(STR))
    


def d(args):
    global DEBUG
    if DEBUG:
      print(args)

if  __name__ =='__main__':
  tStart = time.time()
  main()
  print(['time[ms]',int((time.time() - tStart)*1000)])

