#!/usr/bin/env python3

'''
Find line crossings.
Part 1: only horiz. and vert. lines.
Part 2: horiz., vert. and diag. lines.
'''

def read_input(final):
  if (final):
    fname = 'input'
  else:
    fname = 'input.sample'
  with open(fname, 'rt') as f:
    lines = [rawline.strip().split()[0:3:2] for rawline in f]
    return [[int(n) for n in l[0].split(',') + l[1].split(',')] for l in lines]

def get_points(l):
  if (l[0] == l[2]):
    return [[l[0], i] for i in range(min(l[1], l[3]), max(l[1], l[3]) + 1)]
  elif (l[1] == l[3]):
    return [[i, l[1]] for i in range(min(l[0], l[2]), max(l[0], l[2]) + 1)]
  if (l[2] < l[0]):
    l = [l[2], l[3], l[0], l[1]]
  delta = (l[3]-l[1])//(l[2]-l[0])
  wx = l[2]-l[0]+1
  return [[l[0]+i, l[1]+i*delta] for i in range(wx)]
  

def solve(final, partNo):
  lines = read_input(final)
  # print(list(lines))
  if partNo == 1:
    lines = [l for l in lines if (l[0] == l[2]) or (l[1] == l[3])]
  plist = [p for l in lines for p in get_points(l)]
  max_x = max([p[0] for p in plist]) + 1
  max_y = max([p[1] for p in plist]) + 1
  # print(max_x, max_y)
  board = [[0]*max_x for y in range(max_y)]

  for p in plist:
    # print(p)
    board[p[1]][p[0]] += 1
  # print(board)

  result = sum([1 for row in board for cell in row if cell > 1])
  print(partNo, final, result)

if __name__ == '__main__':
 solve(False, 1)
 solve(True, 1)
 solve(False, 2)
 solve(True, 2)
