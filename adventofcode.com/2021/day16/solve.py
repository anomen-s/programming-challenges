#!/usr/bin/env python3
import math
'''
Decode packets in hex stream
'''

def read_input(final):
  if (final):
    fname = 'input'
  else:
    fname = 'input.sample'
  with open(fname, 'rt') as f:
    return [line.strip() for line in f]

def binary(h):
 result = ''
 for d in h:
   i = int(d, 16)
   result += format(i, '04b')
 return result

class Stream:
   def __init__(self, data):
     self.stream = data

   def __len__(self):
     return len(self.stream)

   def avail(self):
     return self.stream.find('1') >= 0

   def __repr__(self):
     return str(self.stream)

   def readint(self, num):
      return int(self.read(num), 2)

   def read_encoded_num(self):
      result = ''
      flag = 1
      while flag == 1:
        flag = self.readint(1)
        result += self.read(4)
      return int(result, 2)

   def substream(self, num):
      return Stream(self.read(num))

   def read(self, num):
      if len(self.stream) < num:
        raise EOFError(self.stream, num)
      res = self.stream[:num]
      self.stream = self.stream[num:]
      return res


def read_packet(stream):
    result = []
    ver = stream.readint(3)
    typeId = stream.readint(3)
    # print(ver, typeId)
    if typeId == 4:
      n = stream.read_encoded_num()
      result.append((ver, typeId, 'num', n))
    else:
      lengthTypeId = stream.readint(1)
      result.append((ver, typeId, 'len', lengthTypeId))
      if lengthTypeId == 0:
         subs = stream.substream(stream.readint(15))
         while subs.avail():
           result.extend(read_packet(subs))
      else:
         cnt = stream.readint(11)
         for _ in range(cnt):
           result.extend(read_packet(stream))
    return result

def compute_packet(stream):
    ver = stream.readint(3)
    typeId = stream.readint(3)
    if typeId == 4:
      return stream.read_encoded_num()
    else:
      lengthTypeId = stream.readint(1)
      subvalues = []
      if lengthTypeId == 0:
         subs = stream.substream(stream.readint(15))
         while subs.avail():
           subvalues += [compute_packet(subs)]
      else:
         cnt = stream.readint(11)
         for _ in range(cnt):
           subvalues += [compute_packet(stream)]
      if typeId == 0:
         return sum(subvalues)
      if typeId == 1:
         return math.prod(subvalues)
      if typeId == 2:
         return min(subvalues)
      if typeId == 3:
         return max(subvalues)
      if typeId == 5:
         return int(subvalues[0] > subvalues[1])
      if typeId == 6:
         return int(subvalues[0] < subvalues[1])
      if typeId == 7:
         return int(subvalues[0] == subvalues[1])
      raise ValueError(ver, typeId, subvalues)

def solve(final):
  for row in read_input(final):
    print(row)
    binrow = binary(row)
    packets = read_packet(Stream(binrow))
    print('Part1', sum([p[0] for p in packets]))

    result = compute_packet(Stream(binrow))
    print('Part2', result)


if __name__ == '__main__':
 solve(False)
 print('*'*20)
 solve(True)
