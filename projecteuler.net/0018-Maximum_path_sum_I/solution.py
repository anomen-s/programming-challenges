#!/usr/bin/python
# -*- coding: utf-8 -*-

# Find the maximum total from top to bottom of the triangle below:
LEVELS=15

E_VAL = 0
E_FIRST = 1
E_CHILD = 2
E_L = 3

def readfile(filename):
    f = open(filename)
    try:
       data = f.read(6000)
    finally:
       f.close()
    return data.split()

def init(treedata):
    return [[int(i), False, 0, 0]  for i in treedata]
    
def initRowstarts(treedata):
  result = range(LEVELS)
#  treedata[0][E_FIRST] = True
  for i in xrange(1,LEVELS):
    ri = result[i-1] + i
    result[i] = ri
    treedata[ri][E_FIRST] = True
  return result

def initChildren(treedata):
    next = 0
    for i in xrange(0, len(treedata)):
	next = next + 1
	if treedata[i][E_FIRST]:
	  next = next + 1
	if next < len(treedata):
	  treedata[i][E_CHILD] = next

def printtree(treedata):
  for i in treedata:
   if i[E_FIRST]: 
     print ''
   print i,

def computePaths(treedata):
  for i in xrange(len(treedata)-1, -1, -1):
    node = treedata[i]
    if node[E_CHILD] == 0:
      node[E_L] = node[E_VAL]
    else:
      print node[E_VAL], treedata[node[E_CHILD]][E_L], treedata[node[E_CHILD]+1][E_L]
      node[E_L] = node[E_VAL] + max(treedata[node[E_CHILD]][E_L], treedata[node[E_CHILD]+1][E_L])

treedata_raw = readfile('data.txt')
treedata = init(treedata_raw)
initRowstarts(treedata)
initChildren(treedata)

computePaths(treedata)  

printtree(treedata)



