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
    h = len(rawboard)
    for y in range(h):
      for x in range(w):
        board[(x,y)] = int(rawboard[y][x] == '#')
          
    return (mapping, board, w, h)

def printb(board, w, h, s):
  print('*'*30, s)
  for y in range(-s, h+s+1):
    for x in range(-s, w+s+1):
      print('#' if board[(x,y)] else ' ', end='')
    print('')

def transform(board, mapping, w, h, step, defval):
  newboard = defaultdict(lambda: defval)
  for y in range(-step, h+step+1):
    for x in range(-step, w+step+1):
      newboard[(x,y)] = int(apply(board, x, y, mapping))
  return newboard

def apply(board, x, y, mapping):
  pos = [(-1,-1),(0,-1),(1,-1),(-1,0),(0,0),(1,0),(-1,1),(0,1),(1,1)]
  binnum = [str(board[(x+p[0], y+p[1])]) for p in pos]
  return mapping[int(''.join(binnum), 2)]


def countdots(board, w, h, s):

  #print('trimmed',x0,x1,y0,y1)
  #print('0',board.get((x0,y0), 'Nope'))
  #print('1',board.get((x1,y1), 'Nope'))
  total = 0
  for y in range(-s, h+s+1):
    for x in range(-s, w+s+1):
      if board[(x,y)]:
        total += 1
  return total

def solve(final):
  mapping, board,w, h = read_input(final)

  # print(mapping)
  #print(list(board))
  #printb(board,w,h,0)
  defval = 0
  for s in range(1, 51):
    defval = mapping[defval * 0x1FF]
    #print(s,end=' ',flush=True)
    board = transform(board, mapping, w, h, s, defval)
    #print('def',defval, s)
    #printb(board, w, h, s)
    if s == 2:
     print('Part1', final, countdots(board, w, h, s))
    if s == 50:
     print('Part2', final, countdots(board, w, h, s))

  #print('')
  #print(len(board))
  #print(boarddim(board))
  #board = shift(steps, board)
  #printb(board)

if __name__ == '__main__':
 print("(expected:   35,  3351)")
 solve(False)
 print('*'*30)
 print("(expected: 5249, 15714)")
 solve(True)
