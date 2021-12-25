#!/usr/bin/env python3
from collections import defaultdict

'''
Image filtering
'''

def read_input(final):
  if (final):
    fname = 'input'
  else:
    fname = 'input.sample'
  with open(fname, 'rt') as f:
    c = [line.strip() for line in f]
    mapping = [1 if m=='#' else 0 for m in c[0]]
    rawboard = c[2:]
    board = defaultdict(lambda: 0)
    w = len(rawboard[0])
    for y in range(len(rawboard)):
      for x in range(w):
        if rawboard[y][x] == '#':
          board[(x,y)] = 1
    return (mapping, board)

def shift(steps, board):
 w = len(board[0])
 top = ['.' * (w+steps) for _ in range(steps)]
 return top + ['.'*steps + row for row in board]


def boarddim(board):
  minx=min([x for (x,y) in board])
  miny=min([y for (x,y) in board])
  maxx=max([x for (x,y) in board])
  maxy=max([y for (x,y) in board])
  return (minx, maxx, miny, maxy)

def printb(board):
  (minx, maxx, miny, maxy) = boarddim(board)
  print('*'*30)
  for y in range(miny, maxy+1):
    for x in range(minx, maxx+1):
      print('#' if (x,y) in board else ' ', end='')
    print('')

def transform(board, mapping):
  newboard = defaultdict()
  (x0,x1,y0,y1) = boarddim(board)
  for y in range(y0-12, y1+12):
    for x in range(x0-12, x1+12):
      if apply(board, x, y, mapping):
        newboard[(x,y)] = '#'
  return newboard

def apply(board, x, y, mapping):
  pos = [(-1,-1),(0,-1),(1,-1),(-1,0),(0,0),(1,0),(-1,1),(0,1),(1,1)]
  binnum = ['1' if (x+p[0], y+p[1]) in board else '0' for p in pos]
  return mapping[int(''.join(binnum), 2)]


def countdots(board):
  (x0,x1,y0,y1) = boarddim(board)
  #print('all', x0,x1,y0,y1)
  while (x0,(y0+y1)//2-10) in board and (x0,(y0+y1)//2+10) in board:
    x0+=1
  while (x1,(y0+y1)//2-10) in board and (x1,(y0+y1)//2+10) in board: 
    x1-=1
  while ((x0+x1)//2+10, y0) in board and ((x0+x1)//2+10, y0) in board:
    y0+=1
  while ((x0+x1)//2-10, y1) in board and ((x0+x1)//2+10, y1) in board:
    y1-=1

  #print('trimmed',x0,x1,y0,y1)
  #print('0',board.get((x0,y0), 'Nope'))
  #print('1',board.get((x1,y1), 'Nope'))
  total = 0
  for y in range(y0, y1+1):
    for x in range(x0, x1+1):
      if (x,y) in board:
        total += 1
  return total


  
def solve(final, steps):
  mapping, board = read_input(final)
  
  #print(mapping)
  #print(list(board))
  #printb(board)
  
  for s in range(steps):
    #print(s)
    board = transform(board, mapping)
    #printb(board)
  #print(len(board))
  #print(boarddim(board))
  print('Part1', countdots(board))
  #board = shift(steps, board)
  #printb(board)



if __name__ == '__main__':
 print("(expected:   35)", end=' ')
 solve(False, 2)
 #solve(False, 50)
 print("(expected: 5249)", end=' ')
 solve(True, 2)
 #solve(True, 50)
