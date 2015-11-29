#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
Write a function that takes a plaintext, determines if it has valid PKCS#7 padding, and strips the padding off. 

The string:
"ICE ICE BABY\x04\x04\x04\x04"

... has valid padding, and produces the result "ICE ICE BABY".

The string:
"ICE ICE BABY\x05\x05\x05\x05"

... does not have valid padding, nor does:
"ICE ICE BABY\x01\x02\x03\x04"

 If you are writing in a language with exceptions, like Python or Ruby, make your function throw an exception on bad padding. 

 Crypto nerds know where we're going with this. Bear with us.
 '''

import sys

sys.path.append("../toolbox")
import tools


TEXT1=b"ICE ICE BABY\x04\x04\x04\x04"
TEXT2=b"ICE ICE BABY\x05\x05\x05\x05"
TEXT3=b"ICE ICE BABY\x01\x02\x03\x04"


def main():

    r1 = tools.stripPadding(TEXT1)
    passed = 1

    try:
      r2 = tools.stripPadding(TEXT2)
    except:
      passed += 1

    try:
      r3 = tools.stripPadding(TEXT3)
    except:
      passed += 1
    
    if passed != 3:
      print('FAILED')
    else:
      print("Passed")

if __name__ =='__main__':
  tools.run(main)

