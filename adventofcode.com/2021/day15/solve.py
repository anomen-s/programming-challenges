#!/usr/bin/env python3
from heapq import heappush, heappop

'''
Find safest path (lowest score) from top-left to bottom-right.
'''

def read_input(final):
  if (final):
    fname = 'input'
  else:
    fname = 'input.sample'
  with open(fname, 'rt') as f:
    return [[int(n) for n in line.strip()] for line in f]

def grow5times(board):
   bb = []
   for repy in range(5):
     for y in range(len(board)):
       r = []
       for repx in range(5):
         r.extend([(c+repy+repx-1)%9+1 for c in board[y]])
       bb.append(r)
   return bb

def solve(final, part2):
  board = read_input(final)
  if part2: board = grow5times(board)
  
  score = [[-1 for x in row] for row in board]
  # print(board)
  w = len(board[0])
  h = len(board)
  # print(w,h)
  q = []
  heappush(q, (0,0,0))
  while len(q) > 0:
    (s, x, y) = heappop(q)
    if score[y][x] < 0:
      currsc = s + board[y][x]
      score[y][x] = currsc
      if y > 0: heappush(q, (currsc, x, y-1))
      if x > 0: heappush(q, (currsc, x-1, y))
      if x < (w-1): heappush(q, (currsc, x+1, y))
      if y < (h-1): heappush(q, (currsc, x, y+1))
  # print(score)
  print('Part2' if part2 else 'Part1', score[h-1][w-1] - score[0][0])


if __name__ == '__main__':
 solve(False, False)
 solve(True, False)
 print('*'*20)
 solve(False, True)
 solve(True, True)
