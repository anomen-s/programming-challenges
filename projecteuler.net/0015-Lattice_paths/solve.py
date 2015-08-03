#!/usr/bin/python3
# -*- coding: utf-8 -*-


DEBUG = True

# count of edges not cells
W=20+1


def d(args):
    global DEBUG
    if DEBUG:
      print(args)

def printBoard(b):
  cell = 0
  for i in b:
    print(i," \t", end='')
    cell = cell + 1
    if (cell == W):
       print ('')
       cell = 0

def xmain():
    print(list(walk(21)))
    
    
def main():
    global W, H
    board = [0 for i in range(W*W)]
    board[W*W-1] = 1
    for i in walk(W):
      cnt = 0
      if (i % W) < (W-1):
        cnt = cnt + board[i+1]
      if i < (W*(W-1)):
        cnt = cnt + board[i+W]
      d('setting %i to %i' % (i, cnt))
      board[i] = cnt
      
    printBoard(board)

def walk(W):
# 0 1 2 3 4
# 5 6 7 8 9
# 0 1 2 3 4
# 5 6 7 8 9
# 0 1 2 3 4
# -> 24 23 19 22 18 14 21 17 13 9 20 16 12 8 4 15 11 7 3 10 6 2 5  1 0
#      -1    -2+5     -3+10     -4+15        -4+15      -3+10 -2+5  -1
    i = W*W-1
    #yield i # do not visit last vertex
    x = 0
    y = -1
    dy = 1
    for t in range(W*W-1):
       if i == (W-1):
         dy = -1
         i = i - x + (y * W)
       elif i < (W-1):
         x = x - 1
         y = y + dy
         i = i - x + (y * W)
       elif (i % W) == (W-1):
         x = x + 1
         y = y + dy
         i = i - x + (y * W)
       else:
         i = i - (W-1)
       yield i


if  __name__ =='__main__':main()
