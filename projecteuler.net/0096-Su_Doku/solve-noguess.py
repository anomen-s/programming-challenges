#!/usr/bin/python2
# -*- coding: utf-8 -*-

# board = list(rows) of list(cells) of list(avail)

def inflateBoard(board):
    sets = []
    # add rows
    sets.extend(board)
    for i in range(9):
      # add columns
      sets.append([board[r][i] for r in range(9)])
    for x in range(0,9,3):
      for y in range(0,9,3):
        # add block
        sets.append(board[y][x:x+3]+board[y+1][x:x+3]+board[y+2][x:x+3])
    return sets

def initCell(val):
    if val > 0:
      return [val];
    return range(1,10)

def elim(row):
    ''' Clean finalized numbers from other cells   '''
    changed  = False
    finals=[]
    for c in row:
      if len(c) == 1:
       finals.append(c[0])
    if len(finals) == 0:
      return
    for f in finals:
      for c in row:
        if len(c) > 1 and (c.count(f) == 1):
          c.remove(f)
          changed = True
    return changed

def clean(row):
    ''' Set final value to cells  '''
    changed = False
    for i in xrange(1,10):
      availcells = 0;
      availcell = None;
      for c in row:
        if c.count(i) == 1:
          availcells = availcells + 1
          availcell = c
      if availcells == 1 and (len(availcell) > 1):
        del availcell[:]
        availcell.append(i)
        changed = True
    return changed

def readboard(lines):
    board = []
    for r in range(9):
      numbers = list(lines.pop(0).strip())
      board.append([initCell(int(n)) for n in numbers])

    #print board
    return board

def solve(board):
    print 'inflate'
    sets = inflateBoard(board)
    changed = True
    while changed:
      changed = False
      for s in sets:
        changed = changed or elim(s)
        changed = changed or clean(s)
    print (board[0][0:3])
    return board

def main():

  with open('p096_sudoku.txt', 'r') as f:
    lines = f.readlines() # read all lines from file
  while len(lines) > 0:
    title = lines.pop(0);
    print title,
    if not title:
      break;
    board = readboard(lines)
    r = solve(board)

if  __name__ =='__main__':main()
