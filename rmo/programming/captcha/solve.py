#!/usr/bin/python3
# -*- coding: utf-8 -*-

# break simple CAPTCHA

import re
import base64
import urllib.request, urllib.error, urllib.parse
import os.path
import http.cookiejar
import subprocess
from PIL import Image
from PIL import ImageDraw


URL1 = 'http://challenge01.root-me.org/programmation/ch8/'

def main():
  ''' download file and return it as string '''
  cj = http.cookiejar.CookieJar()
  opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
  urllib.request.install_opener(opener)

  inputhtml= urllib.request.urlopen(URL1).readlines()

  print(cj)
  imgdata = parse(inputhtml)
  writedata('img.png', imgdata)
  
  ocrfix()
  
  password = ocrdecode()
  print (password)
 
  postdata = post_data(password)
  print(postdata)

  responsehtml= urllib.request.urlopen(URL1, postdata).readlines()

  resultlines = list(map(lambda x: x.decode("utf-8"), responsehtml))
  for r in resultlines:
    print(r)
    

def post_data(password):
    data = {}
    data['cametu'] = password
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

def ocrdecode():
 try:
   result = subprocess.check_output(['gocr','img-clean.png'])
 except subprocess.CalledProcessError as e:
   if e.returncode > 1:
     print (e.output)
     exit(e.returncode)
   return False

 return result.decode("utf-8").strip()


def writedata(filename, data):
    with open(filename, 'wb') as f:
       data = f.write(data)



def ocrfix():
  BLACK = (0,0,0)
  WHITE =(255,255,255)

  im = Image.open('img.png')
  px = im.load()

  for x in range(250):
    for y in range(50):
      if (px[x,y] == BLACK):
        px[x,y] = WHITE

  im.save('img-clean.png')


if  __name__ =='__main__':
    main()
