#!/usr/bin/python3
# -*- coding: utf-8 -*-

# QR code - fix, decode, respond

import re
import base64
import urllib.request, urllib.error, urllib.parse
import os.path
import http.cookiejar
import subprocess
from PIL import Image
from PIL import ImageDraw


URL1 = 'http://challenge01.root-me.org/programmation/ch7/'

def main():
  ''' download file and return it as string '''
  cj = http.cookiejar.CookieJar()
  opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
  urllib.request.install_opener(opener)

  inputhtml= urllib.request.urlopen(URL1).readlines()

  print(cj)
  imgdata = parse(inputhtml)
  writedata('img.png', imgdata)
  
  qrfix()
  
  password = qrdecode()
  print (password)
 
  postdata = post_data(password)
  print(postdata)
  
  responsehtml= urllib.request.urlopen(URL1, postdata).readlines()

  resultlines = list(map(lambda x: x.decode("utf-8"), responsehtml))
  for r in resultlines:
    print(r)
    

def post_data(password):
    data = {}
    data['metu'] = password
    pdata = urllib.parse.urlencode(data)
    return bytes(pdata, 'utf-8')
    
def parse(data):
    print ('*****************')
    lines = list(map(lambda x: x.decode("utf-8"), data))
    print (lines)
    
    print ('*****************')

    p1 = re.compile('base64,([^"]+)')
    m1 = p1.search(lines[0])

    result = m1.group(1)
    decoded = base64.b64decode(result)
    print(result)
    return decoded

def qrdecode():
 try:
   result = subprocess.check_output(['/usr/lib/jvm/oracle-jdk-bin-1.7/bin/java',\
      '-cp','zxing/javase-3.2.0.jar:zxing/core-3.2.0.jar',\
      'com.google.zxing.client.j2se.CommandLineRunner',\
      'qrcode.png'])
 except subprocess.CalledProcessError as e:
   if e.returncode > 1:
     print (e.output)
     exit(e.returncode)
   return False

 resultLines = result.decode("utf-8").split('\n')
 for r in resultLines:
    p = re.compile('The key is (/\w+)')
    match = p.match(r);
    if match:
      return match.group(1)
 raise Exception("cannot decode QR: " +str(result))


def readtest(filename):
    with open(filename) as f:
       data = f.read(800)
    return data

def writedata(filename, data):
    with open(filename, 'wb') as f:
       data = f.write(data)



def qrfix():
  BLACK = (0,0,0)
  WHITE =(255,255,255)
  W=9

  im = Image.open("img.png")
  draw = ImageDraw.Draw(im)

  for (x,y) in [(18, 18), (18,218), (218,18)]:
    draw.rectangle((x,y, x+7*W, y+7*W),BLACK, BLACK)
    draw.rectangle((x+W,y+W, x+6*W, y+6*W),WHITE, WHITE)
    draw.rectangle((x+2*W,y+2*W, x+5*W, y+5*W),BLACK, BLACK)

  im.save('qrcode.png')

if  __name__ =='__main__':
    main()
