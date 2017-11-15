#!/usr/bin/env python3

import re
import base64
from urllib import parse


def main():
  records = list(parseFile('server.log'))
  
  delays(records)
  bits(records)
  res = sumbits(records)
  for x in records : print(x)
  
  print(''.join([chr(x) for x in res]))

def parseFile(name):

 with open(name, 'rt') as f:

  for line in f.readlines():
    res = parseLine(line)
    if (res):
      yield res


def parseLine(line):
  p = re.compile('.*2017:\d\d:\d\d:(\d\d).*command=(\w+%?\w*) HTTP.*')
  pNum = re.compile('\d+')
  match = p.match(line)
  if match:
      m = match.groups();
      # print([m[0], base64.b64decode(m[1])])
      cmd = str(base64.b64decode(parse.unquote(m[1])))
      nums = pNum.findall(cmd)
      numsr=[nums[0],nums[2],nums[6]]
      return [m[0],  numsr]

  return None

def delays(records):
  last = None
  for record in records:
    if (last):
      last.append(diff(record[0],last[0]))
    last = record

def bits(records):
 for record in records:
  if (len(record) < 3):
    record.append(-1)
    record.append(0)
  elif (record[2] == 0):
    record.append(0)
  elif (record[2] == 2):
    record.append(1)
  elif (record[2] == 4):
    record.append(2)
  elif (record[2] == 6):
    record.append(3)
  else:
    record.append(0)
  
def sumbits(records):
  res = [0]*90
  for record in records:
    cmd = record[1]
    i = int(cmd[0])
    p = 7-int(cmd[1])
    res[i] = res[i] + record[3]*(2**p)
  return res

def diff(a,b):
  ai = int(a)
  bi = int(b)
  if ai >= bi:
    return ai-bi
  else:
    return ai+60-bi

if  __name__ =='__main__':
  main()
