#!/usr/bin/env python3
from heapq import heappush, heappop
from collections import defaultdict

'''
Find when sea cucumbers stop moving
'''

def read_input(inputfile):
  if (inputfile):
    fname = 'input.' + inputfile
  else:
    fname = 'input'
  with open(fname, 'rt') as f:
    return [list(line.strip()) for line in f]

def printb(board, s):
  print('*'*30, s)
  for y in range(0, len(board)):
    for x in range(0, len(board[0])):
      print(board[y][x], end='')
    print('')

def solve(inputfile):
  board = read_input(inputfile)

  # printb(board, 'start')

  w = len(board[0])
  h = len(board)
  for s in range(1, int(10e4)):
     # board only with south facing c.
     result1 = [['v' if board[y][x] == 'v' else '.' for x in range(w)] for y in range(h)]

     # move east
     for y in range(h):
       for x in range(w):
         if board[y][x] == '>':
           if board[y][(x+1) % w] == '.':
             result1[y][(x+1) % w] = '>'
           else:
             result1[y][x] = '>'

     # board only with east facing c. (after they moved)
     result = [[result1[y][x] if result1[y][x] != 'v' else '.' for x in range(w)] for y in range(h)]

     # move south
     for y in range(h):
       for x in range(w):
         if board[y][x] == 'v':
           if (board[(y+1) % h][x] != 'v') and (result1[(y+1) % h][x] == '.'):
             result[(y+1) % h][x] = 'v'
           else:
             result[y][x] = 'v'

     #printb(result, s)
     if board == result:
       print('Part1', s)
       
       break
     board = result

  #printb(board,w,h,0)

if __name__ == '__main__':
 #solve('tiny')
 print("(expected:   58)")
 solve('sample')
 print('*'*30)
 print("(solved: 419)")
 solve('')
