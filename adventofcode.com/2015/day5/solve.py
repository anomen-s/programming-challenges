#!/usr/bin/env python3

'''
Validate strings according to given rules
'''

def read_input(final, part):
  if (final):
    fname = 'input'
  else:
    fname = 'input.sample' + part
  with open(fname, 'rt') as f:
    return [line.strip() for line in f]

def nice(l, part):
  if part == 1:
     return nice1(l)
  elif part == 2:
     return nice2(l)

def nice1(l):
  prev = ''

  seq2 = False
  vow = 0
  proh = False

  for c in l:
     if c == prev:
        seq2 = True
     if c in 'aeiou':
        vow += 1
     if (prev + c) in ['ab', 'cd', 'pq', 'xy']:
        proh = True
     
     prev = c

  return (vow >= 3) and seq2 and not proh


def nice2(l):
  pairs = {}
  pairs2 = False

  for i in range(1, len(l)):
     p = l[i-1:i+1]
     if (p in pairs) and (pairs[p] < (i-1)):
       pairs2 = True
     if not p in pairs:
       pairs[p] = i

  l2 = False
  for i in range(2, len(l)):
     l2 = l2 or (l[i] == l[i-2])

  return pairs2 and l2


def solve(final, part):
  lines = read_input(final, str(part))
  return sum([nice(l, part) for l in lines])


if __name__ == '__main__':
 print("(expected: %i, %i)" % (2, 2))
 print(solve(False, 1))
 print(solve(False, 2))
 print('*'*30)
 print("(expected: %i, %i)" % (236, 51))
 print(solve(True, 1))
 print(solve(True, 2))
