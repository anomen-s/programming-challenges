#!/usr/bin/python2
# -*- coding: utf-8 -*-

import copy
# board = list(rows) of list(cells) of list(avail)

def printBoard(board):
    i = 0
    ir = 0
    for row in board:
      if ir == 3 or ir == 6: print ('-'*24)
      ir = ir + 1
      for cell in row:
        if i % 3 == 0: print '|',
        i = i + 1
        if len(cell) > 1:
          print '_',
        else:
          print cell[0],
      print ''

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

def isSolved(board):
    for row in board:
      for cell in row:
        if (len(cell) == 0):
          raise Exception('no remaining available num in cell')
        if (len(cell) > 1):
          return False
    return True

def guess(board, maxg):
    for glen in xrange(2,6):
      for ir in xrange(9):
        for ic in xrange(9):
          if len(board[ir][ic]) == glen:
            for cellVal in board[ir][ic]:
              gboard = copy.deepcopy(board)
              gboard[ir][ic] = [cellVal]
              #print 'try[%i] %i at %i,%i ' % (glen, cellVal, ic, ir)
              try:
                eliminateBoard(gboard)
                if isSolved(gboard):
                  return gboard
              except Exception as e:
                ignoreException = True
                #print 'not valid'
              if maxg > 1:
                #print 'guess another num'
                g2 = guess(gboard, maxg-1)
                if g2 and isSolved(gboard):
                  return g2
    return None

def elim(row):
    ''' Clean finalized numbers from other cells   '''
    changed  = False
    finals=[]
    for c in row:
      if len(c) == 1:
        finals.append(c[0])
      elif len(c) == 0:
        raise Exception('no remaining available num in cell')
    if len(finals) == 0:
      return
    for f in finals:
      for c in row:
        if len(c) > 1 and (c.count(f) == 1):
          c.remove(f)
          changed = True
    return changed

def setCell(cell, newVal):
    del cell[:]
    cell.append(newVal)
    return cell

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
      if availcells == 0:
        raise Exception('no remaining cell for ' + str(i))
      if availcells == 1 and (len(availcell) > 1):
        setCell(availcell, i)
        changed = True
    return changed

def readboard(lines):
    board = []
    for r in range(9):
      numbers = list(lines.pop(0).strip())
      board.append([initCell(int(n)) for n in numbers])

    #print board
    return board

def eliminateBoard(board):
    sets = inflateBoard(board)
    changed = True
    while changed:
      changed = False
      for s in sets:
        changed = changed or elim(s)
        changed = changed or clean(s)
    return board

def solve(board):
    #printBoard(board)
    #print 'inflate'
    eliminateBoard(board)

#    for r in board:print r
#    printBoard(board)
    #print (board[0][0:3])
    
    if not isSolved(board):
      #print 'not solved'
      for guesses in [1]: # seems to be enough
        gboard = guess(board, guesses)
        if gboard and isSolved(gboard):
          #printBoard(board)
          return gboard

    return board


def main():
  RES = 0;
  
  with open('p096_sudoku.txt', 'r') as f:
    lines = f.readlines() # read all lines from file

  while len(lines) > 0:
    title = lines.pop(0);
    print title,
    if not title:
      break;
    board = readboard(lines)
    r = solve(board)
    printBoard(r)
    if not isSolved(r):
      print("not solved")
      exit(1)
    
    RES = RES + reduce(lambda x,y: x*10+y[0], r[0][0:3],0)

  print RES    

if  __name__ =='__main__':main()
