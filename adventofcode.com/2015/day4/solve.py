#!/usr/bin/env python3

import hashlib

'''
Find MD5 with first 5 digits equal to zero.
Find MD5 with first 6 digits equal to zero.
'''

DIGITS =  [bytes(str(i), 'utf-8') for i in range(10)]

def read_input(final):
  if (final):
    fname = 'input'
  else:
    fname = 'input.sample'
  with open(fname, 'rb') as f:
    return f.read()

def htest(m, part):
  if part == 1:
    return htest1(m)
  elif part == 2:
    return htest2(m)

def htest1(m):
  d = m.digest()
  #print(d)
  return (d[0] == 0) and (d[1] == 0) and (d[2] < 0x10)

def htest2(m):
  d = m.digest()
  #print(d)
  return (d[0] == 0) and (d[1] == 0) and (d[2] == 0)

def search(m, num, maxlen, part):
  ml = [m.copy() for i in range(10)]
  [ml[i].update(DIGITS[i]) for i in range(len(DIGITS))]

  if maxlen == 1:
    dl = [htest(m, part) for m in ml]
    if sum(dl) > 0:
      return [num+str(i) for i,hit in zip(range(10), dl) if hit][0]
    else:
      return None

  if maxlen > 1:
    for i in range(10):
      r = search(ml[i], num+str(i), maxlen-1, part)
      if r:
        return r


def solve(final, part):
  pw = read_input(final)

  for l in range(1,15):
    m = hashlib.md5()
    m.update(pw)
    # print(pw)
    result = search(m, '', l, part)
    if result:
      return result


if __name__ == '__main__':
 print("(expected: %i, %i)" % (609043, -1))
 print(solve(False, 1))
 print(solve(False, 2))
 print('*'*30)
 print("(expected: %i, %i)" % (117946, 3938038))
 print(solve(True, 1))
 print(solve(True, 2))
