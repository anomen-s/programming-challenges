#!/usr/bin/python
# -*- coding: utf-8 -*-


def readfile(filename):
    f = open(filename)
    try:
       data = f.read(6000)
    finally:
       f.close()
    return data.split(',')

def split_input(data, slices):
    result = [[] for i in xrange(slices)]
    slice = 0
    for i in xrange(len(data)):
      result[slice].append(data[i])
      slice = (slice + 1) % slices
    return result


LETTERSCORES = [0 for i in xrange(255)]

def initscores():
    for a in xrange(ord('a'), ord('z')+1):
       LETTERSCORES[a] = 1
    for a in xrange(ord('A'), ord('Z')+1):
       LETTERSCORES[a] = 1
    for a in xrange(ord('0'), ord('9')+1):
       LETTERSCORES[a] = 1
    for a in ['a', 'e', 'i', 'o', 'n']:
       LETTERSCORES[ord(a)] = 10
    for a in ['t', 'u', 'r', 's', 'h']:
       LETTERSCORES[ord(a)] = 3
    for a in ['A', 'E', 'I', 'O', 'N']:
       LETTERSCORES[ord(a)] = 10
    for a in ['T', 'U', 'R', 'S', 'H', ' ']:
       LETTERSCORES[ord(a)] = 3
    for a in ['=', '|','{','}']:
       LETTERSCORES[ord(a)] = -1
    for a in xrange(122, 255):
       LETTERSCORES[a] = -2
 
raw_data = map(int, readfile('p059_cipher.txt'))
data = split_input(raw_data, 3)

bestres = [0 for i in xrange(len(data))]

initscores()

for l in  xrange(len(data)):
 best = 0
 print 'char#', l
 for c in xrange(ord('a'), ord('z')+1):
    decr = map(lambda x : c ^ x,  data[l])
    score = reduce(lambda x, y : x + LETTERSCORES[y], decr, 0 )
    if score >= best:
       bestres[l] = decr
       best = score
       print 'password char guess =', chr(c), '- score =',score

print map(sum, bestres), 'result =', sum(map(sum, bestres))

res = '';
for i in xrange(len(data)):
  while len(bestres[0]) > 0:
    if len(bestres[0]) > 0:
      res = res + chr(bestres[0].pop(0))
    if len(bestres[1]) > 0:
      res = res + chr(bestres[1].pop(0))
    if len(bestres[2]) > 0:
      res = res + chr(bestres[2].pop(0))

print res
