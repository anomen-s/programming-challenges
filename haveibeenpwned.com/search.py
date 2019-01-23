#!/usr/bin/env python3

# search in ordered sha1 password list
# https://haveibeenpwned.com/Passwords

import os.path
import sys
import re
import hashlib

def testBlock(data, target):
  p = re.compile('[0-9A-F]{40}')
  matches = p.findall(data)
  if len(matches) < 1:
    raise Exception('invalid data: ' + str(data))

  if target in matches:
    printResult(data, target)
    return None
  if matches[-1] < target:
    debug(['u', matches[-1], target])
    return False
  if matches[0] > target:
    debug(['l',matches[0], target])
    return True
  print('NOT FOUND')
  return None

def printResult(data, target):
    p = re.compile(target + ':[0-9]*')
    res = p.search(data)
    print(res.group(0))


def searchFor(target):
  FN='pwned-passwords-sha1-ordered-by-hash-v4.txt'
  SIZE=os.path.getsize(FN)
  start = 0
  end = SIZE-45
  found = False
  target = target.upper()
  with open(FN) as f:
   while not found:
    newPos = (end + start) // 2
    debug([start,newPos,end])
    f.seek(max(0,newPos-50), 0)
    block = f.read(1000)
    down = testBlock(block, target)
    debug([down])
    if down == None:
      return
    if down:
      end = newPos
    else:
      start = newPos

def debug(val):
  if 1==0:
    print(val)

def main():
 pwd = 'start';
 while pwd:
  pwd=input()
  m = hashlib.sha1()
  m.update(bytes(pwd, 'utf-8'))
  digest = m.hexdigest()
  print(digest)
  searchFor(digest)

if len(sys.argv) > 1:
 for a in sys.argv[1:]:
   print(a)
   searchFor(a)
else:
 main()
