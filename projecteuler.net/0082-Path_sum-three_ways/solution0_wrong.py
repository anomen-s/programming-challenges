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
    return [map(lambda n: [int(n), False, 0, 0], x.split(',')) for x in data]

def printm(M):
  for r in M:
    print r

#node data
iVal = 0
iVisit = iPath = 1
iX = 2
iY = 3

#print M0[0]
#exit()
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
 M[start][0][iVisit] =  M[start][0][iVal];
 queue = PriorityQueue()
 queue.put((0, M[start][0]))
 while not queue.empty():
  node = queue.get()[1]
  print 'Processsing node', node
  minN = 2**20
  foundN = False
  # find neighbors
  for dir in [[1,0],[0,1],[-1,0],[0,-1]]:
     nbrX = node[iX] + dir[0]
     nbrY = node[iY] + dir[1]
     if nbrX >= 0 and nbrX < DIM and nbrY >= 0 and nbrY < DIM:
       nbr = M[nbrY][nbrX]
       print 'check neighbour:', nbr
     
       if nbr[iVisit]:
         print 'neighbour visited'
         if  dir[0] < 1: #visited, don't go left
          minN = min(minN, nbr[iVisit])
          print 'neighbour path computed', minN
          foundN = True
       else:
         if dir[0] > -1: #visited, don't go left
#           print 'add', nbr
           queue.put((nbr[iVal],nbr)) # WRONG: must be + node[iVisit]
  if foundN:
    node[iVisit] =  node[iVal] + minN
    print node, 'connected to' , minN
  else:
    print 'uncon', node
    if node[iVal] != 11:
     printm(M)
#     die()
#    raise Exception('unconnected node')

 print 'result ', start
 printm(M)
 cmin = min(row[DIM-1][iVisit] for row in M)
 print 'cmin', start, '=', cmin
 MIN = min(MIN,cmin)

 print 'min', MIN
