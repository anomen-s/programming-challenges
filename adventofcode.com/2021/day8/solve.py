#!/usr/bin/env python3

'''
Find number of digits which can be ientified by unique number of powered segments in 7-segment display (i.e.: number of digits 1,4,7,8)
'''

def read_input(final):
  if (final):
    fname = 'input'
  else:
    fname = 'input.sample'
  with open(fname, 'rt') as f:
    rawlines = [line.split('|') for line in f]
    return [[l.strip().split() for l in line]  for line in rawlines]

def unwrap(coll):
  if len(coll) != 1:
    raise ValueError(coll)
  return list(coll)[0]

def analyze(digitList):
  digits = [set(d) for d in digitList]
  no1 = unwrap([d for d in digits if len(d) == 2])
  no7 = unwrap([d for d in digits if len(d) == 3])
  no4 = unwrap([d for d in digits if len(d) == 4])
  no8 = unwrap([d for d in digits if len(d) == 7])
  no9 = unwrap([d for d in digits if len(d) == 6 and len(no4 - d) == 0])
  no6 = unwrap([d for d in digits if len(d) == 6 and len(no7 - d) == 1])
  no0 = unwrap([d for d in digits if len(d) == 6 and d != no6 and d != no9])

  segA = unwrap(no7 - no1)
  segG = unwrap(no9 - (set.union(no4, no7)))
  segE = unwrap(no8 - no9)
  segC = unwrap(no9 - no6)
  segF = unwrap(no1 - set([segC]))
  segD = unwrap(no4 - no0)
  segB = unwrap(no4 - no1 - set([segD]))
  
  m = {segA: 'a', segB:'b', segC:'c',segD:'d', segE:'e',segF:'f',segG:'g'}
  #print(m)
  return m

def digitValue(digit):
  d = ''.join(sorted(digit))
  if d == 'abcefg': return '0'
  if d == 'cf': return '1'
  if d == 'acdeg': return '2'
  if d == 'acdfg': return '3'
  if d == 'bcdf': return '4'
  if d == 'abdfg': return '5'
  if d == 'abdefg': return '6'
  if d == 'acf': return '7'
  if d == 'abcdefg': return '8'
  if d == 'abcdfg': return '9'
  raise ValueError(digit)

def solve(final):
  lines = read_input(final)
  # for p1, p2 in lines: print(p2)

  cnt = sum([1 for l in lines for p in l[1] if len(p) in set([2,3,4,7])])
  print('part1:', cnt)

  total = 0
  for l in lines:
    mapping = analyze(l[0])
    total += int(''.join([digitValue([mapping[ch] for ch in d]) for d in l[1]]))
  print('part2', total)

if __name__ == '__main__':
 solve(False)
 solve(True)
