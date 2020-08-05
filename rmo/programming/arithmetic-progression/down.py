#!/usr/bin/python3
# -*- coding: utf-8 -*-

# compute arithmetic progression

import re
import urllib.request, urllib.error, urllib.parse
import os.path
import http.cookiejar


URL1 = 'http://challenge01.root-me.org/programmation/ch1/'
URL2= 'http://challenge01.root-me.org/programmation/ch1/ep1_v.php?resultat='

def main():
  ''' download file and return it as string '''
  cj = http.cookiejar.CookieJar()
  opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
  urllib.request.install_opener(opener)

  data= urllib.request.urlopen(URL1).readlines()

  print(cj)
  data = list(parse(data))
  print(data)
  result = compute(data)
  
  data = urllib.request.urlopen(URL2 + str(result)).read()
  print (data)
    
def parse(data):
    print ('*****************')
    lines = list(map(lambda x: x.decode("utf-8"), data))
#    lines = str(data.split('\n')
    print (lines)
    
    print ('*****************')

    p1 = re.compile('\[\s+(-?\d+)\s+\+ U<sub>n</sub> \] ([+-]) \[ n \* (-?\d+) \]')
    m1 = p1.search(lines[0])

    p2 = re.compile('=\s+(-?\d+)')
    m2 = p2.search(lines[1])
    
    p3 = re.compile('(-?\d+) de cette ')
    m3 = p3.search(lines[2])
    
    result = map(int, [(m1.group(1)), m1.group(3), m2.group(1), m3.group(1), m1.group(2)+'1'])
    return result

def compute(data):
    a, b, num, it, op = data
    
    for n in range(it+1):
      num = a + num + op * n * b

    return num

def readtest(filename):
    with open(filename) as f:
       data = f.read(800)
    return data

if  __name__ =='__main__':
    main()

    #data = readtest('test.data')
    #print(data)
    #result = compute([40, 5, 122, 7, 1])
    #print(result)
    

