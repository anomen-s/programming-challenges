#!/usr/bin/env python3
import re

'''
Fold transparent paper according input instructions
Part1: count dosts after first step
Part2: display final pattern
'''

def read_input(final):
  if (final):
    fname = 'input'
  else:
    fname = 'input.sample'
  with open(fname, 'rt') as f:
    content = [c.split('\n') for c in f.read().strip().split('\n\n')]
    d = [tuple([int(x) for x in dot.split(',')]) for dot in content[0]]
    return (d, content[1])

def solve(final):
  (dots, steps) = read_input(final)

  board = {}
  w = max([x for (x,y) in dots])+1
  h = max([y for (x,y) in dots])+1
  for dot in dots:
      board[dot] = True

  # print(board)
  # print(steps)
  
  for s in steps:
    spec = re.search('([xy])=(\\d+)', s)
    fold = int(spec[2])
    if spec[1] == 'x':
      for x in range(fold):
        for y in range(h):
          if (2*fold-x,y) in board:
            board[(x,y)] = True
      w = fold
    else:
      for x in range(w):
        for y in range(fold):
          if (x,2*fold-y) in board:
            board[(x,y)] = True
      h = fold

    total = 0
    buffer = ''
    for y in range(h):
      for x in range(w):
          buffer +='#' if (x,y) in board else ' '
          if (x,y) in board:
            total += 1
      buffer += '\n'
    print(s, '->', total, 'dots')

  print('Part2:')
  print(buffer)

if __name__ == '__main__':
 solve(False)
 print('*' * 30)
 solve(True)
