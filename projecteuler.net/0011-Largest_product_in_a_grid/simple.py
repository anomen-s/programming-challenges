#!/usr/bin/python
# -*- coding: utf-8 -*-

DATA=[
0x08,0x02,22,97,38,15,0x00,40,0x00,75,0x04,0x05,0x07,78,52,12,50,77,91,0x08,
49,49,99,40,17,81,18,57,60,87,17,40,98,43,69,48,0x04,56,62,0x00,
81,49,31,73,55,79,14,29,93,71,40,67,53,88,30,0x03,49,13,36,65,
52,70,95,23,0x04,60,11,42,69,24,68,56,0x01,32,56,71,37,0x02,36,91,
22,31,16,71,51,67,63,89,41,92,36,54,22,40,40,28,66,33,13,80,
24,47,32,60,99,0x03,45,0x02,44,75,33,53,78,36,84,20,35,17,12,50,
32,98,81,28,64,23,67,10,26,38,40,67,59,54,70,66,18,38,64,70,
67,26,20,68,0x02,62,12,20,95,63,94,39,63,0x08,40,91,66,49,94,21,
24,55,58,0x05,66,73,99,26,97,17,78,78,96,83,14,88,34,89,63,72,
21,36,23,0x09,75,0x00,76,44,20,45,35,14,0x00,61,33,97,34,31,33,95,
78,17,53,28,22,75,31,67,15,94,0x03,80,0x04,62,16,14,0x09,53,56,92,
16,39,0x05,42,96,35,31,47,55,58,88,24,0x00,17,54,24,36,29,85,57,
86,56,0x00,48,35,71,89,0x07,0x05,44,44,37,44,60,21,58,51,54,17,58,
19,80,81,68,0x05,94,47,69,28,73,92,13,86,52,17,77,0x04,89,55,40,
0x04,52,0x08,83,97,35,99,16,0x07,97,57,32,16,26,26,79,33,27,98,66,
88,36,68,87,57,62,20,72,0x03,46,33,67,46,55,12,32,63,93,53,69,
0x04,42,16,73,38,25,39,11,24,94,72,18,0x08,46,29,32,40,62,76,36,
20,69,36,41,72,30,23,88,34,62,99,69,82,67,59,85,74,0x04,36,16,
20,73,35,29,78,31,90,0x01,74,31,49,71,48,86,81,16,23,57,0x05,54,
0x01,70,54,71,83,51,54,69,16,92,33,48,61,43,52,0x01,89,19,67,48]

W=20
H=len(DATA)/W

print 'Dimensions', W, H

def getXY(x, y):
    return DATA[x + y * W];

def computeH(x, y, l):
    r = 1
    for i in xrange(0,l):
        r = r * DATA[(x + i) + y * W];
    return r;

def computeV(x, y, l):
    r = 1
    for i in xrange(0,l):
        r = r * DATA[x + (y + i) * W];
    return r;

def computeD(x, y, l):
    r = 1
    for i in xrange(0,l):
        r = r * DATA[(x + i) + (y + i) * W];
    return r;

def computeD2(x, y, l):
    r = 1
    for i in xrange(0,l):
        r = r * DATA[(x - i) + (y + i) * W];
    return r;
    
L=4

MAX=0
MAXX=-1
MAXY=-1

for x in xrange(0, W-L):
  for y in xrange(0, H-1):
    r = computeH(x,y,L)
    if (r > MAX):
      MAX = r; MAXX = x; MAXY = y

print MAX, MAXX, MAXY
print ': %s %s ...' % (getXY(MAXX, MAXY), getXY(MAXX+1, MAXY))
MAX=0

for x in xrange(0, W-1):
  for y in xrange(0, H-L):
    r = computeV(x,y,L)
    if (r > MAX):
      MAX = r; MAXX = x; MAXY = y

print MAX, MAXX, MAXY
print ': %s %s ...' % (getXY(MAXX, MAXY), getXY(MAXX, MAXY+1))
MAX=0

for x in xrange(0, W-L):
  for y in xrange(0, H-L):
    r = computeD(x,y,L)
    if (r > MAX):
      MAX = r; MAXX = x; MAXY = y

print MAX, MAXX, MAXY
print ': %s %s ...' % (getXY(MAXX, MAXY), getXY(MAXX+1, MAXY+1))

for x in xrange(L-1, W):
  for y in xrange(0, H-L):
    r = computeD2(x,y,L)
    if (r > MAX):
      MAX = r; MAXX = x; MAXY = y

print MAX, MAXX, MAXY
print ': %s %s ...' % (getXY(MAXX, MAXY), getXY(MAXX-1, MAXY+1))
