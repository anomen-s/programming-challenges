#!/usr/bin/python
# -*- coding: utf-8 -*-

def readfile(filename):
    f = open(filename)
    try:
       return map(lambda x : x.strip(),  f.readlines())
    finally:
       f.close()

raw_data = readfile('p079_keylog.sorted.txt')

RELS = [[0 for i in xrange(10)] for i in xrange(10)]

NEEDED = [0 for i in xrange(10)]

def add_rel(x, y):
  x = int(x)
  y = int(y)
  global RELS
  global NEEDED
  RELS[x][y] = RELS[x][y] + 1
  NEEDED[x] = 1
  NEEDED[y] = 1
 
# count relations
for pin in raw_data:
 add_rel(pin[0], pin[1])
 add_rel(pin[0], pin[2])
 add_rel(pin[1], pin[2])

# elimination
# in this case it's possible to find solution withou duplicate numbers, so it's trivial

remaining = range(10)
result_prefix = []
result_postfix = []

while reduce(lambda x, y: x + sum(y), RELS, 0) > 0:


  for n in remaining[:]:
    if sum(RELS[n]) == 0:
       for r in RELS:
        print r
       print 'found row %s' % n
       remaining.remove(n)
       for r in xrange(10):
         RELS[r][n] = 0
       if NEEDED[n]:
        result_postfix.insert(0,n)

  for n in remaining[:]:
    if reduce(lambda x,y : x + y[n], RELS, 0) == 0:
       for r in RELS:
        print r
       print 'found col %s' % n
       remaining.remove(n)
       for r in xrange(10):
         RELS[n][r] = 0
       if NEEDED[n]:
         result_prefix.append(n)

# end

print remaining
print result_prefix, result_postfix

