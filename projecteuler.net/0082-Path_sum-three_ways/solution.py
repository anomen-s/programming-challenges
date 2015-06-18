#!/usr/bin/python
# -*- coding: utf-8 -*-
from Queue import PriorityQueue 


FILENAME='sample.txt'
FILENAME='sample2.txt'
FILENAME='p082_matrix.txt'

def readfile(filename):
    f = open(filename)
    try:
       data = f.readlines()
    finally:
       f.close()
    return [map(lambda n: [int(n), False, 2**30, 0, 0], x.split(',')) for x in data]

def printm(M):
  for r in M:
    print r

def cadd(x, node):
  if node[iVisit]:
    return x+1
  else:
    return x

def countProgress(M):
 return sum( [reduce(cadd, r, 0) for r in M])
 
#node data
iVal = 0
iVisit = 1
iPath = 2
iX = 3
iY = 4

M = readfile(FILENAME)
DIM=len(M)

MIN=2**20

for start in xrange(DIM): 
 M = readfile(FILENAME)

 for x in xrange(DIM):
  for y in xrange(DIM):
#   print x, y, iX, M0[y]
    M[y][x][iX] = x
    M[y][x][iY] = y

 print 'start', start
 M[start][0][iPath] =  M[start][0][iVal];
# M[start][0][iVisit] = True;
 startNode=True
 queue = PriorityQueue()
 queue.put((0, M[start][0]))
 while not queue.empty():
  node = queue.get()[1]
#  print 'Progress', countProgress(M)
  if startNode or not node[iVisit]:
#   print 'already visited', node
#  else:
#   print 'Processsing node', node
   minN = 2**20
   foundN = False
   # find Visited  neighbors
   for dir in [[0,1],[-1,0],[0,-1]]:
      nbrX = node[iX] + dir[0]
      nbrY = node[iY] + dir[1]
      if nbrX >= 0 and nbrX < DIM and nbrY >= 0 and nbrY < DIM:
        nbr = M[nbrY][nbrX]
#        print 'check neighbour:', nbr
      
        if nbr[iVisit]:
#           print 'neighbour visited', nbr
           minN = min(minN, nbr[iPath])
#           print 'neighbour path computed', minN
           foundN = True
   if startNode:
     node[iVisit] = True
   if foundN:
     node[iPath] =  node[iVal] + minN
     node[iVisit] = True
#     print node, 'connected to' , minN, 'total', node[iPath]
   else:
     print 'uncon', node
   if not node[iVisit]:
      printm(M)
      die(1)
   for dir in [[1,0],[0,1],[0,-1]]:
#      print 'check neighbour:', dir, 'from', node
      nbrX = node[iX] + dir[0]
      nbrY = node[iY] + dir[1]
      if nbrX >= 0 and nbrX < DIM and nbrY >= 0 and nbrY < DIM:
        nbr = M[nbrY][nbrX]
#        print 'check neighbour:', nbr
     
        if not nbr[iVisit]:
#          print 'Adding', nbr, 'to', queue.qsize()
          queue.put((nbr[iVal]+node[iPath],nbr))
#     die()
#    raise Exception('unconnected node')
  startNode=False

 print 'result ', start
# printm(M)
 cmin = min(row[DIM-1][iPath] for row in M)
 print 'cmin', start, '=', cmin
 MIN = min(MIN,cmin)

 print 'min', MIN
